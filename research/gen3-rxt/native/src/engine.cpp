#include "memory_headroom.hpp"
#include "engine.hpp"
#include "atom3d.hpp"
#include "starbreaker.hpp"
#include "knowledge.hpp"
#include "joint_binding.hpp"
#include "training.hpp"
#include "rh.hpp"
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/rand.h>
#include <omp.h>
#include <sched.h>
#include <sys/file.h>
#include <fcntl.h>
#include <unistd.h>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>

namespace rxt {
using Clock = std::chrono::steady_clock;
namespace fs = std::filesystem;
static void require(bool b, const std::string& s) { if(!b) throw std::invalid_argument(s); }
static bool integer(const json& x) { return x.is_number_integer() || x.is_number_unsigned(); }
static size_t product(size_t a, size_t b) {
    if(b && a>std::numeric_limits<size_t>::max()/b) throw std::overflow_error("Allocation size overflow");
    return a*b;
}
static std::string read_text(const fs::path& path) {
    std::ifstream in(path); if(!in) throw std::runtime_error("Cannot read "+path.string());
    return {std::istreambuf_iterator<char>(in),std::istreambuf_iterator<char>()};
}
json read_json(const fs::path& path) { return json::parse(read_text(path)); }
std::string hash(const std::string& bytes) {
    unsigned char out[EVP_MAX_MD_SIZE]; unsigned n=0;
    if(!EVP_Digest(bytes.data(),bytes.size(),out,&n,EVP_sha256(),nullptr)) throw std::runtime_error("SHA256 failed");
    std::ostringstream s; s<<std::hex<<std::setfill('0');
    for(unsigned i=0;i<n;++i) s<<std::setw(2)<<unsigned(out[i]);
    return s.str();
}
mpq_class rational(const json& x) {
    require(integer(x)||x.is_string(),"Exact operands must be integers or rational strings");
    std::string s=x.is_string()?x.get<std::string>():x.dump();
    require(!s.empty() && s.find_first_not_of("0123456789-/")==std::string::npos,"Malformed exact rational");
    require(std::count(s.begin(),s.end(),'/')<=1,"Malformed rational denominator");
    auto slash=s.find('/');
    if(slash!=std::string::npos) {
        std::string den=s.substr(slash+1); require(!den.empty(),"Missing denominator");
        mpz_class d(den); require(d!=0,"Zero denominator");
    }
    mpq_class q;
    require(mpq_set_str(q.get_mpq_t(),s.c_str(),10)==0,"Malformed rational");
    q.canonicalize(); return q;
}
json number(const mpq_class& x) {
    mpq_class reduced=x; reduced.canonicalize();
    if(reduced.get_den()==1 && reduced.get_num().fits_slong_p()) return reduced.get_num().get_si();
    return reduced.get_str();
}
json log_value(const mpq_class& x) {
    require(x>0,"Logarithm needs a positive source ratio");
    return {{"type","EXACT_LOG_POSITIVE_RATIONAL"},{"argument",number(x)},{"sign",(x>1)-(x<1)}};
}
static uint64_t current_host_headroom(uint64_t limit,uint64_t& current,uint64_t& reclaimable){
    try {current=std::stoull(read_text("/sys/fs/cgroup/memory.current"));} catch(...) {}
    reclaimable=0;
    try {std::istringstream input(read_text("/sys/fs/cgroup/memory.stat"));std::map<std::string,uint64_t> values;std::string key;uint64_t bytes;
        while(input>>key>>bytes)values[key]=bytes;
        reclaimable=clean_inactive_cache(current,values["inactive_file"],values["file"],values["file_dirty"],values["file_writeback"],values["file_mapped"],values["shmem"]);
    } catch(...) {}
    uint64_t host_available=limit;
    try {std::istringstream input(read_text("/proc/meminfo"));std::string line;
        while(std::getline(input,line)){std::istringstream row(line);std::string key;uint64_t kib;if(row>>key>>kib&&key=="MemAvailable:"){host_available=kib*1024;break;}}
    } catch(...) {}
    return bounded_host_headroom(limit,current,reclaimable,host_available);
}
Resources Resources::detect() {
    Resources r; cpu_set_t set; CPU_ZERO(&set);
    r.cpu_quota=(sched_getaffinity(0,sizeof(set),&set)==0)?CPU_COUNT(&set):1;
    std::ifstream cpu("/sys/fs/cgroup/cpu.max"); std::string quota; uint64_t period=0;
    if(cpu>>quota>>period && quota!="max" && period) r.cpu_quota=std::min(r.cpu_quota,std::stod(quota)/double(period));
    r.cpu_threads=std::max(1u,unsigned(r.cpu_quota));
    r.host_limit=180ull*1024*1024*1024;
    try { auto s=read_text("/sys/fs/cgroup/memory.max"); if(s.find("max")==std::string::npos) r.host_limit=std::min(r.host_limit,uint64_t(std::stoull(s))); } catch(...) {}
    r.host_budget=current_host_headroom(r.host_limit,r.host_current,r.host_reclaimable)*95/100;
    auto g=CudaBackend::info(); r.gpu_budget=g.free_bytes*95/100;
    return r;
}
json Resources::describe() const {
    return {{"cpu_quota",cpu_quota},{"cpu_workers",cpu_threads},{"host_limit_bytes",host_limit},
            {"host_current_at_start_bytes",host_current},{"clean_inactive_cache_at_start_bytes",host_reclaimable},{"host_work_budget_bytes",host_budget},
            {"gpu_work_budget_bytes",gpu_budget},{"allocation","DEMAND_DRIVEN"}};
}
void Resources::admit(uint64_t host, uint64_t device) const {
    uint64_t current=host_current,reclaimable=0;const auto available=current_host_headroom(host_limit,current,reclaimable);
    require(host<=host_budget && host<=available*95/100,
            "Host memory admission exceeded; submit a smaller batch");
    if(device) {
        auto g=CudaBackend::info();
        require(device<=gpu_budget && device<=g.free_bytes*95/100,"GPU memory admission exceeded; submit a smaller batch");
    }
}
static int phase_cpu(uint32_t a,int c) { return int((a>>c)&1u)+2*int((a>>(c+9))&1u); }
static uint32_t write_cpu(uint32_t a, Event e) {
    int phase=(phase_cpu(a,e.coordinate)+e.direction+4)%4;
    a &= ~((1u<<e.coordinate)|(1u<<(e.coordinate+9)));
    return a | (uint32_t(phase&1)<<e.coordinate) | (uint32_t(phase>>1)<<(e.coordinate+9));
}
static int component_cpu(int p,int side) {
    static const int v[4][2]={{1,0},{0,1},{-1,0},{0,-1}}; return v[p][side];
}
Contract::Contract(const json& raw, const Resources& resources):source(raw) {
    require(raw.is_object(),"Source contract must be an object");
    const std::set<std::string> allowed={"schema","name","coordinates","events","receivers","states",
        "contact_coordinates","source_binding","units","motion_profile"};
    for(auto it=raw.begin();it!=raw.end();++it) require(allowed.count(it.key()),"Unknown source field: "+it.key());
    require(raw.value("schema","")=="SLC_GEN2_SOURCE_V1","Unsupported source contract schema");
    require(!raw.contains("motion_profile")||raw["motion_profile"].is_null(),"Motion source lowering is not implemented in this core");
    require(raw.contains("source_binding")&&!raw["source_binding"].is_null(),"Source binding required");
    require(raw.contains("coordinates")&&raw["coordinates"].is_array(),"Coordinates required");
    std::set<int> seen;
    for(const auto& c:raw["coordinates"]) {
        require(integer(c)&&c>=0&&c<9,"Coordinate must be in 0..8");
        int value=c.get<int>(); require(seen.insert(value).second,"Duplicate coordinate"); coordinates.push_back(value);
    }
    require(!coordinates.empty(),"Empty coordinate domain");
    tables.index.assign(ADDRESS_COUNT,-1);
    auto pack=[&](const json& q) {
        require(q.is_array()&&q.size()==coordinates.size(),"State width differs from source");
        uint32_t address=0;
        for(size_t i=0;i<q.size();++i) {
            require(integer(q[i])&&q[i]>=0&&q[i]<4,"State phase must be in 0..3");
            unsigned phase=q[i].get<unsigned>(); int c=coordinates[i];
            address|=((phase&1)<<c)|((phase>>1)<<(c+9));
        }
        return address;
    };
    if(raw.contains("states")&&!raw["states"].is_null()) {
        require(raw["states"].is_array()&&!raw["states"].empty(),"Empty explicit domain");
        json states=raw["states"]; std::sort(states.begin(),states.end()); source["states"]=states;
        for(const auto& q:states) tables.addresses.push_back(pack(q));
    } else {
        size_t n=size_t(1)<<(2*coordinates.size());
        for(size_t i=0;i<n;++i) {
            json q=json::array();
            for(size_t c=0;c<coordinates.size();++c) q.push_back((i>>(2*(coordinates.size()-c-1)))&3);
            tables.addresses.push_back(pack(q));
        }
    }
    for(size_t i=0;i<tables.addresses.size();++i) {
        auto& idx=tables.index[tables.addresses[i]];
        require(idx<0,"Duplicate source state"); idx=int32_t(i);
    }
    require(raw.contains("events")&&raw["events"].is_array()&&!raw["events"].empty(),"Source events required");
    json events=raw["events"];
    require(events.size()<=65535,"Too many event labels for R1 IR");
    std::sort(events.begin(),events.end(),[](const json& a,const json& b){return a.at("label")<b.at("label");});
    source["events"]=events;
    std::set<std::string> names;
    for(const auto& e:events) {
        for(auto it=e.begin();it!=e.end();++it) require(it.key()=="label"||it.key()=="coordinate"||it.key()=="direction"||it.key()=="admitted_states","Unknown event field");
        require(e.at("label").is_string()&&!e["label"].get<std::string>().empty(),"Event label required");
        std::string label=e["label"];
        require(names.insert(label).second,"Duplicate event label");
        require(integer(e.at("coordinate"))&&seen.count(e["coordinate"].get<int>()),"Event coordinate outside source");
        require(integer(e.at("direction"))&&(e["direction"]==1||e["direction"]==-1),"Event direction must be +1 or -1");
        labels.push_back(label); tables.events.push_back({e["coordinate"],e["direction"]});
    }
    const size_t n=tables.addresses.size();
    resources.admit(product(n,events.size())+product(n,64));
    tables.admitted.assign(product(n,events.size()),0);
    for(size_t ev=0;ev<events.size();++ev) {
        const auto& e=events[ev];
        if(!e.contains("admitted_states")||e["admitted_states"].is_null()) {
            std::fill_n(tables.admitted.begin()+ev*n,n,1);
        } else {
            require(e["admitted_states"].is_array(),"Event state admission must be an array");
            for(const auto& q:e["admitted_states"]) {
                uint32_t a=pack(q); require(tables.index[a]>=0,"Admitted event state outside domain");
                tables.admitted[ev*n+tables.index[a]]=1;
            }
        }
        for(size_t i=0;i<n;++i) if(tables.admitted[ev*n+i])
            require(tables.index[write_cpu(tables.addresses[i],tables.events[ev])]>=0,"Admitted Write leaves source domain");
    }
    require(raw.contains("receivers")&&raw["receivers"].is_array()&&!raw["receivers"].empty(),"Receivers required");
    std::set<std::string> receiver_names;
    std::vector<std::vector<int64_t>> weights;
    for(const auto& receiver:raw["receivers"]) {
        require(receiver.size()==3&&receiver.contains("name")&&receiver.contains("coordinates")&&receiver.contains("matrix"),"Receiver requires name, coordinates, matrix");
        require(receiver["name"].is_string()&&receiver_names.insert(receiver["name"].get<std::string>()).second,"Duplicate receiver name");
        std::vector<int> coords; std::set<int> used;
        for(const auto& c:receiver["coordinates"]) {
            require(integer(c)&&seen.count(c.get<int>())&&used.insert(c.get<int>()).second,"Invalid receiver coordinate"); coords.push_back(c.get<int>());
        }
        require(!coords.empty()&&receiver["matrix"].is_array()&&!receiver["matrix"].empty(),"Receiver matrix required");
        for(const auto& row:receiver["matrix"]) {
            require(row.is_array()&&row.size()==2*coords.size(),"Receiver row width differs");
            std::vector<mpq_class> values; mpz_class denominator=1;
            for(const auto& value:row) { auto v=rational(value); mpz_lcm(denominator.get_mpz_t(),denominator.get_mpz_t(),v.get_den().get_mpz_t()); values.push_back(v); }
            std::vector<int64_t> weight(18,0); mpz_class bound=0;
            for(size_t j=0;j<values.size();++j) {
                mpz_class numerator=values[j].get_num()*(denominator/values[j].get_den());
                require(numerator.fits_slong_p(),"Receiver exceeds R1 int64 lane; arbitrary-width receiver lowering pending");
                bound+=abs(numerator); weight[(j/coords.size())*9+coords[j%coords.size()]]=numerator.get_si();
            }
            require(bound<=mpz_class(std::numeric_limits<long>::max()/4),"Receiver lane bound exceeds exact int64 admission");
            denominators.push_back(denominator); weights.push_back(std::move(weight));
        }
    }
    size_t half=weights.size(); tables.channels=2*half;
    resources.admit(product(product(n,tables.channels),sizeof(int64_t))+product(n,events.size())+4*ADDRESS_COUNT);
    for(const auto& w:weights) tables.weights.insert(tables.weights.end(),w.begin(),w.end());
    for(size_t c=0;c<half;++c) denominators.push_back(denominators[c]);
    tables.frames.resize(product(n,tables.channels)); tables.contacts.resize(n,0);
    if(raw.contains("contact_coordinates")&&!raw["contact_coordinates"].is_null()) {
        const auto& cc=raw["contact_coordinates"]; require(cc.is_array()&&cc.size()==3,"Contact requires three coordinates");
        for(int j=0;j<3;++j) { require(integer(cc[j])&&seen.count(cc[j].get<int>()),"Contact outside source"); tables.contact_coordinates[j]=cc[j]; }
        has_contact=true;
    }
    #pragma omp parallel for num_threads(resources.cpu_threads) schedule(static)
    for(size_t i=0;i<n;++i) {
        uint32_t a=tables.addresses[i];
        for(size_t c=0;c<half;++c) {
            int64_t signed_value=0,occupancy=0;
            for(int k=0;k<18;++k) {
                int h=component_cpu(phase_cpu(a,k%9),k/9);
                signed_value+=weights[c][k]*h; occupancy+=weights[c][k]*std::abs(h);
            }
            tables.frames[c*n+i]=signed_value; tables.frames[(half+c)*n+i]=occupancy;
        }
        if(has_contact) {
            int q[3]; for(int j=0;j<3;++j) q[j]=phase_cpu(a,tables.contact_coordinates[j]);
            int dot02=0,dot12=0;
            for(int side=0;side<2;++side) { dot02+=component_cpu(q[0],side)*component_cpu(q[2],side); dot12+=component_cpu(q[1],side)*component_cpu(q[2],side); }
            tables.contacts[i]=6-2*dot02+2*dot12;
        }
    }
    id=hash(source.dump());
}
uint32_t Contract::encode(const json& q) const {
    require(q.is_array()&&q.size()==coordinates.size(),"Initial state width differs"); uint32_t a=0;
    for(size_t i=0;i<q.size();++i) {
        require(integer(q[i])&&q[i]>=0&&q[i]<4,"Initial phase outside 0..3");
        unsigned p=q[i].get<unsigned>(); a|=((p&1)<<coordinates[i])|((p>>1)<<(coordinates[i]+9));
    }
    require(tables.index[a]>=0,"State outside admitted source domain"); return a;
}
json Contract::decode(uint32_t a) const {
    json q=json::array(); for(int c:coordinates) q.push_back(phase_cpu(a,c)); return q;
}
json Contract::frame(uint32_t a,const std::string& view) const {
    require(a<ADDRESS_COUNT&&tables.index[a]>=0,"Frame outside source domain");
    require(view=="JOINT"||view=="SIGNED"||view=="OCCUPANCY","Unsupported observation view");
    size_t n=tables.addresses.size(),half=tables.channels/2,begin=view=="OCCUPANCY"?half:0,end=view=="SIGNED"?half:tables.channels;
    json out=json::array();
    for(size_t c=begin;c<end;++c) out.push_back(number(mpq_class(mpz_class(long(tables.frames[c*n+tables.index[a]])),denominators[c])));
    return out;
}
Batch Contract::batch(const json& payload) const {
    require(payload.contains("initial")&&payload["initial"].is_array()&&!payload["initial"].empty(),"Initial state batch required");
    require(payload.contains("programs")&&payload["programs"].is_array(),"One program per initial state required");
    Batch b; b.count=payload["initial"].size();
    require(payload["programs"].size()==b.count,"Program batch width differs");
    b.steps=payload["programs"][0].size(); b.events.resize(product(b.count,b.steps));
    for(size_t lane=0;lane<b.count;++lane) {
        b.initial.push_back(encode(payload["initial"][lane]));
        const auto& p=payload["programs"][lane];
        require(p.is_array()&&p.size()==b.steps,"R1 batches require equal lengths; group programs by length");
        for(size_t step=0;step<b.steps;++step) {
            require(p[step].is_string(),"Event label must be a string");
            auto it=std::find(labels.begin(),labels.end(),p[step].get<std::string>());
            require(it!=labels.end(),"Unknown source event"); b.events[step*b.count+lane]=uint16_t(it-labels.begin());
        }
    }
    return b;
}
json Contract::describe() const {
    return {{"contract_id",id},{"source",source},{"states",tables.addresses.size()},
            {"events",labels},{"channels",tables.channels},{"receiver_arithmetic","SCALED_EXACT_INT64"}};
}
Trace run_cpu(const Tables& t,const Batch& b,unsigned threads) {
    auto start=Clock::now(); Trace out; out.count=b.count; out.steps=b.steps; out.backend="EPYC_OPENMP";
    out.states.resize(product(b.count,b.steps+1)); out.actions.resize(out.states.size());
    std::atomic<size_t> error{std::numeric_limits<size_t>::max()}; size_t n=t.addresses.size();
    unsigned workers=b.count*b.steps<16384?1:std::min(threads,std::max(1u,unsigned(b.count/512)));
    out.cpu_workers=workers;
    #pragma omp parallel for num_threads(workers) schedule(static)
    for(size_t lane=0;lane<b.count;++lane) {
        uint32_t q=b.initial[lane]; int32_t qi=t.index[q]; out.states[lane]=q; out.actions[lane]=t.contacts[qi];
        for(size_t step=0;step<b.steps;++step) {
            size_t ev=b.events[step*b.count+lane];
            if(!t.admitted[ev*n+qi]) { error.store(lane); break; }
            q=write_cpu(q,t.events[ev]); qi=t.index[q]; size_t at=(step+1)*b.count+lane;
            out.states[at]=q; out.actions[at]=t.contacts[qi];
        }
    }
    require(error.load()==std::numeric_limits<size_t>::max(),"Event not admitted in CPU batch");
    out.wall_seconds=std::chrono::duration<double>(Clock::now()-start).count(); out.kernel_seconds=out.wall_seconds; return out;
}

json log_account(const json& source) {
    require(source.contains("quantity")&&source["quantity"].is_object()&&source.contains("source_binding"),"Log account requires typed quantity and source binding");
    for(const char* key:{"kind","units","scope"}) require(source["quantity"].contains(key),std::string("Quantity requires ")+key);
    const auto& points=source.at("points"); const auto& edges=source.at("edges");
    require(points.is_array()&&!points.empty()&&edges.is_array()&&edges.size()+1==points.size(),"Log account needs every ordered point and connecting event");
    std::set<std::string> pids,eids;
    json segments=json::array(),gaps=json::array(),segment,ties;
    mpq_class initial=1,previous=1,up=1,down=1,maximum=1;
    bool active=false; size_t count=0;
    auto finish=[&]() {
        if(!active) return;
        mpq_class net=previous/initial;
        require(up/down==net,"Exact log identity failed");
        segment["initial_action"]=number(initial); segment["final_action"]=number(previous);
        segment["U"]=log_value(up); segment["D"]=log_value(down);
        segment["V"]=log_value(mpq_class(up*down)); segment["L"]=log_value(net); segment["net"]=log_value(net);
        segment["M"]=log_value(maximum); segment["maximizing_points"]=ties; segment["edge_count"]=count;
        segments.push_back(segment); active=false;
    };
    for(size_t i=0;i<points.size();++i) {
        const auto& p=points[i];
        require(p.is_object()&&p.contains("id")&&p["id"].is_string()&&!p["id"].get<std::string>().empty()&&p.contains("state"),"Point needs occurrence id and complete source state");
        std::string pid=p["id"];
        require(pids.insert(pid).second,"Repeated point occurrence");
        if(i) {
            const auto& e=edges[i-1]; require(e.is_object()&&e.contains("id")&&e["id"].is_string()&&e.contains("event"),"Edge needs occurrence id and source event");
            require(e.at("before")==points[i-1]["id"]&&e.at("after")==p["id"],"Log edge is not adjacent to source points");
            require(eids.insert(e["id"].get<std::string>()).second,"Repeated edge occurrence");
        }
        std::string status=p.value("status","OBSERVED");
        require(status=="OBSERVED"||status=="MISSING"||status=="UNAVAILABLE","Unknown source point availability");
        bool observed=status=="OBSERVED"&&p.contains("action")&&!p["action"].is_null();
        mpq_class action=observed?rational(p["action"]):mpq_class(0);
        if(!observed||action<=0) { finish(); gaps.push_back(pid); continue; }
        if(!active) {
            active=true; initial=previous=action; up=down=maximum=1; count=0;
            segment={{"first_point",pid},{"last_point",pid}}; ties=json::array({pid});
        } else {
            mpq_class delta=action/previous;
            if(delta>1) up*=delta; else if(delta<1) down/=delta;
            mpq_class net=action/initial;
            if(net>maximum) { maximum=net; ties=json::array({pid}); }
            else if(net==maximum) ties.push_back(pid);
            previous=action; ++count; segment["last_point"]=pid;
        }
    }
    finish(); bool defined=gaps.empty()&&segments.size()==1;
    json summary;
    if(defined) summary=segments[0];
    else summary={{"U",nullptr},{"D",nullptr},{"V",nullptr},{"L",nullptr},{"net",nullptr},{"M",nullptr},
                  {"unavailable_points",gaps},{"segments",segments}};
    return {{"schema","GEN_RXT_LOG_READOUT_V1"},{"status",defined?"DEFINED":"UNDEFINED_GAPS"},
            {"quantity",source["quantity"]},{"source_binding",source["source_binding"]},
            {"point_count",points.size()},{"edge_count",edges.size()},{"summary",summary},
            {"normalization",{{"kind","ORIGINAL_POSITIVE_SOURCE_RATIO"},{"reference_point",points[0]["id"]}}},
            {"full_history_retained",true}};
}
json Contract::describe_trace(const Batch& b,const Trace& trace,size_t lane) const {
    json states=json::array(),observations=json::array(),actions=json::array(),program=json::array(),directions=json::array();
    json points=json::array(),edges=json::array(); int maximum=std::numeric_limits<int>::min();
    for(size_t step=0;step<=b.steps;++step) {
        size_t at=step*b.count+lane; auto state=decode(trace.states[at]); states.push_back(state);
        observations.push_back(frame(trace.states[at]));
        json action=has_contact?json(trace.actions[at]):json(nullptr); actions.push_back(action);
        maximum=std::max(maximum,trace.actions[at]);
        std::string pid="p"+std::to_string(step);
        points.push_back({{"id",pid},{"state",state},{"action",action}});
        if(step) {
            size_t ev=b.events[(step-1)*b.count+lane]; program.push_back(labels[ev]); directions.push_back(tables.events[ev].direction);
            edges.push_back({{"id","e"+std::to_string(step-1)},{"before","p"+std::to_string(step-1)},
                {"after",pid},{"event",{{"label",labels[ev]},{"direction",tables.events[ev].direction}}}});
        }
    }
    json account={{"quantity",{{"kind","SOURCE_ACTION"},{"units",{{"native_source_action",1}}},{"scope","HISTORY"},{"source",id}}},
                  {"source_binding",id},{"points",points},{"edges",edges}};
    return {{"contract_id",id},{"initial",states[0]},{"program",program},{"states",states},{"observations",observations},
            {"directions",directions},{"contact_profile",actions},{"barrier",has_contact?json(maximum-trace.actions[lane]):json(nullptr)},
            {"view","JOINT"},{"log",log_account(account)},{"history",account}};
}

static void sync_dir(const fs::path& path) {
    int fd=open(path.c_str(),O_RDONLY|O_DIRECTORY); if(fd<0) throw std::runtime_error("Cannot open checkpoint directory");
    int rc=fsync(fd); close(fd); if(rc<0) throw std::runtime_error("Checkpoint directory fsync failed");
}
static void atomic_write(const fs::path& path,const std::string& bytes,mode_t mode=0600) {
    std::string temp=path.string()+".tmp."+std::to_string(getpid());
    int fd=open(temp.c_str(),O_WRONLY|O_CREAT|O_EXCL,mode);
    if(fd<0) throw std::runtime_error("Cannot create checkpoint object: "+temp);
    try {
        size_t offset=0;
        while(offset<bytes.size()) { ssize_t n=write(fd,bytes.data()+offset,bytes.size()-offset); if(n<=0) throw std::runtime_error("Checkpoint write failed"); offset+=size_t(n); }
        if(fsync(fd)<0) throw std::runtime_error("Checkpoint fsync failed");
        close(fd); fd=-1;
        if(rename(temp.c_str(),path.c_str())<0) throw std::runtime_error("Checkpoint rename failed");
        sync_dir(path.parent_path());
    } catch(...) { if(fd>=0) close(fd); unlink(temp.c_str()); throw; }
}
static std::string mac(const std::string& key,const std::string& bytes) {
    unsigned char out[EVP_MAX_MD_SIZE]; unsigned n=0;
    require(HMAC(EVP_sha256(),key.data(),int(key.size()),reinterpret_cast<const unsigned char*>(bytes.data()),bytes.size(),out,&n)!=nullptr,"Root authentication failed");
    std::ostringstream s; s<<std::hex<<std::setfill('0'); for(unsigned i=0;i<n;++i) s<<std::setw(2)<<unsigned(out[i]); return s.str();
}
Store::Store(const fs::path& root):root_(fs::absolute(root)) {
    fs::create_directories(root_/"objects"); lock_fd_=open((root_/"LOCK").c_str(),O_RDWR|O_CREAT,0600);
    if(lock_fd_<0||flock(lock_fd_,LOCK_EX|LOCK_NB)<0) { if(lock_fd_>=0) close(lock_fd_); lock_fd_=-1; throw std::runtime_error("Checkpoint store already in use"); }
    try {
        if(!fs::exists(root_/"KEY")) {
            require(!fs::exists(root_/"HEAD.json"),"Checkpoint key is missing");
            unsigned char key[32]; require(RAND_bytes(key,sizeof(key))==1,"Cannot create custody key");
            atomic_write(root_/"KEY",std::string(reinterpret_cast<char*>(key),sizeof(key)));
        }
    } catch(...) { close(lock_fd_); lock_fd_=-1; throw; }
}
Store::~Store() { if(lock_fd_>=0) { flock(lock_fd_,LOCK_UN); close(lock_fd_); } }
std::string Store::remember(const std::string& key,const json& value) {
    auto previous=recall(key);
    require(previous.is_null()||previous==value,"Immutable native memory key has a different value");
    std::string id=put(value),name=hash(key);
    fs::create_directories(root_/"memory"/name.substr(0,2));
    auto path=root_/"memory"/name.substr(0,2)/(name+".json");
    if(!fs::exists(path)) atomic_write(path,json({{"key",key},{"object",id},{"mac",mac(read_text(root_/"KEY"),key+":"+id)}}).dump());
    return id;
}
json Store::recall(const std::string& key) const {
    auto name=hash(key);auto path=root_/"memory"/name.substr(0,2)/(name+".json");
    if(!fs::exists(path)) return nullptr;
    auto ref=read_json(path);std::string id=ref.at("object"),signature=ref.at("mac"),expected=mac(read_text(root_/"KEY"),key+":"+id);
    require(ref.at("key")==key&&signature.size()==expected.size()&&CRYPTO_memcmp(signature.data(),expected.data(),expected.size())==0,"Native memory index authentication differs");
    return get(id);
}
std::string Store::put(const json& object) {
    std::string bytes=object.dump(),id=hash(bytes); auto path=root_/"objects"/(id+".json");
    if(!fs::exists(path)) atomic_write(path,bytes);
    else require(hash(read_text(path))==id,"Existing checkpoint object is corrupt");
    return id;
}
json Store::get(const std::string& id) const {
    require(id.size()==64&&id.find_first_not_of("0123456789abcdef")==std::string::npos,"Malformed object digest");
    std::string bytes=read_text(root_/"objects"/(id+".json")); require(hash(bytes)==id,"Checkpoint object digest differs"); return json::parse(bytes);
}
std::string Store::commit(const json& state) {
    for(const auto& run:state.at("runs"))if(run.is_string()){auto id=run.get<std::string>();if(!validated_runs_.contains(id)){get(id);validated_runs_.insert(id);}}
    std::string id=put(state),key=read_text(root_/"KEY");
    json head={{"schema","GEN_RXT_ROOT_V1"},{"root",id},{"mac",mac(key,id)}};
    atomic_write(root_/"HEAD.json",head.dump()); return id;
}
json Store::restore() const {
    if(!fs::exists(root_/"HEAD.json")) return nullptr;
    auto head=read_json(root_/"HEAD.json"); require(head.at("schema")=="GEN_RXT_ROOT_V1","Checkpoint root schema differs");
    std::string id=head.at("root"),signature=head.at("mac"),expected=mac(read_text(root_/"KEY"),id);
    require(signature.size()==expected.size()&&CRYPTO_memcmp(signature.data(),expected.data(),expected.size())==0,"Checkpoint root authentication differs");
    auto state=get(id); require((state.at("version")==VERSION||state.at("version")=="GEN3-RXT-R2"||state.at("version")=="GEN3-RXT-R3"||state.at("version")=="GEN3-RXT-R4"||state.at("version")=="GEN3-RXT-R5"||state.at("version")=="GEN3-RXT-R6"||state.at("version")=="GEN3-RXT-R7")&&state.at("schema")=="GEN_RXT_MACHINE_V1","Checkpoint engine version differs");
    for(const auto& run:state.at("runs"))if(run.is_string()){auto id=run.get<std::string>();if(!validated_runs_.contains(id)){get(id);validated_runs_.insert(id);}}
    return state;
}

Engine::Engine():resources_(Resources::detect()) {}
Engine::~Engine()=default;
const Contract& Engine::contract() const { require(bool(contract_),"Compile a source first"); return *contract_; }
Trace Engine::run(const Batch& b,const std::string& backend) {
    const auto& c=contract(); require(b.count>0&&b.initial.size()==b.count&&b.events.size()==product(b.count,b.steps),"Invalid batch IR");
    for(auto a:b.initial) require(a<ADDRESS_COUNT&&c.tables.index[a]>=0,"Invalid initial state in IR");
    for(auto e:b.events) require(e<c.tables.events.size(),"Invalid event in IR");
    size_t points=product(b.count,b.steps+1);
    size_t bytes=product(points,8)+product(b.events.size(),2)+product(b.count,4);
    std::string selected=backend;
    if(selected=="auto") selected=b.count>=4096?"cuda":"cpu";
    require(selected=="cpu"||selected=="cuda","Backend must be cpu, cuda or auto");
    resources_.admit(bytes,selected=="cuda"?bytes:0);
    if(selected=="cpu") return run_cpu(c.tables,b,resources_.cpu_threads);
    if(!gpu_) {
        size_t table_bytes=c.tables.frames.size()*8+c.tables.weights.size()*8+c.tables.admitted.size()+c.tables.addresses.size()*8+ADDRESS_COUNT*4;
        resources_.admit(bytes,bytes+table_bytes);
        gpu_=std::make_unique<CudaBackend>(c.tables);
    }
    return gpu_->run(b);
}
json Engine::checkpoint() {
    require(bool(store_),"Attach a durable store first"); std::string root=store_->commit(state_);
    return {{"root",root},{"sequence",state_["sequence"]},{"status","COMMITTED"}};
}
json Engine::inverse(const json& payload) {
    const auto& c=contract(); const auto& observations=payload.at("observations");
    require(observations.is_array()&&!observations.empty(),"Inverse requires an observation sequence");
    std::string view=payload.value("view","JOINT");
    size_t width=view=="JOINT"?c.tables.channels:c.tables.channels/2;
    require(view=="JOINT"||view=="SIGNED"||view=="OCCUPANCY","Unknown inverse view");
    std::vector<std::vector<mpq_class>> actual(observations.size());
    for(size_t i=0;i<observations.size();++i) if(!observations[i].is_null()) {
        require(observations[i].is_array()&&observations[i].size()==width,"Observation width differs from source channel");
        for(const auto& v:observations[i]) actual[i].push_back(rational(v));
    }
    json directions=payload.value("directions",json::array());
    if(directions.empty()) directions=json::array();
    require(directions.empty()||directions.size()+1==observations.size(),"One direction per observation edge required");
    for(const auto& d:directions) require(d.is_null()||(integer(d)&&(d==1||d==-1)),"Invalid inverse direction");
    std::vector<uint32_t> roots;
    if(payload.contains("initial_states")&&!payload["initial_states"].is_null()) {
        std::set<uint32_t> seen;
        for(const auto& q:payload["initial_states"]) if(seen.insert(c.encode(q)).second) roots.push_back(c.encode(q));
    } else roots=c.tables.addresses;
    auto matches=[&](uint32_t q,size_t step) {
        if(observations[step].is_null()) return true;
        auto f=c.frame(q,view);
        for(size_t k=0;k<f.size();++k) if(rational(f[k])!=actual[step][k]) return false;
        return true;
    };
    // Each node keeps root/current/barrier; every parent event is retained.
    struct Node { size_t time; uint32_t root,q; int barrier; mpz_class paths; };
    std::vector<Node> nodes; std::vector<size_t> frontier; json edges=json::array();
    for(auto q:roots) if(matches(q,0)) { frontier.push_back(nodes.size()); nodes.push_back({0,q,q,0,mpz_class(1)}); }
    size_t limit=payload.value("max_nodes",size_t(1000000));
    require(limit>0&&limit<=10000000,"max_nodes must be in 1..10000000");
    resources_.admit(product(limit,256)); require(nodes.size()<=limit,"Inverse root set exceeds node budget");
    size_t domain=c.tables.addresses.size();
    for(size_t step=1;step<observations.size();++step) {
        std::map<std::tuple<uint32_t,uint32_t,int>,size_t> layer;
        std::vector<size_t> next;
        for(size_t parent:frontier) {
            Node prior=nodes[parent]; size_t qi=c.tables.index[prior.q];
            for(size_t ev=0;ev<c.tables.events.size();++ev) {
                auto event=c.tables.events[ev];
                if(!directions.empty()&&!directions[step-1].is_null()&&directions[step-1]!=event.direction) continue;
                if(!c.tables.admitted[ev*domain+qi]) continue;
                uint32_t target=write_cpu(prior.q,event); if(!matches(target,step)) continue;
                int barrier=c.has_contact?std::max(prior.barrier,c.tables.contacts[c.tables.index[target]]-c.tables.contacts[c.tables.index[prior.root]]):0;
                auto key=std::make_tuple(prior.root,target,barrier); auto it=layer.find(key); size_t child;
                if(it==layer.end()) {
                    require(nodes.size()<limit,"Inverse node budget exhausted; no partial answer committed");
                    child=nodes.size(); layer[key]=child; next.push_back(child); nodes.push_back({step,prior.root,target,barrier,mpz_class(0)});
                } else child=it->second;
                nodes[child].paths+=prior.paths;
                require(edges.size()<limit*32,"Inverse edge budget exhausted; no partial answer committed");
                edges.push_back({{"from",parent},{"to",child},{"event",c.labels[ev]}});
            }
        }
        frontier=std::move(next);
    }
    json node_rows=json::array(); mpz_class histories=0;
    for(const auto& node:nodes) node_rows.push_back({{"time",node.time},{"root",c.decode(node.root)},{"state",c.decode(node.q)},
        {"barrier",c.has_contact?json(node.barrier):json(nullptr)},{"path_count",node.paths.get_str()}});
    for(size_t i:frontier) histories+=nodes[i].paths;
    return {{"schema","GEN_RXT_INVERSE_DAG_V1"},{"contract_id",c.id},{"view",view},{"observations",observations},
            {"nodes",node_rows},{"edges",edges},{"frontier",frontier},{"history_count",histories.get_str()},
            {"complete",true},{"all_parent_events_retained",true}};
}
json Engine::execute(const json& request) {
    require(request.is_object()&&request.contains("op")&&request["op"].is_string(),"Request requires op");
    std::string op=request["op"]; json p=request.value("payload",json::object()); require(p.is_object(),"Payload must be an object");
    if(op=="STATUS") {
        auto g=CudaBackend::info();
        return {{"version",VERSION},{"implementation","INDEPENDENT_CPP_CUDA"},{"resources",resources_.describe()},
            {"gpu",{{"name",g.name},{"compute_capability",std::to_string(g.major)+"."+std::to_string(g.minor)},
                    {"sms",g.sms},{"free_bytes",g.free_bytes},{"total_bytes",g.total_bytes}}},
            {"sequence",state_["sequence"]},{"learned_relations",state_["knowledge"].size()},
            {"contract_id",contract_?json(contract_->id):json(nullptr)},{"store_attached",bool(store_)},
            {"atom3d",atom3d_?atom3d_->status():json(nullptr)},{"starbreaker",starbreaker_?starbreaker_->status():json(nullptr)}};
    }
    if(op=="COMPILE") {
        auto next=std::make_unique<Contract>(p.at("source"),resources_);
        json next_state=state_; next_state["source"]=next->source;
        // A new source cannot inherit the preceding source's continuation state.
        if(!contract_||contract_->id!=next->id) next_state.erase("last");
        if(store_) store_->commit(next_state);
        contract_=std::move(next); gpu_.reset(); state_=std::move(next_state); return contract_->describe();
    }
    if(op=="ATTACH") {
        require(!store_,"Store already attached"); require(state_["sequence"]==0&&state_["accounts"].empty(),"Attach before executing work");
        auto next=std::make_unique<Store>(p.at("directory").get<std::string>()); auto saved=next->restore();
        if(!saved.is_null()) {
            if(saved.at("version")!=VERSION){saved["migration"]={{"from",saved.at("version")},{"to",VERSION},{"authenticated_predecessor_state",hash(saved.dump())}};saved["version"]=VERSION;}
            std::unique_ptr<Contract> restored;
            std::unique_ptr<Atom3d> domain;
            std::unique_ptr<Starbreaker> starbreaker;
            std::unique_ptr<ConstructionKnowledge> memory;
            if(saved.contains("source")) restored=std::make_unique<Contract>(saved["source"],resources_);
            if(saved.contains("atom3d")) {
                domain=std::make_unique<Atom3d>(saved["atom3d"].at("directory").get<std::string>(),resources_);
                require(domain->binding()==saved["atom3d"],"Saved ATOM3D source binding differs");
            }
            if(saved.contains("starbreaker")) {
                starbreaker=std::make_unique<Starbreaker>(saved["starbreaker"].at("directory").get<std::string>(),resources_);
                require(starbreaker->binding()==saved["starbreaker"],"Saved Starbreaker source binding differs");
                require(next->get(saved.at("sb_policy_object").get<std::string>())==starbreaker->policy(),"Acquired policy checkpoint differs");
                for(auto& entry:saved.at("sb_accounts")){auto account=entry.is_string()?next->get(entry.get<std::string>()):entry;next->get(account.at("history_head").get<std::string>());if(!entry.is_string())entry=next->put(account);}
            }
            if(saved.contains("joint_binding")) {
                const auto& binding=saved.at("joint_binding");
                require(binding.at("bundle_sha256")==JOINT_BUNDLE_SHA&&file_sha256(fs::path(binding.at("directory").get<std::string>())/"BUNDLE.json")==JOINT_BUNDLE_SHA,"Saved joint source differs");
                require(bool(domain)&&bool(starbreaker),"Joint checkpoint requires both domains");
                auto bundle=read_json(fs::path(binding.at("directory").get<std::string>())/"BUNDLE.json");
                auto source=saved.at("construction_memory");
                memory=std::make_unique<ConstructionKnowledge>(source.at("directory").get<std::string>(),bundle["sources"]["learning"].get<std::string>(),resources_);
                require(memory->binding()==source,"Saved construction memory differs");
                if(saved.contains("joint_log_head")) next->get(saved["joint_log_head"].get<std::string>());
                for(const auto& job:saved.at("joint_jobs")) next->get(job.get<std::string>());
            }
            if(saved.contains("core_memory"))for(const auto& ref:saved["core_memory"]["packages"])next->get(ref.get<std::string>());
            if(saved.contains("trained_models"))for(auto it=saved["trained_models"].begin();it!=saved["trained_models"].end();++it){require(bool(starbreaker),"Learned model needs its source domain");starbreaker->adopt(it.key(),next->get(it.value().get<std::string>()));}
            state_=std::move(saved); contract_=std::move(restored); atom3d_=std::move(domain); starbreaker_=std::move(starbreaker); construction_memory_=std::move(memory); gpu_.reset();joint_saved_sets_.clear();joint_predictions_.clear();joint_prediction_object_.clear();
        }
        store_=std::move(next); if(state_.contains("migration"))store_->commit(state_);return {{"status","ATTACHED"},{"sequence",state_["sequence"]}};
    }
    if(op=="CHECKPOINT") return checkpoint();
    if(op.rfind("GEN3_TRANSFER_",0)==0 || op=="ATOM3D_COMMON_MINIMA")return transfer(op,p);
    if(op.rfind("RH_",0)==0)return rh(op,p);
    if(op.rfind("SB_HORIZON_",0)==0)return horizon(op,p);
    if(op.rfind("CAMPAIGN_",0)==0)return campaign(op,p);
    if(op.rfind("GEN3_CORE_",0)==0||op.rfind("GEN3_MEMORY_",0)==0)return core(op,p);
    if(op.rfind("TRAIN_",0)==0)return train(op,p);
    if(op.rfind("JOINT_",0)==0||op=="ATOM3D_KNOWLEDGE"||op=="ATOM3D_CONSTRUCTION_POLICY"||op=="ATOM3D_CONSTRUCTION_RESULT"||op=="SB_CONSTRUCTION_RESULT"||op=="ATOM3D_CONSTRUCTION_MINIMUM_SET") return joint(op,p);
    if(op=="SB_COMPILE") {
        require(bool(store_),"Attach a durable store before loading Starbreaker");
        auto domain=std::make_unique<Starbreaker>(p.at("directory").get<std::string>(),resources_);
        if(state_.contains("starbreaker")) require(state_["starbreaker"]==domain->binding(),"Cannot replace an acquired Starbreaker source in this store");
        json next=state_; next["starbreaker"]=domain->binding(); next["sb_policy_object"]=store_->put(domain->policy());
        if(!next.contains("sb_accounts")) next["sb_accounts"]=json::object();
        store_->commit(next); state_=std::move(next); starbreaker_=std::move(domain); return starbreaker_->status();
    }
    if(op.rfind("SB_",0)==0) {
        require(bool(starbreaker_),"Compile the Starbreaker source first");
        if(op=="SB_STATUS"||op=="SB_READOUT"||op=="SB_HISTORY") return starbreaker_->execute(op,p,state_,store_.get());
        std::string batch_id=p.value("batch_id",std::string());auto request_sha=hash(request.dump());
        if(!batch_id.empty()&&state_.contains("sb_batches")&&state_["sb_batches"].contains(batch_id)){auto row=state_["sb_batches"][batch_id];require(row["request_sha256"]==request_sha,"SB batch identity changed");return store_->get(row["result"].get<std::string>());}
        auto payload=p;payload.erase("batch_id");json next=state_; auto result=starbreaker_->execute(op,payload,next,store_.get());
        if(!batch_id.empty())next["sb_batches"][batch_id]={{"request_sha256",request_sha},{"result",store_->put(result)}};
        next["sequence"]=state_["sequence"].get<uint64_t>()+1;
        json record={{"domain","STARBREAKER"},{"source",starbreaker_->binding()},{"request",request},{"result",result}};
        next["runs"].push_back(store_->put(record));
        next["knowledge"]["STARBREAKER:"+hash(request.dump())]={{"source_binding",starbreaker_->binding()["source_binding"]},{"operation",op},{"result_sha256",hash(result.dump())}};
        std::string root=store_->commit(next); state_=std::move(next);
        result["checkpoint"]={{"root",root},{"sequence",state_["sequence"]},{"status","COMMITTED"}}; return result;
    }
    if(op=="ATOM3D_COMPILE") {
        auto next=std::make_unique<Atom3d>(p.at("directory").get<std::string>(),resources_);
        if(p.contains("source_sha256")) require(next->binding()["source_sha256"]==p["source_sha256"],"Requested ATOM3D source differs");
        json next_state=state_; next_state["atom3d"]=next->binding();
        if(store_) store_->commit(next_state);
        state_=std::move(next_state); atom3d_=std::move(next); return atom3d_->status();
    }
    if(op.rfind("ATOM3D_",0)==0||op.rfind("LI6_",0)==0||op=="A3D41_CONTACT") {
        require(bool(atom3d_),"Compile the ATOM3D source first");
        auto result=atom3d_->execute(op,p);
        if(op=="ATOM3D_STATUS") return result;
        json record={{"domain","ATOM3D"},{"source",atom3d_->binding()},{"request",request},{"result",result}};
        json next=state_; next["sequence"]=state_["sequence"].get<uint64_t>()+1;
        next["runs"].push_back(store_?json(store_->put(record)):record);
        next["knowledge"]["ATOM3D:"+hash(request.dump())]={{"source_sha256",atom3d_->binding()["source_sha256"]},{"operation",op},{"result_sha256",hash(result.dump())}};
        if(store_) store_->commit(next);
        state_=std::move(next); return result;
    }
    if(op=="READOUT") {
        if(p.contains("account")) return log_account(state_.at("accounts").at(p["account"].get<std::string>()));
        const auto& c=contract(); uint32_t q=c.encode(p.at("state"));
        return {{"state",c.decode(q)},{"frame",c.frame(q,p.value("view","JOINT"))},
                {"action",c.has_contact?json(c.tables.contacts[c.tables.index[q]]):json(nullptr)}};
    }
    if(op=="HISTORY") {
        if(p.contains("account")) return state_.at("accounts").at(p["account"].get<std::string>());
        size_t run=p.at("run").get<size_t>(); const auto& item=state_.at("runs").at(run);
        return item.is_string()?store_->get(item.get<std::string>()):item;
    }
    if(op=="LOG_OPEN"||op=="LOG_APPEND"||op=="LOG_COMPOSE") {
        std::string name=p.at("account"); require(!name.empty(),"Account identity is empty"); json source;
        if(op=="LOG_APPEND") {
            source=state_.at("accounts").at(name);
            require(p.at("points").is_array()&&p.at("edges").is_array()&&p["points"].size()==p["edges"].size(),"Append needs each new point and connecting edge");
            for(const auto& point:p["points"]) source["points"].push_back(point);
            for(const auto& edge:p["edges"]) source["edges"].push_back(edge);
        } else {
            require(!state_["accounts"].contains(name),"Account already exists");
            if(op=="LOG_OPEN") { source=p; source.erase("account"); }
            else {
                const auto& left=state_.at("accounts").at(p.at("left").get<std::string>());
                const auto& right=state_.at("accounts").at(p.at("right").get<std::string>());
                require(left["quantity"]==right["quantity"]&&left["source_binding"]==right["source_binding"],"Compose identical quantity/source accounts");
                require(left["points"].back()==right["points"].front(),"Composition boundary occurrence differs");
                require(log_account(left)["status"]=="DEFINED"&&log_account(right)["status"]=="DEFINED","Compose positive segments explicitly");
                source=left;
                for(size_t i=1;i<right["points"].size();++i) source["points"].push_back(right["points"][i]);
                for(const auto& edge:right["edges"]) source["edges"].push_back(edge);
            }
        }
        json result=log_account(source),next=state_; next["accounts"][name]=source;
        if(store_) store_->commit(next);
        state_=std::move(next); return result;
    }
    if(op=="INVERSE") return inverse(p);
    if(op=="VERIFY_GPU_TABLES") {
        const auto& c=contract(); CudaBackend backend(c.tables); auto got=backend.frames();
        require(got==c.tables.frames,"Native GPU receiver compilation differs from CPU");
        return {{"status","PASS"},{"exact_values",got.size()}};
    }
    if(op=="T18_MAP_HASH") {
        CudaBackend backend(contract().tables); auto map=backend.map(); std::string bytes; bytes.reserve(map.size()*4);
        for(uint32_t value:map) for(int shift=24;shift>=0;shift-=8) bytes.push_back(char((value>>shift)&255));
        return {{"sha256_big_endian",hash(bytes)},{"transitions",map.size()}};
    }
    if(op=="RUN"||op=="GEN3_EXECUTE") {
        const auto& c=contract();
        if(!p.contains("initial")) { require(state_.contains("last"),"First run needs initial state"); p["initial"]=json::array({state_["last"]}); }
        auto b=c.batch(p); size_t expanded=product(product(b.count,b.steps+1),product(c.tables.channels+c.coordinates.size(),64));
        resources_.admit(expanded);
        json result=json::array(),next=state_;uint64_t reused=0,acquired=0;
        auto selected=p.value("backend",std::string("learned"));
        auto trace=(op=="GEN3_EXECUTE"||selected=="learned")?learned_run(b,next,reused,acquired):run(b,selected);
        for(size_t lane=0;lane<b.count;++lane) result.push_back(c.describe_trace(b,trace,lane));
        for(size_t step=0;step<b.steps;++step) for(size_t lane=0;lane<b.count;++lane) {
            uint32_t before=trace.states[step*b.count+lane],after=trace.states[(step+1)*b.count+lane]; size_t ev=b.events[step*b.count+lane];
            std::string key=c.id+":"+std::to_string(before)+":"+std::to_string(ev);
            next["knowledge"][key]={{"from",before},{"event",c.labels[ev]},{"to",after}};
        }
        next["sequence"]=next["sequence"].get<uint64_t>()+1; next["last"]=c.decode(trace.states.back());
        json record={{"sequence",next["sequence"]},{"contract",c.source},{"results",result},
                     {"execution",{{"backend",trace.backend},{"kernel_seconds",trace.kernel_seconds},{"wall_seconds",trace.wall_seconds},{"learned_events_executed",reused},{"native_events_acquired",acquired}}}};
        if(next.contains("core_statistics")){
            for(auto item:{std::pair{"learned_events_executed",reused},std::pair{"native_events_acquired",acquired}})next["core_statistics"][item.first]=next["core_statistics"][item.first].get<uint64_t>()+item.second;
            for(const auto& row:result){auto k=hash(json({{"contract",c.id},{"initial",row["initial"]},{"program",row["program"]},{"view",row["view"]}}).dump());next["core_compositions"][k]=store_->put(row);}
        }
        next["runs"].push_back(store_?json(store_->put(record)):record);
        if(store_) store_->commit(next);
        state_=std::move(next);
        return record;
    }
    throw std::invalid_argument("Operation has no native lowering in this core: "+op);
}
}
