#include "atom3d.hpp"
#include <algorithm>
#include <chrono>
#include <fstream>
#include <future>
#include <numeric>
#include <set>
#include <unordered_map>
#include <fcntl.h>
#include <unistd.h>
#include <omp.h>

namespace rxt {
namespace {
using Clock=std::chrono::steady_clock;
constexpr uint64_t FAMILIES=4800000,STRIDE=15485863,OFFSET=1060912;
constexpr size_t SET_BYTES=ADDRESS_COUNT/8;
double seconds(Clock::time_point a){return std::chrono::duration<double>(Clock::now()-a).count();}
double monotonic(){return std::chrono::duration<double>(Clock::now().time_since_epoch()).count();}
void check(bool b,const std::string& message){if(!b)throw std::invalid_argument("CONSTRUCTION: "+message);}
uint64_t natural(const json& p,const char* key,uint64_t fallback,uint64_t lo,uint64_t hi){auto v=p.value(key,json(fallback));check(v.is_number_integer()&&!v.is_boolean(),std::string(key)+" must be integer");auto n=v.get<int64_t>();check(n>=0&&uint64_t(n)>=lo&&uint64_t(n)<=hi,std::string(key)+" outside campaign bounds");return n;}
mpz_class integer128(A3DWide x){mpz_class n(std::to_string(x.hi));n<<=64;n+=mpz_class(std::to_string(x.lo));return n;}
std::string action(A3DWide x){mpq_class v(integer128(x),mpz_class(576));v.canonicalize();return v.get_str();}
bool equal(A3DWide a,A3DWide b){return a.lo==b.lo&&a.hi==b.hi;}
bool positive_gap(A3DWide separated,A3DWide connected){return separated.hi>connected.hi||(separated.hi==connected.hi&&separated.lo>connected.lo);}
void write_all(int fd,const char* p,size_t n){while(n){auto done=::write(fd,p,n);if(done<=0)throw std::runtime_error("Campaign artifact write failed");p+=done;n-=size_t(done);}}
void atomic_json(const std::filesystem::path& path,const json& value){
    auto temp=path.string()+".tmp";auto body=value.dump(2)+"\n";
    int fd=::open(temp.c_str(),O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC,0600);check(fd>=0,"Cannot write progress");
    try{write_all(fd,body.data(),body.size());check(fsync(fd)==0,"Cannot sync progress");::close(fd);fd=-1;std::filesystem::rename(temp,path);int d=::open(path.parent_path().c_str(),O_RDONLY|O_DIRECTORY);check(d>=0&&fsync(d)==0,"Cannot sync campaign directory");::close(d);}catch(...){if(fd>=0)::close(fd);throw;}
}
struct Family {
    uint64_t id=0;int rho=0,assignment=0,hidden=0,pair_policy=0,pattern=0,multiplicity[4]{};
    bool covered[9]{};int instances=0;
    json describe()const{return {{"id",id},{"rho",rho+1},{"assignment",assignment},{"hidden_operator_multiplicity",hidden},{"pair_policy",pair_policy?"REPLACE_COVERED_PAIRS":"RETAIN_ALL_PAIRS"},{"triad_multiplicities",std::vector<int>(multiplicity,multiplicity+4)},{"grammar_operator_instances",instances},{"field_type","CANDIDATE"}};}
};
struct Source {
    int64_t pair[2][9]{},triad[2][4]{},weights[6][3]{};int edges[4][3]{};
    const A3DInputs& in;
    explicit Source(const json& grammar,const A3DInputs& inputs):in(inputs){
        const auto& g=grammar.at("geometry");
        auto scaled=[](const json& x,int multiplier){mpq_class v=rational(x)*multiplier;check(v.get_den()==1,"Source operator cannot lower exactly");check(v.get_num().fits_slong_p(),"Source operator exceeds native integer");return int64_t(v.get_num().get_si());};
        for(int c=0;c<2;++c){std::string name=c?"observed":"native";for(int e=0;e<9;++e)pair[c][e]=scaled(g["pair_motifs"][e][name],576);for(int t=0;t<4;++t)triad[c][t]=scaled(g["triad_motifs"][t][name],192);}
        for(int t=0;t<4;++t)for(int k=0;k<3;++k)edges[t][k]=g["triad_motifs"][t]["edge_indices"][k];
        for(int a=0;a<6;++a)for(int e=0;e<3;++e)weights[a][e]=g["source_assignments"][a]["native_account_numerators"][e];
        // Exhaustive coefficient-bound admission over all source rho/placements.
        for(int a=0;a<6;++a)for(int r=0;r<128;++r){mpz_class b=0;for(int e=0;e<3;++e)for(int k=0;k<3;++k)b+=abs(mpz_class(std::to_string(in.tensors[(e*128+r)*3+k])))*weights[a][e]*8*128;check(b<mpz_class("9223372036854775807"),"Center requires wider pre-scaling accumulation");}
    }
    Family family(uint64_t id)const{
        check(id<FAMILIES,"Family outside construction lattice");Family f;f.id=id;auto x=id;f.rho=x%128;x/=128;f.assignment=x%6;x/=6;f.hidden=x%5;x/=5;f.pair_policy=x%2;x/=2;f.pattern=x;
        for(int t=0;t<4;++t){f.multiplicity[t]=x%5;x/=5;if(f.multiplicity[t])for(int k=0;k<3;++k)f.covered[edges[t][k]]=true;f.instances+=f.multiplicity[t];}
        for(int e=0;e<9;++e)f.instances+=!f.pair_policy||!f.covered[e];
        f.instances+=f.hidden;return f;
    }
    A3DQuery query(const Family& f,int context)const{
        A3DQuery q;q.mask=context%4;q.kind=(context/4)%2;int channel=(context/8)%2,receiver=(context/16)%2;
        for(int e=0;e<3;++e)for(int k=0;k<3;++k)q.center[e*3+k]=8*weights[f.assignment][e]*in.tensors[(e*128+f.rho)*3+k]*in.geometry.masks[q.mask*9+in.geometry.centers[e]];
        for(int e=0;e<9;++e)if(!f.pair_policy||!f.covered[e])q.motif[e]+=pair[channel][e]*in.geometry.masks[q.mask*9+e];
        for(int t=0;t<4;++t){int64_t w=triad[channel][t]*f.multiplicity[t];if(receiver)for(int k=0;k<3;++k)q.motif[edges[t][k]]+=w;else q.motif[9+t]+=w;}
        if(q.mask==3)q.motif[13]+=81*f.hidden;
        return q;
    }
};
struct Work {uint64_t ordinal=0;std::vector<Family> families;std::vector<A3DQuery> queries;};
Work make_work(const Source& source,uint64_t ordinal,size_t n){Work w;w.ordinal=ordinal;w.families.reserve(n);w.queries.reserve(n*32);for(size_t i=0;i<n;++i){auto f=source.family(((ordinal+i)*STRIDE+OFFSET)%FAMILIES);w.families.push_back(f);for(int c=0;c<32;++c)w.queries.push_back(source.query(f,c));}return w;}
uint64_t family_id(int pattern,int pair,int hidden,int assignment,int rho){return (((uint64_t(pattern)*2+pair)*5+hidden)*6+assignment)*128+rho-1;}
}

json Atom3d::construction_ids(const json& p){
    const auto& ids=p.at("family_ids");auto backend=p.value("backend",std::string("cuda"));
    check(backend=="cpu"||backend=="cuda","Explicit cpu or cuda backend required");
    check(ids.is_array()&&!ids.empty()&&ids.size()<=(backend=="cuda"?640:8),"Use 1..640 CUDA or 1..8 CPU families per exact batch");
    std::set<uint32_t> seen;std::vector<Family> families;std::vector<A3DQuery> queries;Source source(grammar_,inputs_);
    for(const auto& id:ids){check(id.is_number_integer()&&!id.is_boolean()&&id.get<int64_t>()>=0&&id.get<int64_t>()<int64_t(FAMILIES),"Invalid family ID");auto n=id.get<uint32_t>();check(seen.insert(n).second,"Repeated family ID");families.push_back(source.family(n));for(int c=0;c<32;++c)queries.push_back(source.query(families.back(),c));}
    uint64_t device=backend=="cuda"?queries.size()*(uint64_t(ADDRESS_COUNT)*16+65536)+(512ull<<20):0;
    uint64_t owned=backend=="cuda"&&gpu_?gpu_->resident_bytes():0;
    check(device<=resources_.gpu_budget||backend=="cpu","Construction workspace exceeds the native GPU budget");
    resources_.admit((256ull<<20)+queries.size()*SET_BYTES*3,device>owned?device-owned:0);
    auto started=Clock::now();A3DBatchMinimum bulk;std::vector<A3DMinimum> cpu;
    if(backend=="cuda"){ensure_gpu();bulk=gpu_->minimum_batch(queries);}else{cpu.reserve(queries.size());for(const auto& q:queries)cpu.push_back(minimum_cpu(q));}
    std::vector<std::string> digests(queries.size());
    #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static) if(queries.size()>64)
    for(size_t i=0;i<queries.size();++i)digests[i]=backend=="cuda"?hash(std::string(bulk.bits.data()+i*SET_BYTES,SET_BYTES)):hash(std::string(reinterpret_cast<const char*>(cpu[i].bits.data()),cpu[i].bits.size()));
    if(construction_set_cache_.size()>8192)construction_set_cache_=json::object();
    json rows=json::array(),sets=json::object();
    for(size_t f=0;f<families.size();++f){json row={{"schema","A3D41_EXACT_CONSTRUCTION_OUTCOME_V1"},{"family_id",families[f].id},{"family",families[f].describe()},{"source_contract","A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1"},{"source_domain_sha256",source_id_},{"origin","NATIVE_CONSTRUCTION"},{"contexts",json::array()}};
        for(int c=0;c<32;++c){size_t i=f*32+c;auto value=backend=="cuda"?bulk.values[i]:cpu[i].value;auto count=backend=="cuda"?bulk.counts[i]:cpu[i].count;
            auto digest=digests[i];
            if(!sets.contains(digest)&&construction_set_cache_.contains(digest)){check(construction_set_cache_[digest]["count"]==count,"Cached minimum-set count differs");sets[digest]=construction_set_cache_[digest];}
            if(!sets.contains(digest)){json quartet=json::array();bool orbit=false;
                std::string bits=backend=="cuda"?bulk.bits.substr(i*SET_BYTES,SET_BYTES):std::string(reinterpret_cast<const char*>(cpu[i].bits.data()),cpu[i].bits.size());
                if(count==4){std::set<uint32_t> states;for(uint32_t q=0;q<ADDRESS_COUNT;++q)if((uint8_t(bits[q/8])>>(q%8))&1)states.insert(q);check(states.size()==4,"Minimum count differs from complete bitset");
                    uint32_t q=*states.begin();std::set<uint32_t> rotation;for(int turn=0;turn<4;++turn){rotation.insert(q);uint32_t next=0;for(int edge=0;edge<9;++edge){int phase=(((q>>edge)&1)+2*((q>>(edge+9))&1)+1)%4;next|=uint32_t(phase&1)<<edge;next|=uint32_t(phase>>1)<<(edge+9);}q=next;}orbit=states==rotation;for(auto state:states)quartet.push_back(state);
                }
                static constexpr char hex[]="0123456789abcdef";std::string encoded(bits.size()*2,'0');for(size_t k=0;k<bits.size();++k){auto b=uint8_t(bits[k]);encoded[k*2]=hex[b>>4];encoded[k*2+1]=hex[b&15];}
                sets[digest]={{"sha256",digest},{"count",count},{"bits_hex",encoded},{"single_quarter_turn_orbit",orbit},{"four_states",quartet}};
                construction_set_cache_[digest]=sets[digest];
            }
            row["contexts"].push_back({{"context",c},{"minimum",action(value)},{"count",count},{"set",digest},{"single_quarter_turn_orbit",sets[digest]["single_quarter_turn_orbit"]},{"four_states",sets[digest]["four_states"]}});
        }rows.push_back(std::move(row));
    }
    return {{"schema","A3D41_EXACT_CONSTRUCTION_IDS_V1"},{"status","COMPLETE"},{"backend",backend},{"families",families.size()},{"exact_contexts",queries.size()},{"complete_minimum_sets",sets},{"rows",rows},{"wall_seconds",seconds(started)},{"gpu_kernel_seconds",bulk.kernel_seconds},{"gpu_batch_wall_seconds",bulk.wall_seconds},{"source_sha256",source_id_}};
}

json Atom3d::construction(const json& p){
    Source source(grammar_,inputs_);ensure_gpu();gpu_->table("CURRENTS",false);
    auto mode=p.value("mode",std::string("RUN"));
    if(mode=="CHECK"){
        std::vector<Family> families;
        for(auto id:{family_id(0,0,0,0,1),family_id(1,1,1,0,1),family_id(5,1,1,0,1),family_id(25,1,1,0,1),family_id(125,1,1,0,1),family_id(624,0,4,5,128),family_id(307,1,3,2,64)})families.push_back(source.family(id));
        std::vector<A3DQuery> queries;for(auto& f:families)for(int c=0;c<32;++c)queries.push_back(source.query(f,c));
        resources_.admit(256ull<<20,queries.size()*(uint64_t(ADDRESS_COUNT)*16+65536)+(256ull<<20));
        auto bulk=gpu_->minimum_batch(queries);size_t comparisons=0;
        for(size_t i=0;i<queries.size();++i){auto small=gpu_->minimum(queries[i]);check(equal(small.value,bulk.values[i])&&small.count==bulk.counts[i]&&std::equal(small.bits.begin(),small.bits.end(),reinterpret_cast<const uint8_t*>(bulk.bits.data()+i*SET_BYTES)),"Batch differs from independent single-query reduction");++comparisons;}
        size_t cpu_checks=0;for(size_t i:{size_t(3),size_t(11),size_t(31),size_t(160),size_t(171),size_t(191),size_t(195),size_t(219)}){auto cpu=minimum_cpu(queries[i]);check(equal(cpu.value,bulk.values[i])&&cpu.count==bulk.counts[i]&&std::equal(cpu.bits.begin(),cpu.bits.end(),reinterpret_cast<const uint8_t*>(bulk.bits.data()+i*SET_BYTES)),"Candidate CPU/GPU exact minimum differs");++cpu_checks;}
        size_t controls=0;for(int cover=0;cover<5;++cover)for(int channel=0;channel<2;++channel){json old={{"state",14336},{"cover",cover},{"hidden_loop",cover!=0},{"channel",channel?"observed":"native"}};auto ref=readout(old);size_t i=size_t(cover)*32+3+channel*8;check(ref["minimum_source_action"]==action(bulk.values[i])&&ref["minimum_state_count"]==bulk.counts[i]&&ref["minimum_state_set_sha256"]==hash(bulk.bits.substr(i*SET_BYTES,SET_BYTES)),"Current source-cover control differs");++controls;}
        return {{"status","PASS"},{"mode","CHECK"},{"batched_complete_minimum_sets",comparisons},{"independent_cpu_complete_minima",cpu_checks},{"current_source_cover_controls",controls},{"source_sha256",source_id_},{"native_gpu_kernel_seconds",bulk.kernel_seconds},{"batch_wall_seconds",bulk.wall_seconds},{"query_context_order","mask + 4*kind + 8*channel(native=0) + 16*receiver(circulation=0)"}};
    }
    if(mode=="CALIBRATE"){
        json samples=json::array();for(int n:{16,32,64,128}){auto w=make_work(source,0,n);resources_.admit(512ull<<20,w.queries.size()*(uint64_t(ADDRESS_COUNT)*16+65536)+(256ull<<20));auto first=gpu_->minimum_batch(w.queries);auto second=gpu_->minimum_batch(w.queries);check(first.bits==second.bits,"Calibration repeat differs");samples.push_back({{"families",n},{"queries",w.queries.size()},{"kernel_seconds",second.kernel_seconds},{"wall_seconds",second.wall_seconds},{"state_evaluations_per_second",double(w.queries.size())*ADDRESS_COUNT/second.wall_seconds},{"bitset_return_bytes",second.bits.size()}});}
        return {{"status","PASS"},{"mode","CALIBRATE"},{"samples",samples}};
    }
    check(mode=="RUN","Unknown campaign mode");
    size_t width=natural(p,"batch_families",128,1,256);uint64_t duration=natural(p,"duration_seconds",300,1,604800),cursor=natural(p,"start_ordinal",0,0,FAMILIES-1),limit=natural(p,"family_limit",FAMILIES,1,FAMILIES);limit=std::min(limit,FAMILIES-cursor);
    auto out=std::filesystem::absolute(p.at("output_directory").get<std::string>());check(!std::filesystem::exists(out),"Use a new campaign run directory");std::filesystem::create_directories(out);
    resources_.admit(uint64_t(width)*32*SET_BYTES*3+(256ull<<20),uint64_t(width)*32*(uint64_t(ADDRESS_COUNT)*16+65536)+(256ull<<20));
    json plan=p;plan["source"]=binding();plan["construction_schema"]="A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1";plan["family_count"]=FAMILIES;plan["permutation_multiplier"]=STRIDE;plan["permutation_offset"]=OFFSET;plan["contexts_per_family"]=32;plan["states_per_query"]=ADDRESS_COUNT;atomic_json(out/"PLAN.json",plan);
    Store journal(out/"journal");json state={{"schema","GEN_RXT_MACHINE_V1"},{"version",VERSION},{"sequence",0},{"runs",json::array()},{"accounts",json::object()},{"knowledge",json::object()},{"atom3d",binding()}};
    int sets_fd=::open((out/"MINIMUM_SETS.bin").c_str(),O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC,0600);check(sets_fd>=0,"Cannot create minimum-set archive");
    struct Close {int fd;~Close(){::close(fd);}} close{sets_fd};
    std::unordered_map<std::string,uint64_t> known_sets;uint64_t set_bytes=0,batches=0,completed=0,queries_done=0,initial_cursor=cursor;double kernel_seconds=0,gpu_wall=0,cpu_receipt_seconds=0;std::string previous;json frontier=json::array();
    auto start=Clock::now();double start_mono=monotonic();
    auto progress=[&](const char* status){return json{{"status",status},{"start_monotonic",start_mono},{"elapsed_seconds",seconds(start)},{"duration_requested_seconds",duration},{"families_completed",completed},{"queries_completed",queries_done},{"state_evaluations",queries_done*uint64_t(ADDRESS_COUNT)},{"next_ordinal",initial_cursor+completed},{"batch_count",batches},{"batch_families",width},{"unique_minimum_sets",known_sets.size()},{"minimum_set_bytes",set_bytes},{"native_gpu_kernel_seconds",kernel_seconds},{"gpu_batch_wall_seconds",gpu_wall},{"cpu_receipt_seconds",cpu_receipt_seconds},{"previous_batch",previous},{"source_sha256",source_id_}};};
    atomic_json(out/"PROGRESS.json",progress("RUNNING"));
    auto launch=[&](const Work& w){return std::async(std::launch::async,[this,q=w.queries]{return gpu_->minimum_batch(q);});};
    Work work=make_work(source,cursor,std::min<uint64_t>(width,limit));auto future=launch(work);
    while(true){
        auto result=future.get();auto receipt_start=Clock::now();uint64_t next_completed=completed+work.families.size();bool more=seconds(start)<duration&&next_completed<limit;
        Work next;std::future<A3DBatchMinimum> next_future;if(more){next=make_work(source,initial_cursor+next_completed,std::min<uint64_t>(width,limit-next_completed));next_future=launch(next);}
        std::vector<std::string> hashes(result.values.size());
        #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static)
        for(size_t i=0;i<hashes.size();++i)hashes[i]=hash(std::string(result.bits.data()+i*SET_BYTES,SET_BYTES));
        json additions=json::array();for(size_t i=0;i<hashes.size();++i)if(!known_sets.contains(hashes[i])){known_sets[hashes[i]]=set_bytes;write_all(sets_fd,result.bits.data()+i*SET_BYTES,SET_BYTES);additions.push_back({{"sha256",hashes[i]},{"offset",set_bytes},{"bytes",SET_BYTES},{"state_count",result.counts[i]}});set_bytes+=SET_BYTES;}
        check(fsync(sets_fd)==0,"Cannot sync minimum sets");json rows=json::array();
        for(size_t f=0;f<work.families.size();++f){auto& family=work.families[f];json row={{"family",family.describe()},{"contexts",json::array()}};
            for(int c=0;c<32;++c){size_t i=f*32+c;row["contexts"].push_back({{"context",c},{"minimum",action(result.values[i])},{"count",result.counts[i]},{"set",hashes[i]}});}
            uint32_t native_count=result.counts[f*32+3],observed_count=result.counts[f*32+11];bool gap=positive_gap(result.values[f*32],result.values[f*32+3])&&positive_gap(result.values[f*32+8],result.values[f*32+11]);
            row["positive_connected_gap_both_channels"]=gap;
            if(gap){json candidate={{"family",family.describe()},{"native_minimum_count",native_count},{"observed_minimum_count",observed_count},{"operator_instances",family.instances},{"native_set",hashes[f*32+3]},{"observed_set",hashes[f*32+11]}};bool dominated=false;
                for(auto& old:frontier)if(old["native_minimum_count"].get<uint32_t>()<=native_count&&old["observed_minimum_count"].get<uint32_t>()<=observed_count&&old["operator_instances"].get<int>()<=family.instances){dominated=true;break;}
                if(!dominated){json keep=json::array();for(auto& old:frontier)if(!(native_count<=old["native_minimum_count"].get<uint32_t>()&&observed_count<=old["observed_minimum_count"].get<uint32_t>()&&family.instances<=old["operator_instances"].get<int>()))keep.push_back(old);keep.push_back(candidate);frontier=std::move(keep);}
            }rows.push_back(row);
        }
        json batch={{"schema","GEN_RXT_CONSTRUCTION_BATCH_V1"},{"ordinal",work.ordinal},{"family_count",work.families.size()},{"source_sha256",source_id_},{"previous_batch",previous},{"new_minimum_sets",additions},{"minimum_set_extent_bytes",set_bytes},{"rows",rows},{"gpu_kernel_seconds",result.kernel_seconds},{"gpu_batch_wall_seconds",result.wall_seconds}};
        previous=journal.put(batch);state["runs"]=json::array({previous});state["sequence"]=++batches;completed=next_completed;queries_done+=result.values.size();kernel_seconds+=result.kernel_seconds;gpu_wall+=result.wall_seconds;
        state["construction"]={{"next_ordinal",initial_cursor+completed},{"last_batch",previous},{"minimum_set_extent_bytes",set_bytes},{"plan_sha256",hash(plan.dump())}};journal.commit(state);
        cpu_receipt_seconds+=seconds(receipt_start);atomic_json(out/"PROGRESS.json",progress("RUNNING"));atomic_json(out/"FRONTIER.json",frontier);
        if(!more)break;
        work=std::move(next);future=std::move(next_future);
    }
    auto result=progress("TRIAL_COMPLETE");result["frontier"]=frontier;result["run_directory"]=out.string();result["minimum_sets_complete"]=true;result["work_repeated_for_utilization"]=false;result["query_context_order"]="mask + 4*kind + 8*channel(native=0) + 16*receiver(circulation=0)";result["native_revision"]="A3D41-RXT-CONSTRUCTION-R1";result["scientific_scope"]="Typed candidate operator construction on the admitted Li-6 source; paired phase/mask/channel/receiver controls";atomic_json(out/"PROGRESS.json",result);atomic_json(out/"RESULT.json",result);return result;
}
}
