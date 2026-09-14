#include "starbreaker.hpp"
#include "signed_energy.hpp"
#include "starbreaker_binding.hpp"
#include <algorithm>
#include <chrono>
#include <fstream>
#include <set>
#include <omp.h>

namespace rxt {
namespace {
void need(bool b,const std::string& why) { if(!b) throw std::invalid_argument(why); }
std::string bytes(const std::filesystem::path& p) { std::ifstream f(p,std::ios::binary); need(bool(f),"Cannot read Starbreaker source: "+p.string()); return {std::istreambuf_iterator<char>(f),{}}; }
uint64_t natural(const json& x,uint64_t low,uint64_t high,const std::string& name) {
    need(x.is_number_integer()&&!x.is_boolean(),name+" needs an integer");
    if(x.is_number_unsigned()) { auto n=x.get<uint64_t>(); need(n>=low&&n<=high,name+" outside admitted range"); return n; }
    auto n=x.get<int64_t>(); need(n>=0&&uint64_t(n)>=low&&uint64_t(n)<=high,name+" outside admitted range"); return uint64_t(n);
}
void fields(const json& p,const std::set<std::string>& names) { need(p.is_object(),"Starbreaker payload must be an object"); for(auto i=p.begin();i!=p.end();++i) need(names.count(i.key()),"Unknown Starbreaker field: "+i.key()); }
uint32_t translate(uint32_t a,const int* delta,int sign=1) {
    uint32_t b=0;
    for(int c=0;c<9;++c) { int q=(int((a>>c)&1)+2*int((a>>(c+9))&1)+sign*delta[c]+8)%4; b|=(uint32_t(q&1)<<c)|(uint32_t(q>>1)<<(c+9)); }
    return b;
}
json execution(const std::string& backend,const SBExecution& e) { return {{"backend",backend},{"kernel_seconds",e.kernel_seconds},{"wall_seconds",e.wall_seconds}}; }
}
void sb_features(const SBPolicyIR& p,uint32_t family,int64_t* out) {
    uint32_t a=family; out[7]=a%128+1; a/=128; out[6]=a%6; a/=6; out[4]=a%5; a/=5; out[5]=a%2; a/=2;
    auto pattern=a; for(int i=0;i<4;++i) { out[i]=a%5; a/=5; }
    out[8]=p.inventory[(pattern*5+out[4])*2+out[5]];
    std::copy_n(p.features.data()+pattern*23,23,out+9);
}
int sb_leaf(const SBPolicyIR& p,uint32_t family,int root) {
    int64_t features[32]; sb_features(p,family,features); int at=root;
    while(p.nodes[at].feature>=0) { const auto& n=p.nodes[at]; at=features[n.feature]<=n.threshold?n.left:n.right; }
    return at;
}
SBCycleResult sb_cycle_cpu(const SBCycle& j) {
    SBCycleResult r; r.addresses[0]=translate(j.initial,j.h);
    for(int k=1;k<=j.steps;++k) r.addresses[k]=translate(r.addresses[k-1],j.v);
    r.recovered=translate(r.addresses[j.steps],j.h,-1);
    for(int k=0;k<4;++k) { int64_t x=j.amplitudes[2*k],y=j.amplitudes[2*k+1]; r.actions[k]=x*x+y*y; }
    return r;
}
int Starbreaker::flatten(const json& node,const json& model,int target) {
    int id=int(ir_.nodes.size()); ir_.nodes.push_back({}); nodes_.push_back(node); node_models_.push_back(target);
    // Only the selected tree depth is executable; deeper development nodes
    // remain preserved in the acquired source package.
    if(!node.at("split").is_null()&&node.at("depth")<model.at("selected_depth")) {
        int local=int(natural(node["split"].at("feature"),0,model.at("columns").size()-1,"split feature"));
        int coordinate=int(natural(model["columns"][local],0,31,"feature coordinate"));
        need(node["split"].at("threshold").is_number_integer(),"Native policy threshold must be an exact integer");
        int left=flatten(node.at("left"),model,target),right=flatten(node.at("right"),model,target);
        ir_.nodes[id]={coordinate,left,right,node["split"]["threshold"].get<int64_t>()};
    }
    need(rational(node.at("probability"))>=0&&rational(node.at("probability"))<=1,"Policy probability outside 0..1");
    return id;
}
Starbreaker::Starbreaker(const std::filesystem::path& directory,const Resources& resources):resources_(resources) {
    auto dir=std::filesystem::absolute(directory); auto manifest_bytes=bytes(dir/"BUNDLE.json");
    need(hash(manifest_bytes)==SB_BUNDLE_SHA,"Starbreaker bundle differs from compiled source binding");
    auto manifest=json::parse(manifest_bytes); need(manifest.at("schema")=="SB_GEN3_RXT_SOURCE_V1","Starbreaker bundle schema differs");
    resources_.admit(512ull*1024*1024);
    for(auto i=manifest.at("files").begin();i!=manifest["files"].end();++i) {
        need(i.key().find('/')==std::string::npos&&i.key().find("..") == std::string::npos,"Invalid source filename");
        need(hash(bytes(dir/i.key()))==i.value().get<std::string>(),"Starbreaker file digest differs: "+i.key());
    }
    source_binding_=read_json(dir/"SOURCE_BINDING.json"); source_id_=hash(source_binding_.dump());
    need(source_id_==manifest.at("native_port_of_binding").get<std::string>(),"Starbreaker source identity differs");
    policy_=read_json(dir/"POLICY.json"); need(policy_.at("models").size()==45&&policy_.at("names").size()==32,"Acquired policy dimensions differ");
    need(source_binding_.at("policy_sha256")==manifest["files"]["POLICY.json"],"Acquired model source differs");
    for(const auto& row:policy_.at("feature_table")) { need(row.size()==23,"Feature row width differs"); for(const auto& v:row) { need(v.is_number_integer(),"Feature must be an integer"); ir_.features.push_back(v.get<int64_t>()); } }
    for(const auto& pattern:policy_.at("inventory_counts")) { need(pattern.size()==5,"Inventory hidden width differs"); for(const auto& hidden:pattern) { need(hidden.size()==2,"Inventory pair width differs"); for(const auto& v:hidden) ir_.inventory.push_back(int64_t(natural(v,0,1000000,"inventory"))); } }
    need(ir_.features.size()==625*23&&ir_.inventory.size()==625*5*2,"Feature table domain differs");
    for(auto i=policy_["models"].begin();i!=policy_["models"].end();++i) { int target=int(names_.size()); names_.push_back(i.key()); ir_.roots.push_back(flatten(i.value().at("model").at("tree"),i.value().at("model"),target)); }
    std::ifstream responses(dir/"responses.jsonl"); std::string line;
    while(std::getline(responses,line)) if(!line.empty()) {
        auto r=json::parse(line); auto key=std::make_pair(r.at("relation_id").get<std::string>(),int(natural(r.at("rho"),1,128,"rho")));
        need(responses_.emplace(key,r).second,"Duplicate response source");
        for(const auto* direction:{"forward_amplitude","reverse_amplitude"}) {
            need(r.at(direction).size()==4,"Signed response needs four phases");
            for(const auto& a:r[direction]) { need(a.size()==2,"Signed receiver needs two components"); for(const auto& x:a) need(x.is_number_integer()&&x>=-2147483647LL&&x<=2147483647LL,"Squared source exceeds exact signed int64 admission"); }
        }
    }
    std::ifstream packets(dir/"packets.jsonl"); size_t packet_count=0;
    while(std::getline(packets,line)) if(!line.empty()) {
        auto r=json::parse(line); auto key=std::make_tuple(r.at("relation_id").get<std::string>(),r.at("direction").get<std::string>(),uint32_t(natural(r.at("incoming_theta18_address"),0,262143,"incoming address")));
        auto phase=natural(r.at("phase"),0,3,"phase"); need(packets_[key][phase].is_null(),"Duplicate packet source phase"); packets_[key][phase]=std::move(r); ++packet_count;
    }
    need(responses_.size()==1152&&packets_.size()==18318&&packet_count==73272,"Starbreaker source cardinality differs");
    binding_={{"directory",dir.string()},{"bundle_sha256",SB_BUNDLE_SHA},{"source_binding",source_id_},{"policy_sha256",source_binding_["policy_sha256"]},{"native_domain",SB_VERSION},{"source_domain","SB-GEN3-ACCUMULATION-R1"}};
}
json Starbreaker::status() const {
    return {{"domain_update","SB-GEN3-RXT-R2"},{"version",SB_VERSION},{"execution_engine",VERSION},{"basis","SLC-GEN3-R3"},{"binding",binding_},{"learned_targets",names_},{"native_tree_nodes",ir_.nodes.size()},
        {"operations",{"SB_STATUS","SB_J4_ACCUMULATE","SB_J4_BATCH","SB_READOUT","SB_HISTORY","SB_CONSTRUCTION_POLICY","SB_POLICY_SCAN"}},
        {"gpu_resident_bytes",gpu_?gpu_->resident_bytes():0},{"exact_logarithms","ARBITRARY_PRECISION_POSITIVE_RATIONAL_ARGUMENTS"}};
}
void Starbreaker::adopt(const std::string& target,const json& learned){
    need(policy_["models"].contains(target),"Unknown learned target");
    need(learned.at("target_definition")==policy_["models"][target]["target_definition"],"Learned target changes its source meaning");
    need(learned.at("baseline_policy_sha256")==binding_.at("policy_sha256"),"Learned head belongs to another baseline source");
    auto previous=policy_["models"][target];policy_["models"][target]=learned;
    try {
        SBPolicyIR saved=ir_;auto saved_nodes=nodes_;auto saved_models=node_models_;
        ir_.nodes.clear();ir_.roots.clear();nodes_.clear();node_models_.clear();
        try {for(size_t i=0;i<names_.size();++i){const auto& m=policy_["models"][names_[i]]["model"];ir_.roots.push_back(flatten(m.at("tree"),m,int(i)));}}
        catch(...){ir_=std::move(saved);nodes_=std::move(saved_nodes);node_models_=std::move(saved_models);throw;}
        gpu_.reset();
    }catch(...){policy_["models"][target]=std::move(previous);throw;}
}
json Starbreaker::campaign_requests(uint64_t start,size_t count,const std::string& prefix) const {
    std::vector<std::tuple<std::string,std::string,uint32_t>> keys;for(const auto& row:packets_)keys.push_back(row.first);
    json rows=json::array();for(size_t i=0;i<count;++i){uint64_t n=start+i;const auto& k=keys[(n*7919)%keys.size()];rows.push_back({{"account",prefix+"."+std::to_string(i)},{"relation",std::get<0>(k)},{"direction",std::get<1>(k)},{"incoming_address",std::get<2>(k)},{"rho",1+(n*37)%128},{"cycles",1+(n/128)%16}});}return rows;
}
SBGpu& Starbreaker::gpu() { if(!gpu_) { resources_.admit(16*1024*1024,16*1024*1024); gpu_=std::make_unique<SBGpu>(ir_); } return *gpu_; }
std::string Starbreaker::backend(const json& p,size_t size) const {
    auto b=p.value("backend",std::string("auto")); need(b=="cpu"||b=="cuda"||b=="auto","Backend must be cpu, cuda or auto");
    return b=="auto"?(size>=64?"cuda":"cpu"):b;
}
std::vector<int> Starbreaker::targets(const json& p) const {
    auto selected=p.value("targets",json::array({"shared_four_state_orbit","channel_minimum_sets_agree"}));
    need(selected.is_array()&&!selected.empty()&&selected.size()<=45,"Select 1..45 learned targets"); std::set<int> seen; std::vector<int> result;
    for(const auto& name:selected) { need(name.is_string(),"Target must be a name"); auto i=std::find(names_.begin(),names_.end(),name.get<std::string>()); need(i!=names_.end(),"Unknown learned target"); int id=int(i-names_.begin()); need(seen.insert(id).second,"Repeated learned target"); result.push_back(id); }
    return result;
}
json Starbreaker::policies(const json& p,bool scan) {
    fields(p,scan?std::set<std::string>{"start_family","count","source_contract","targets","backend"}:std::set<std::string>{"family_ids","source_contract","targets","backend"});
    need(p.value("source_contract",std::string())==policy_.at("source_contract").get<std::string>(),"Policy requires A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1");
    auto chosen=targets(p); std::vector<int> roots; json selected_names=json::array(); for(int i:chosen) { roots.push_back(ir_.roots[i]); selected_names.push_back(names_[i]); }
    SBExecution timing;
    if(scan) {
        auto start=uint32_t(natural(p.at("start_family"),0,4799999,"start_family")); auto count=uint32_t(natural(p.at("count"),1,4800000-start,"count"));
        std::string device=backend(p,size_t(count)*roots.size()); std::vector<uint64_t> counts;
        resources_.admit(64*1024*1024,device=="cuda"?64*1024*1024:0);
        if(device=="cuda") counts=gpu().scan(start,count,roots,timing);
        else {
            auto begin=std::chrono::steady_clock::now(); counts.assign(ir_.nodes.size(),0);
            #pragma omp parallel num_threads(resources_.cpu_threads)
            {
                std::vector<uint64_t> local(counts.size(),0);
                #pragma omp for schedule(static)
                for(uint32_t i=0;i<count;++i) for(int root:roots) ++local[sb_leaf(ir_,start+i,root)];
                #pragma omp critical
                for(size_t i=0;i<counts.size();++i) counts[i]+=local[i];
            }
            timing.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
        }
        json hist=json::object(); uint64_t total=0;
        for(int target:chosen) hist[names_[target]]=json::array();
        for(size_t i=0;i<counts.size();++i) if(counts[i]) {
            total+=counts[i]; hist[names_[node_models_[i]]].push_back({{"decision_path",nodes_[i]["path"]},{"probability",nodes_[i]["probability"]},{"family_count",counts[i]},{"training_support",nodes_[i]["training_families"]}});
        }
        need(total==uint64_t(count)*roots.size(),"Incomplete native learned-policy scan");
        return {{"schema","SB_GEN3_RXT_POLICY_SCAN_V1"},{"version",SB_VERSION},{"source_contract",policy_["source_contract"]},{"acquired_policy_sha256",source_binding_["policy_sha256"]},{"start_family",start},{"family_count",count},{"policy_applications",total},{"targets",selected_names},{"complete_leaf_counts",hist},{"leaf_counts_sha256",hash(hist.dump())},{"execution",execution(device,timing)}};
    }
    const auto& input=p.at("family_ids"); need(input.is_array()&&!input.empty()&&input.size()<=4096&&input.size()*roots.size()<=16384,"Limit request to 4096 unique families and 16384 policy applications");
    std::vector<uint32_t> ids; std::set<uint32_t> unique;
    for(const auto& i:input) { auto n=uint32_t(natural(i,0,4799999,"family_id")); need(unique.insert(n).second,"Repeated candidate family"); ids.push_back(n); }
    std::string device=backend(p,ids.size()*roots.size()); std::vector<int> leaves;
    if(device=="cuda") leaves=gpu().predict(ids,roots,timing);
    else { auto begin=std::chrono::steady_clock::now(); leaves.resize(ids.size()*roots.size());
        #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static) if(ids.size()>64)
        for(size_t i=0;i<ids.size();++i) for(size_t j=0;j<roots.size();++j) leaves[i*roots.size()+j]=sb_leaf(ir_,ids[i],roots[j]);
        timing.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
    }
    json rows=json::array(); std::map<std::vector<std::string>,std::vector<uint32_t>> groups;
    for(size_t i=0;i<ids.size();++i) {
        int64_t f[32]; sb_features(ir_,ids[i],f); json source=json::object(),predictions=json::object(); std::vector<std::string> scores;
        for(size_t k=0;k<9;++k) source[policy_["names"][k].get<std::string>()]=f[k];
        for(size_t j=0;j<roots.size();++j) {
            int leaf=leaves[i*roots.size()+j]; need(leaf>=0&&size_t(leaf)<nodes_.size()&&node_models_[leaf]==chosen[j]&&ir_.nodes[leaf].feature<0,"CUDA policy returned an invalid leaf");
            const auto& node=nodes_[leaf]; json questions=json::array(); std::string path=node.at("path"); int at=roots[j];
            for(size_t k=4;k<path.size();++k) { const auto& n=ir_.nodes[at]; bool left=path[k]=='L'; need(n.feature>=0&&(path[k]=='L'||path[k]=='R'),"Policy path differs"); questions.push_back({{"feature",policy_["names"][n.feature]},{"value",f[n.feature]},{"threshold",n.threshold},{"branch",left?"left":"right"}}); at=left?n.left:n.right; }
            need(at==leaf,"Acquired leaf ancestry differs");
            auto target=names_[chosen[j]]; predictions[target]={{"probability",node["probability"]},{"training_support",node["training_families"]},{"decision_path",node["path"]},{"questions",questions},{"model_sha256",policy_["models"][target]["sha256"]}};
            scores.push_back(node["probability"].get<std::string>());
        }
        rows.push_back({{"family_id",ids[i]},{"source_fields",source},{"predictions",predictions}}); groups[scores].push_back(ids[i]);
    }
    std::vector<std::vector<std::string>> order; for(const auto& g:groups) order.push_back(g.first);
    std::sort(order.begin(),order.end(),[](const auto& a,const auto& b) { for(size_t i=0;i<a.size();++i) { auto x=rational(a[i]),y=rational(b[i]); if(x!=y) return x>y; } return false; });
    json ranking=json::array(); for(const auto& score:order) { json values=json::object(); for(size_t j=0;j<chosen.size();++j) values[names_[chosen[j]]]=score[j]; auto families=groups[score]; std::sort(families.begin(),families.end()); ranking.push_back({{"probabilities",values},{"family_ids",families}}); }
    return {{"schema","SB_GEN3_CONSTRUCTION_PROPOSALS_V1"},{"version",SB_VERSION},{"source_contract",policy_["source_contract"]},{"acquired_policy_sha256",source_binding_["policy_sha256"]},{"status","ACQUIRED_PREDICTIONS"},{"rows",rows},{"ranked_tie_groups",ranking},{"execution",execution(device,timing)}};
}
json Starbreaker::accumulate(const json& p,json& state,Store* store) {
    fields(p,{"requests","backend"}); const auto& requests=p.at("requests"); need(requests.is_array()&&!requests.empty()&&requests.size()<=4096,"Admit 1..4096 J4 histories per batch");
    need(store!=nullptr,"Attach a durable store before accumulating Starbreaker histories");
    std::vector<SBCycle> jobs; std::vector<json> selections; std::set<std::string> accounts;
    for(const auto& q:requests) {
        fields(q,{"account","relation","direction","rho","incoming_address","cycles","receiver_family_ids"});
        need(q.at("account").is_string(),"Account must be a name"); std::string name=q["account"]; need(!name.empty()&&name.size()<=128&&accounts.insert(name).second,"Account name empty, too long or repeated in batch");
        auto rho=natural(q.at("rho"),1,128,"rho"),incoming=natural(q.at("incoming_address"),0,262143,"incoming_address"),cycles=natural(q.value("cycles",json(1)),1,16,"cycles");
        need(q.at("relation").is_string()&&q.at("direction").is_string(),"Relation and direction must be source names");
        std::string relation=q["relation"],direction=q["direction"]; need(direction=="FORWARD"||direction=="REVERSE","Use FORWARD or REVERSE");
        auto packet=packets_.find({relation,direction,uint32_t(incoming)}); auto response=responses_.find({relation,int(rho)});
        need(packet!=packets_.end()&&response!=responses_.end(),"Selection outside retained J4 packet/response support");
        json selection={{"relation",relation},{"direction",direction},{"rho",rho},{"incoming_address",incoming},{"source_binding",source_id_}};
        if(state["sb_accounts"].contains(name)){const auto& entry=state["sb_accounts"][name];auto account=entry.is_string()?store->get(entry.get<std::string>()):entry;need(account["selection"]==selection,"Cannot append a different source to a Starbreaker account");}
        const auto& first=packet->second[0]; const auto& amplitudes=response->second[direction=="FORWARD"?"forward_amplitude":"reverse_amplitude"];
        SBCycle job; job.initial=uint32_t(incoming); job.steps=int(cycles*4);
        for(int c=0;c<9;++c) { job.h[c]=int(natural(first["retained_history_translation"][c],0,3,"history translation")); job.v[c]=int(natural(first["signed_w8_translation"][c],0,3,"phase translation")); }
        for(int k=0;k<4;++k) for(int c=0;c<2;++c) job.amplitudes[2*k+c]=amplitudes[k][c].get<int64_t>();
        jobs.push_back(job); selections.push_back(selection);
    }
    SBExecution timing; std::string device=backend(p,jobs.size()); std::vector<SBCycleResult> results;
    resources_.admit(uint64_t(jobs.size())*65536+16*1024*1024,device=="cuda"?uint64_t(jobs.size())*(sizeof(SBCycle)+sizeof(SBCycleResult)):0);
    if(device=="cuda") results=gpu().cycles(jobs,timing);
    else { auto begin=std::chrono::steady_clock::now(); results.resize(jobs.size());
        #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static) if(jobs.size()>64)
        for(size_t i=0;i<jobs.size();++i) results[i]=sb_cycle_cpu(jobs[i]);
        timing.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
    }
    json answers=json::array();
    for(size_t i=0;i<jobs.size();++i) {
        const auto& q=requests[i]; const auto& selection=selections[i]; const auto& job=jobs[i]; const auto& r=results[i];
        std::string name=q["account"],relation=q["relation"],direction=q["direction"];
        const auto& packets=packets_.at({relation,direction,job.initial}); const auto& response=responses_.at({relation,q["rho"].get<int>()});
        for(int k=0;k<=job.steps;++k) need(r.addresses[k]==packets[k%4].at("outgoing_theta18_address"),"Native J4 phase propagation differs from retained source");
        need(r.recovered==job.initial&&r.addresses[0]==r.addresses[job.steps],"Native J4 closure/inverse differs");
        for(auto a:r.actions) need(a>0,"J4 response norm must be positive");
        bool old=state["sb_accounts"].contains(name);json account=old?state["sb_accounts"][name]:json::object();if(account.is_string())account=store->get(account.get<std::string>());
        uint64_t prior=old?account.at("readout").at("edge_count").get<uint64_t>():0;
        json points=json::array(),edges=json::array();
        mpq_class initial=old?rational(account["readout"]["summary"]["initial_action"]):mpq_class(r.actions[0]);
        mpq_class previous=old?rational(account["readout"]["summary"]["final_action"]):initial;
        mpq_class up=old?rational(account["readout"]["summary"]["U"]["argument"]):mpq_class(1);
        mpq_class down=old?rational(account["readout"]["summary"]["D"]["argument"]):mpq_class(1);
        mpq_class maximum=old?rational(account["readout"]["summary"]["M"]["argument"]):mpq_class(1);
        json ties=old?account["readout"]["summary"]["maximizing_points"]:json::array({name+"/shell/0"});
        auto direction_key=direction=="FORWARD"?"forward_amplitude":"reverse_amplitude";
        for(int local=old?1:0;local<=job.steps;++local) {
            auto step=prior+uint64_t(local); int phase=local%4; std::string id=name+"/shell/"+std::to_string(step); mpq_class action=r.actions[phase];
            points.push_back({{"id",id},{"status","OBSERVED"},{"action",number(action)},{"state",{{"source_selection",selection},{"shell",step},{"phase",phase},{"theta18_address",r.addresses[local]},{"signed_amplitude",response[direction_key][phase]},{"response_source_row",response["semantic_sha256"]},{"packet_source_row",packets[phase]["semantic_sha256"]}}}});
            if(local>0) {
                edges.push_back({{"id",name+"/edge/"+std::to_string(step)},{"before",name+"/shell/"+std::to_string(step-1)},{"after",id},{"event",{{"signed_w8_translation",packets[0]["signed_w8_translation"]},{"direction",direction},{"relation",relation},{"shell",step}}}});
                mpq_class delta=action/previous; if(delta>1) up*=delta; else if(delta<1) down/=delta;
                mpq_class excursion=action/initial; if(excursion>maximum) { maximum=excursion; ties=json::array({id}); } else if(excursion==maximum) ties.push_back(id);
            }
            previous=action;
        }
        mpq_class net=previous/initial; need(up/down==net,"Native exact accumulation identity differs");
        json summary={{"initial_action",number(initial)},{"final_action",number(previous)},{"first_point",name+"/shell/0"},{"last_point",name+"/shell/"+std::to_string(prior+job.steps)},{"edge_count",prior+job.steps},
            {"U",log_value(up)},{"D",log_value(down)},{"V",log_value(mpq_class(up*down))},{"L",log_value(net)},{"net",log_value(net)},{"M",log_value(maximum)},{"maximizing_points",ties}};
        json quantity={{"kind","SB_SIGNED_RECEIVER_NORM_SQUARED"},{"units",{{"native_receiver_amplitude",2}}},{"normalization",{{"source_account",name},{"ratio_reference","original positive source point"}}},{"reference_state",name+"/shell/0"},{"frame",response[direction=="FORWARD"?"forward_frame_id":"reverse_frame_id"]},{"scope","HISTORY"},{"sign_convention","NONNEGATIVE_VALUE"},{"source",response["semantic_sha256"]}};
        json chunk={{"schema","SB_GEN3_RXT_HISTORY_CHUNK_V1"},{"source_binding",source_id_},{"account",name},{"previous",old?account["history_head"]:json(nullptr)},{"points",points},{"edges",edges}};
        std::string head=store->put(chunk);
        json readout={{"schema","GEN_RXT_LOG_READOUT_V1"},{"status","DEFINED"},{"quantity",quantity},{"source_binding",selection},{"point_count",prior+job.steps+1},{"edge_count",prior+job.steps},{"summary",summary},{"normalization",{{"kind","ORIGINAL_POSITIVE_SOURCE_RATIO"},{"reference_point",name+"/shell/0"}}},{"full_history_retained",true}};
        json energy_edges=json::array();
        for(int k=0;k<4;++k) {
            json left=response[direction_key][k],right=response[direction_key][(k+1)%4];
            auto edge=signed_energy(left,right,mpq_class(1),mpq_class(1));
            edge["phase"]=k;energy_edges.push_back(edge);
        }
        readout["signed_energy"]={{"revision","SB-GEN3-RXT-R2"},{"quantity","SIGNED_RECEIVER_VECTOR_DIFFERENCE"},{"support","ONE_SOURCE_PHASE_PER_CHILD"},{"edges_per_cycle",energy_edges},{"cycles_in_chunk",job.steps/4},{"physical_action_unchanged",true}};
        state["sb_accounts"][name]=store->put({{"selection",selection},{"readout",readout},{"history_head",head}});
        json actions=json::array(),addresses=json::array(); for(auto a:r.actions) actions.push_back(std::to_string(a)); for(int k=0;k<=job.steps;++k) addresses.push_back(r.addresses[k]);
        int h=0,v=0; for(int c=0;c<9;++c) { h+=job.h[c]==3?1:job.h[c]; v+=job.v[c]==3?1:job.v[c]; }
        json answer={{"schema","SB_GEN3_J4_ACCUMULATION_V1"},{"version",SB_VERSION},{"source_selection",selection},{"action_profile",source_binding_["action_profile"]},{"actions_per_cycle",actions},{"native_shell_addresses",addresses},{"accumulation",readout},{"history_head",head},
            {"propagation",{{"source_match",true},{"closed",true},{"inverse_recovered",true},{"native_writes",2*h+job.steps*v}}},{"construction_proposals",nullptr}};
        if(q.contains("receiver_family_ids")) answer["construction_proposals"]=policies({{"family_ids",q["receiver_family_ids"]},{"source_contract",policy_["source_contract"]}},false);
        answers.push_back(std::move(answer));
    }
    return {{"schema","SB_GEN3_RXT_J4_BATCH_V1"},{"version",SB_VERSION},{"results",answers},{"histories",jobs.size()},{"execution",execution(device,timing)}};
}
json Starbreaker::execute(const std::string& op,const json& p,json& state,Store* store) {
    need(p.is_object(),"Starbreaker payload must be an object");
    if(op=="SB_STATUS") { need(p.empty(),"SB_STATUS takes an empty payload"); return status(); }
    if(op=="SB_CONSTRUCTION_POLICY"||op=="SB_POLICY_SCAN") return policies(p,op=="SB_POLICY_SCAN");
    if(op=="SB_READOUT"||op=="SB_HISTORY") {
        fields(p,{"account"}); need(p.at("account").is_string(),"Account must be a name"); std::string name=p["account"];
        auto account=state.at("sb_accounts").at(name);if(account.is_string()){need(store!=nullptr,"Attach the account's durable store");account=store->get(account.get<std::string>());}need(account["selection"]["source_binding"]==source_id_,"Account source binding differs");
        if(op=="SB_READOUT") return account.at("readout");
        need(store!=nullptr,"Attach the account's durable store"); std::vector<json> chunks; std::string id=account.at("history_head"); std::set<std::string> seen;
        while(!id.empty()) { need(seen.insert(id).second,"Cycle in stored history chain"); auto chunk=store->get(id); need(chunk.at("schema")=="SB_GEN3_RXT_HISTORY_CHUNK_V1"&&chunk.at("source_binding")==source_id_&&chunk.at("account")==name,"History chunk source differs"); id=chunk["previous"].is_null()?"":chunk["previous"].get<std::string>(); chunks.push_back(std::move(chunk)); }
        json out={{"quantity",account["readout"]["quantity"]},{"source_binding",account["selection"]},{"points",json::array()},{"edges",json::array()}};
        for(auto i=chunks.rbegin();i!=chunks.rend();++i) { for(const auto& point:i->at("points")) out["points"].push_back(point); for(const auto& edge:i->at("edges")) out["edges"].push_back(edge); }
        need(out["points"].size()==account["readout"]["point_count"]&&out["edges"].size()==account["readout"]["edge_count"],"Stored history cardinality differs"); return out;
    }
    if(op=="SB_J4_BATCH") return accumulate(p,state,store);
    if(op=="SB_J4_ACCUMULATE") { json q=p; std::string b=q.value("backend",std::string("auto")); q.erase("backend"); auto result=accumulate({{"requests",json::array({q})},{"backend",b}},state,store); json answer=result["results"][0]; answer["execution"]=result["execution"]; return answer; }
    throw std::invalid_argument("Unknown native Starbreaker operation: "+op);
}
}
