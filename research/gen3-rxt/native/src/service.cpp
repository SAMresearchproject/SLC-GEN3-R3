#include "service.hpp"
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/stat.h>
#include <unistd.h>
#include <csignal>
#include <cerrno>
#include <cstring>
#include <iostream>
#include <stdexcept>

namespace rxt {
namespace {
volatile sig_atomic_t stopping=0;
void stop(int){stopping=1;}
struct Socket {
    int fd=-1;
    Socket():fd(::socket(AF_UNIX,SOCK_STREAM|SOCK_CLOEXEC,0)){if(fd<0)throw std::runtime_error("Cannot create native domain socket");}
    explicit Socket(int descriptor):fd(descriptor){}
    ~Socket(){if(fd>=0)::close(fd);}
};
sockaddr_un address(const std::filesystem::path& path){
    sockaddr_un a{};a.sun_family=AF_UNIX;auto s=std::filesystem::absolute(path).string();
    if(s.size()>=sizeof(a.sun_path))throw std::invalid_argument("Native socket path is too long");
    std::memcpy(a.sun_path,s.c_str(),s.size()+1);return a;
}
void send_all(int fd,const std::string& text){
    size_t at=0;while(at<text.size()){auto n=::send(fd,text.data()+at,text.size()-at,MSG_NOSIGNAL);if(n<0&&errno==EINTR)continue;if(n<=0)throw std::runtime_error("Native domain client disconnected");at+=size_t(n);}
}
json answer(Engine& engine,const std::string& line){
    try{return {{"ok",true},{"result",engine.execute(json::parse(line))}};}
    catch(const std::exception& e){return {{"ok",false},{"error",e.what()}};}
}
}
int domain_service(const std::filesystem::path& path,const std::filesystem::path& source,const std::filesystem::path& store){
    Engine engine;
    engine.execute({{"op","ATTACH"},{"payload",{{"directory",store.string()}}}});
    if(read_json(source/"BUNDLE.json").value("schema","")=="GEN3_RXT_JOINT_SOURCE_V1") {
        engine.execute({{"op","JOINT_COMPILE"},{"payload",{{"directory",source.string()}}}});
    } else if(read_json(source/"BUNDLE.json").value("schema","")=="SB_GEN3_RXT_SOURCE_V1") {
        engine.execute({{"op","SB_COMPILE"},{"payload",{{"directory",source.string()}}}});
    } else {
        engine.execute({{"op","ATOM3D_COMPILE"},{"payload",{{"directory",source.string()}}}});
        for(auto op:{"LI6_PHASE_CENSUS","LI6_GRAMMAR","LI6_ASSEMBLY"})engine.execute({{"op",op}});
    }
    if(std::filesystem::exists(source/"core/MANIFEST.json"))engine.execute({{"op","GEN3_CORE_SYNC"},{"payload",{{"directory",(source/"core").string()}}}});
    if(std::filesystem::exists(source/"training/BUNDLE.json"))engine.execute({{"op","TRAIN_COMPILE"},{"payload",{{"directory",(source/"training").string()}}}});
    if(std::filesystem::exists(source/"horizon/BUNDLE.json"))engine.execute({{"op","SB_HORIZON_COMPILE"},{"payload",{{"directory",(source/"horizon").string()}}}});
    if(std::filesystem::exists(source/"rh/BUNDLE.json"))engine.execute({{"op","RH_COMPILE"},{"payload",{{"directory",(source/"rh").string()}}}});
    Socket listener;auto a=address(path);
    // An existing socket belongs to its existing service until explicitly stopped.
    if(::bind(listener.fd,reinterpret_cast<sockaddr*>(&a),sizeof(a))!=0)throw std::runtime_error("Cannot bind native domain socket: "+std::string(std::strerror(errno)));
    struct Cleanup {std::filesystem::path path;~Cleanup(){::unlink(path.c_str());}} cleanup{std::filesystem::absolute(path)};
    if(::chmod(a.sun_path,0600)!=0||::listen(listener.fd,16)!=0)throw std::runtime_error("Cannot configure native domain socket");
    struct sigaction action{};action.sa_handler=stop;sigemptyset(&action.sa_mask);sigaction(SIGTERM,&action,nullptr);sigaction(SIGINT,&action,nullptr);
    std::cout<<json({{"status","READY"},{"socket",a.sun_path},{"pid",getpid()},{"machine",engine.execute({{"op","STATUS"}})}}).dump()<<std::endl;
    while(!stopping){
        Socket client(::accept4(listener.fd,nullptr,nullptr,SOCK_CLOEXEC));
        if(client.fd<0){if(errno==EINTR)continue;throw std::runtime_error("Native domain accept failed");}
        try{
            std::string pending;char block[8192];
            while(!stopping){auto n=::recv(client.fd,block,sizeof(block),0);if(n<0&&errno==EINTR)continue;if(n<=0)break;pending.append(block,size_t(n));
                if(pending.size()>16*1024*1024)throw std::invalid_argument("Native domain request exceeds 16 MiB");
                size_t end;while((end=pending.find('\n'))!=std::string::npos){auto line=pending.substr(0,end);pending.erase(0,end+1);send_all(client.fd,answer(engine,line).dump()+"\n");}
            }
        }catch(const std::exception& e){std::cerr<<json({{"client_error",e.what()}}).dump()<<std::endl;}
    }
    engine.execute({{"op","CHECKPOINT"}});return 0;
}
int domain_client(const std::filesystem::path& path,const std::filesystem::path& job){
    auto requests=read_json(job);if(!requests.is_array())throw std::invalid_argument("Native client job must be an array");Socket socket;auto a=address(path);
    if(::connect(socket.fd,reinterpret_cast<sockaddr*>(&a),sizeof(a))!=0)throw std::runtime_error("Cannot connect to native domain service");
    bool failed=false;std::string pending;char block[8192];
    for(const auto& request:requests){send_all(socket.fd,request.dump()+"\n");size_t end;
        while((end=pending.find('\n'))==std::string::npos){auto n=::recv(socket.fd,block,sizeof(block),0);if(n<0&&errno==EINTR)continue;if(n<=0)throw std::runtime_error("Native ATOM3D service ended before replying");pending.append(block,size_t(n));}
        auto response=json::parse(pending.substr(0,end));pending.erase(0,end+1);failed|=!response.at("ok").get<bool>();std::cout<<response.dump()<<'\n';
    }
    return failed?1:0;
}
}
