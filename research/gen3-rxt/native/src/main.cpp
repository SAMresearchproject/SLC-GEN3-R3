#include "engine.hpp"
#include "service.hpp"
#include <algorithm>
#include <chrono>
#include <iostream>
#include <stdexcept>

using namespace rxt;
static void check(bool condition,const std::string& message) { if(!condition) throw std::runtime_error(message); }
static json compile(Engine& e,const std::filesystem::path& p) {
    return e.execute({{"op","COMPILE"},{"payload",{{"source",read_json(p)}}}});
}
static Batch sample(const Contract& c,size_t count,size_t steps) {
    if(count==0||count>1048576||steps>4096||count*(steps+1)>134217728) throw std::invalid_argument("Benchmark shape outside bounded runner");
    Batch b; b.count=count; b.steps=steps; b.initial.resize(count); b.events.resize(count*steps);
    uint64_t state=20260911;
    auto random=[&]() { state=state*6364136223846793005ULL+1442695040888963407ULL; return state>>32; };
    for(size_t i=0;i<count;++i) b.initial[i]=c.tables.addresses[random()%c.tables.addresses.size()];
    for(auto& event:b.events) event=uint16_t(random()%c.tables.events.size());
    return b;
}
static json validate(const std::filesystem::path& basis) {
    Engine e; json rows=json::array(); uint64_t values=0;
    auto oracle=read_json(basis/"oracle.json");
    for(const auto& f:oracle) {
        compile(e,basis/f.at("contract_file").get<std::string>()); const auto& c=e.contract();
        check(c.id==f["contract_id"].get<std::string>(),"R3 contract identity differs");
        check(c.tables.addresses.size()==f["states"].size(),"R3 state domain differs");
        for(size_t i=0;i<c.tables.addresses.size();++i) {
            auto a=c.tables.addresses[i];
            check(c.decode(a)==f["states"][i],"R3 state order differs");
            check(c.frame(a)==f["frames"][i],"R3 receiver differs");
            check(c.tables.contacts[i]==f["contacts"][i],"R3 action differs");
            values+=c.tables.channels+1+c.coordinates.size();
        }
        Batch b; b.count=c.tables.addresses.size()*c.labels.size(); b.steps=1;
        b.initial.reserve(b.count); b.events.reserve(b.count);
        for(auto address:c.tables.addresses) for(size_t ev=0;ev<c.labels.size();++ev) { b.initial.push_back(address); b.events.push_back(uint16_t(ev)); }
        auto cpu=e.run(b,"cpu"),gpu=e.run(b,"cuda");
        check(cpu.states==gpu.states&&cpu.actions==gpu.actions,"CPU/GPU native batch differs");
        for(size_t lane=0;lane<b.count;++lane) {
            auto expected=f["transitions"][lane/c.labels.size()][lane%c.labels.size()];
            check(c.decode(gpu.states[b.count+lane])==expected,"R3 transition differs");
            values+=c.coordinates.size()+1;
        }
        auto table=e.execute({{"op","VERIFY_GPU_TABLES"}}); values+=table["exact_values"].get<uint64_t>();
        rows.push_back({{"source",f["contract_file"]},{"states",c.tables.addresses.size()},
                       {"transitions",b.count},{"gpu_receiver_values",table["exact_values"]},{"status","PASS"}});
    }
    auto map=e.execute({{"op","T18_MAP_HASH"}});
    check(map["sha256_big_endian"]==read_json(basis/"t18.json")["map_sha256_big_endian"],"Frozen T18 map hash differs");
    return {{"status","PASS"},{"basis","SLC-GEN3-R3"},{"sources",rows},{"exact_comparisons",values},
            {"t18",map},{"machine",e.execute({{"op","STATUS"}})}};
}
static json bench(const std::filesystem::path& source,size_t count,size_t steps) {
    Engine e; compile(e,source); auto b=sample(e.contract(),count,steps);
    auto first_start=std::chrono::steady_clock::now();
    auto cold=e.run(b,"cuda");
    double first_wall=std::chrono::duration<double>(std::chrono::steady_clock::now()-first_start).count();
    auto cpu=e.run(b,"cpu");
    check(cold.states==cpu.states&&cold.actions==cpu.actions,"Cold CUDA/CPU benchmark output differs");
    json rows=json::array();
    for(int i=0;i<3;++i) {
        cpu=e.run(b,"cpu");
        auto gpu=e.run(b,"cuda");
        check(gpu.states==cpu.states&&gpu.actions==cpu.actions,"Warm CUDA/CPU benchmark output differs");
        rows.push_back({{"cpu_wall_seconds",cpu.wall_seconds},{"kernel_seconds",gpu.kernel_seconds},{"wall_seconds",gpu.wall_seconds},
                       {"host_overhead_and_transfers_seconds",gpu.transfer_seconds},
                       {"kernel_writes_per_second",double(count*steps)/gpu.kernel_seconds},
                       {"wall_writes_per_second",double(count*steps)/gpu.wall_seconds},
                       {"cpu_wall_over_gpu_wall",cpu.wall_seconds/gpu.wall_seconds}});
    }
    return {{"status","PASS"},{"histories",count},{"writes_per_history",steps},{"writes",count*steps},
            {"returned_state_and_action_values",cpu.states.size()*2},{"cpu_wall_seconds",cpu.wall_seconds},{"cpu_workers_used",cpu.cpu_workers},
            {"first_cuda_submission_including_table_compile_seconds",first_wall},{"warm_cuda_runs",rows},
            {"comparison","same initial states, events, complete packed state/action histories; receiver expansion and durable commits excluded"},
            {"resources",e.resources().describe()}};
}
int main(int argc,char** argv) {
    try {
        if(argc<2) throw std::invalid_argument("Usage: gen-rxt serve | status | run SOURCE JOB STORE | atom3d SOURCE JOB [STORE] | daemon SOCKET SOURCE STORE | call SOCKET JOB | validate BASIS | bench SOURCE [COUNT STEPS]");
        std::string command=argv[1];
        if(command=="daemon"&&argc==5)return domain_service(argv[2],argv[3],argv[4]);
        if(command=="call"&&argc==4)return domain_client(argv[2],argv[3]);
        if(command=="serve") {
            Engine engine; std::string line;
            while(std::getline(std::cin,line)) {
                try { auto request=json::parse(line); auto result=engine.execute(request); std::cout<<json({{"ok",true},{"result",result}}).dump()<<std::endl; }
                catch(const std::exception& e) { std::cout<<json({{"ok",false},{"error",e.what()}}).dump()<<std::endl; }
            }
        } else if((command=="starbreaker"||command=="joint")&&argc==5) {
            Engine engine;
            engine.execute({{"op","ATTACH"},{"payload",{{"directory",argv[4]}}}});
            engine.execute({{"op",command=="joint"?"JOINT_COMPILE":"SB_COMPILE"},{"payload",{{"directory",argv[2]}}}});
            auto job=read_json(argv[3]); check(job.is_array(),"Starbreaker job must be an array");
            for(const auto& request:job) std::cout<<json({{"op",request.at("op")},{"result",engine.execute(request)}}).dump()<<'\n';
        } else if(command=="atom3d"&&argc>=4&&argc<=5) {
            Engine engine;
            if(argc==5) engine.execute({{"op","ATTACH"},{"payload",{{"directory",argv[4]}}}});
            engine.execute({{"op","ATOM3D_COMPILE"},{"payload",{{"directory",argv[2]}}}});
            auto job=read_json(argv[3]);
            check(job.is_array(),"ATOM3D job must be an array of native requests");
            for(const auto& request:job) std::cout<<json({{"op",request.at("op")},{"result",engine.execute(request)}}).dump()<<'\n';
        } else if(command=="status") {
            Engine engine; std::cout<<engine.execute({{"op","STATUS"}}).dump(2)<<'\n';
        } else if(command=="run"&&argc==5) {
            Engine engine;
            engine.execute({{"op","ATTACH"},{"payload",{{"directory",argv[4]}}}});
            compile(engine,argv[2]);
            auto job=read_json(argv[3]);
            check(job.is_array(),"Job must be an array of native requests");
            for(const auto& request:job) std::cout<<json({{"op",request.at("op")},{"result",engine.execute(request)}}).dump()<<'\n';
        } else if(command=="validate"&&argc==3) std::cout<<validate(argv[2]).dump(2)<<'\n';
        else if(command=="bench"&&(argc==3||argc==5))
            std::cout<<bench(argv[2],argc==5?std::stoull(argv[3]):65536,argc==5?std::stoull(argv[4]):64).dump(2)<<'\n';
        else throw std::invalid_argument("Unknown command or argument count");
        return 0;
    } catch(const std::exception& e) { std::cerr<<json({{"ok",false},{"error",e.what()}}).dump()<<'\n'; return 1; }
}
