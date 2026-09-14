#include "engine.hpp"
#include "atom3d.hpp"
#include "starbreaker.hpp"
#include "knowledge.hpp"
#include "joint_binding.hpp"
#include <algorithm>
#include <chrono>
#include <set>

namespace rxt {
namespace {
void need(bool b,const std::string& s){if(!b)throw std::invalid_argument("Joint engine: "+s);}
void fields(const json& p,const std::set<std::string>& allowed){for(auto i=p.begin();i!=p.end();++i)need(allowed.contains(i.key()),"Unknown field: "+i.key());}
uint32_t id(const json& value){need(value.is_number_integer()&&!value.is_boolean()&&value.get<int64_t>()>=0&&value.get<int64_t>()<4800000,"Family ID must be in 0..4799999");return value.get<uint32_t>();}
std::string outcome_key(const json& binding,uint32_t family){return "A3D41_OUTCOME:"+binding.at("source_sha256").get<std::string>()+":"+std::to_string(family);}
std::string set_key(const json& binding,const std::string& digest){return "A3D41_SET:"+binding.at("source_sha256").get<std::string>()+":"+digest;}
json summary(const json& job){return {{"job_id",job.at("job_id")},{"status",job.at("cursor")==job.at("family_count")?"COMPLETE":"QUEUED"},{"completed_families",job.at("cursor")},{"family_count",job.at("family_count")},{"backend",job.at("backend")},{"completed_batches",job.at("batches").size()},{"reused_acquired",job.at("reused_acquired")},{"reused_native",job.at("reused_native")},{"newly_computed",job.at("newly_computed")},{"request_sha256",job.at("request_sha256")},{"proposal_object",job.at("proposal_object")}};}
json minimum_record(const std::string& digest,const std::string& bits){static constexpr char hex[]="0123456789abcdef";std::string encoded(bits.size()*2,'0');for(size_t i=0;i<bits.size();++i){auto b=uint8_t(bits[i]);encoded[2*i]=hex[b>>4];encoded[2*i+1]=hex[b&15];}return {{"sha256",digest},{"bits_hex",encoded}};}
}

json Engine::joint(const std::string& op,const json& p){
    need(bool(store_),"Attach a durable store first");
    auto commit=[&](json next,const json& result){
        json record={{"schema","GEN3_RXT_JOINT_EVENT_V1"},{"previous",state_.value("joint_log_head",json(nullptr))},{"operation",op},{"request",p},{"result",result}};
        next["joint_log_head"]=store_->put(record);next["sequence"]=state_["sequence"].get<uint64_t>()+1;
        auto root=store_->commit(next);state_=std::move(next);auto out=result;out["checkpoint"]={{"root",root},{"sequence",state_["sequence"]},{"status","COMMITTED"}};return out;
    };
    if(op=="JOINT_COMPILE"){
        fields(p,{"directory"});auto directory=std::filesystem::absolute(p.at("directory").get<std::string>());
        need(file_sha256(directory/"BUNDLE.json")==JOINT_BUNDLE_SHA,"Joint source bundle differs");
        json binding={{"directory",directory.string()},{"bundle_sha256",JOINT_BUNDLE_SHA},{"version",VERSION}};
        if(state_.contains("joint_binding")){need(state_["joint_binding"]["bundle_sha256"]==binding["bundle_sha256"],"Use a separate store for another joint source");return joint("JOINT_STATUS",json::object());}
        need(!atom3d_&&!starbreaker_,"Compile both domains together into a fresh joint store");
        auto bundle=read_json(directory/"BUNDLE.json");
        for(auto name:{"atom3d","starbreaker","learning"})need(file_sha256(directory/name/"BUNDLE.json")==bundle["sources"][name].get<std::string>(),"Domain source differs: "+std::string(name));
        auto atom=std::make_unique<Atom3d>(directory/"atom3d",resources_);auto sb=std::make_unique<Starbreaker>(directory/"starbreaker",resources_);
        auto memory=std::make_unique<ConstructionKnowledge>(directory/"learning",bundle["sources"]["learning"].get<std::string>(),resources_);
        need(memory->binding()["source_domain_sha256"]==atom->binding()["source_sha256"],"Acquired observations use another domain");
        need(memory->binding()["policy_sha256"]==sb->binding()["policy_sha256"],"Acquired policy and observation library differ");
        json next=state_;next["joint_binding"]=binding;next["atom3d"]=atom->binding();next["starbreaker"]=sb->binding();next["construction_memory"]=memory->binding();next["sb_policy_object"]=store_->put(sb->policy());next["sb_accounts"]=json::object();next["joint_jobs"]=json::object();next["joint_order"]=json::array();next["joint_observed_families"]=0;
        auto result=commit(std::move(next),{{"status","COMPILED"},{"binding",binding},{"memory",memory->status()}});
        atom3d_=std::move(atom);starbreaker_=std::move(sb);construction_memory_=std::move(memory);return result;
    }
    need(bool(atom3d_)&&bool(starbreaker_)&&bool(construction_memory_),"Compile the joint A3D41/Starbreaker source first");
    if(op=="JOINT_STATUS"||op=="ATOM3D_KNOWLEDGE"){
        fields(p,{});json jobs=json::array();uint64_t pending=0;
        for(const auto& name:state_["joint_order"]){auto job=store_->get(state_["joint_jobs"][name.get<std::string>()].get<std::string>());jobs.push_back(summary(job));pending+=job["family_count"].get<uint64_t>()-job["cursor"].get<uint64_t>();}
        return {{"version",VERSION},{"binding",state_["joint_binding"]},{"status",pending?"READY_PENDING_WORK":"IDLE"},{"atom3d",atom3d_->status()},{"starbreaker",starbreaker_->status()},{"construction_memory",construction_memory_->status()},{"shared_resources",resources_.describe()},{"scheduling","ONE_PROCESS_ONE_QUEUE_ONE_ACTIVE_GPU_BATCH"},{"training_state",state_.value("training_state",std::string("READY_FOR_NATIVE_TRAINING"))},{"pending_families",pending},{"observed_family_deliveries",state_["joint_observed_families"]},{"jobs",jobs},{"operations",{"JOINT_STATUS","JOINT_SUBMIT","JOINT_STEP","JOINT_RESULT","ATOM3D_KNOWLEDGE","ATOM3D_CONSTRUCTION_POLICY","ATOM3D_CONSTRUCTION_RESULT","SB_CONSTRUCTION_RESULT","ATOM3D_CONSTRUCTION_MINIMUM_SET"}}};
    }
    if(op=="ATOM3D_CONSTRUCTION_POLICY")return starbreaker_->execute("SB_CONSTRUCTION_POLICY",p,state_,store_.get());
    if(op=="ATOM3D_CONSTRUCTION_RESULT"||op=="SB_CONSTRUCTION_RESULT"){
        fields(p,{"family_id"});auto family=id(p.at("family_id"));auto outcome=construction_memory_->contains(family)?construction_memory_->outcome(family):store_->recall(outcome_key(atom3d_->binding(),family));
        if(outcome.is_null())return {{"status","UNCOMPUTED"},{"family_id",family},{"source",atom3d_->binding()}};
        return {{"status","EXACT_OUTCOME"},{"outcome",outcome},{"observed_targets",construction_memory_->labels(outcome,starbreaker_->policy())}};
    }
    if(op=="ATOM3D_CONSTRUCTION_MINIMUM_SET"){
        fields(p,{"sha256"});auto digest=p.at("sha256").get<std::string>();need(digest.size()==64&&digest.find_first_not_of("0123456789abcdef")==std::string::npos,"Invalid minimum-set SHA");auto cached=store_->recall(set_key(atom3d_->binding(),digest));
        if(!cached.is_null())return cached;return minimum_record(digest,construction_memory_->bits(digest));
    }
    if(op=="JOINT_SUBMIT"){
        fields(p,{"job_id","family_ids","source_contract","targets","backend","ranking"});auto name=p.at("job_id").get<std::string>();need(!name.empty()&&name.size()<=128,"Use a job name of 1..128 bytes");
        std::string backend=p.value("backend",std::string("cuda"));need(backend=="cpu"||backend=="cuda","Choose cpu or cuda backend");
        json request=p;request["backend"]=backend;request["targets"]=p.value("targets",json::array({"shared_four_state_orbit","channel_minimum_sets_agree"}));auto request_sha=hash(request.dump());
        if(state_["joint_jobs"].contains(name)){auto job=store_->get(state_["joint_jobs"][name].get<std::string>());need(job.at("request_sha256")==request_sha,"Job name already belongs to a different request");auto result=summary(job);result["idempotent_replay"]=true;return result;}
        auto ranking=request.value("ranking",std::string("POLICY"));need(ranking=="POLICY"||ranking=="NONE","Unknown candidate ranking mode");
        auto policy_request=request;policy_request.erase("job_id");policy_request.erase("ranking");json proposals;
        if(ranking=="POLICY")proposals=starbreaker_->execute("SB_CONSTRUCTION_POLICY",policy_request,state_,store_.get());
        else{need(p.at("source_contract")=="A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1","Construction source differs");const auto& input=p.at("family_ids");need(input.is_array()&&!input.empty()&&input.size()<=4096,"Admit 1..4096 source families");std::set<uint32_t> seen;json rows=json::array();for(const auto& raw:input){auto f=id(raw);need(seen.insert(f).second,"Repeated family ID");rows.push_back({{"family_id",f},{"predictions",json::object()}});}proposals={{"rows",rows},{"ranked_tie_groups",json::array({{{"family_ids",input},{"probabilities",json::object()}}})},{"ranking","SOURCE_ORDER_NO_POLICY"}};}
        json order=json::array();for(const auto& group:proposals["ranked_tie_groups"])for(const auto& family:group["family_ids"])order.push_back(family);
        need(order.size()==request.at("family_ids").size(),"All score ties must remain in the queue");
        json job={{"schema","GEN3_RXT_JOINT_JOB_V1"},{"job_id",name},{"request_sha256",request_sha},{"request_object",store_->put(request)},{"proposal_object",store_->put(proposals)},{"order",order},{"cursor",0},{"family_count",order.size()},{"backend",backend},{"batches",json::array()},{"reused_acquired",0},{"reused_native",0},{"newly_computed",0}};
        auto next=state_;next["joint_jobs"][name]=store_->put(job);next["joint_order"].push_back(name);auto result=summary(job);result["ranked_tie_groups"]=proposals["ranked_tie_groups"];result["all_ties_retained"]=true;return commit(std::move(next),result);
    }
    if(op=="JOINT_RESULT"){
        fields(p,{"job_id","include_feedback"});auto name=p.at("job_id").get<std::string>();auto job=store_->get(state_["joint_jobs"].at(name).get<std::string>());auto result=summary(job);result["batch_objects"]=job["batches"];
        if(p.value("include_feedback",false)){result["feedback"]=json::array();for(const auto& ref:job["batches"]){auto batch=store_->get(ref.get<std::string>());for(const auto& row:batch["rows"])result["feedback"].push_back(row);}}
        return result;
    }
    if(op=="JOINT_DRAIN"){
        fields(p,{"job_id","max_families","max_batches"});need(joint_drain_remaining_==0&&!joint_prefetch_.valid(),"Another native drain is active");
        auto batches=p.value("max_batches",uint64_t(16));need(batches>0&&batches<=4096,"Drain admits 1..4096 batches");auto begin=std::chrono::steady_clock::now();json summaries=json::array(),last;double gpu_seconds=0;uint64_t fresh=0;
        try{for(joint_drain_remaining_=batches;joint_drain_remaining_>0;--joint_drain_remaining_){json request=p;request.erase("max_batches");last=joint("JOINT_STEP",request);if(last.contains("batch")){const auto& b=last["batch"];gpu_seconds+=b["execution"]["gpu_kernel_seconds"].get<double>();fresh+=b["newly_computed"].get<uint64_t>();}auto brief=last;brief.erase("batch");summaries.push_back(brief);if(last.value("status",std::string())=="COMPLETE"||last.value("status",std::string())=="IDLE")break;}
            joint_drain_remaining_=0;need(!joint_prefetch_.valid(),"Unconsumed native simulation prefetch");
        }catch(...){joint_drain_remaining_=0;if(joint_prefetch_.valid()){try{joint_prefetch_.get();}catch(...){}}joint_prefetch_ids_=nullptr;throw;}
        auto result=last;result.erase("batch");result["batches"]=summaries;result["newly_computed_this_drain"]=fresh;result["gpu_kernel_seconds"]=gpu_seconds;result["drain_wall_seconds"]=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();result["pipeline"]="NEXT_NATIVE_CUDA_BATCH_OVERLAPS_CURRENT_CUSTODY";return result;
    }
    need(op=="JOINT_STEP","Unknown joint operation: "+op);fields(p,{"job_id","max_families"});
    std::string name=p.value("job_id",std::string());
    if(name.empty())for(const auto& entry:state_["joint_order"]){auto job=store_->get(state_["joint_jobs"][entry.get<std::string>()].get<std::string>());if(job["cursor"]!=job["family_count"]){name=entry.get<std::string>();break;}}
    if(name.empty())return {{"status","IDLE"},{"completed_families",0}};
    auto job=store_->get(state_["joint_jobs"].at(name).get<std::string>());auto backend=job.at("backend").get<std::string>();
    auto limit=p.value("max_families",json(backend=="cuda"?256:8));need(limit.is_number_integer()&&!limit.is_boolean()&&limit.get<int64_t>()>0&&limit.get<int64_t>()<=(backend=="cuda"?640:8),"Batch exceeds the selected backend limit");
    auto begin=std::chrono::steady_clock::now();size_t cursor=job["cursor"].get<size_t>(),end=std::min(cursor+limit.get<size_t>(),job["order"].size());
    if(cursor==end)return summary(job);
    auto proposal_id=job["proposal_object"].get<std::string>();
    if(joint_prediction_object_!=proposal_id){auto proposals=store_->get(proposal_id);joint_predictions_.clear();for(const auto& row:proposals["rows"])joint_predictions_[row["family_id"].get<uint32_t>()]=row["predictions"];joint_prediction_object_=proposal_id;}
    const auto& predictions=joint_predictions_;
    std::map<uint32_t,json> outcomes;json fresh=json::array();uint64_t acquired=0,cached=0;
    for(size_t i=cursor;i<end;++i){auto family=job["order"][i].get<uint32_t>();if(construction_memory_->contains(family)){outcomes[family]=construction_memory_->outcome(family);++acquired;}else{auto found=store_->recall(outcome_key(atom3d_->binding(),family));if(found.is_null())fresh.push_back(family);else{outcomes[family]=std::move(found);++cached;}}}
    json execution={{"backend",backend},{"gpu_kernel_seconds",0},{"gpu_batch_wall_seconds",0},{"exact_contexts",0}};
    if(!fresh.empty()){
        json result;if(joint_prefetch_.valid()){need(joint_prefetch_ids_==fresh,"Prefetched family identities differ");result=joint_prefetch_.get();joint_prefetch_ids_=nullptr;}else result=atom3d_->execute("ATOM3D_CONSTRUCTION_IDS",{{"family_ids",fresh},{"backend",backend}});
        if(joint_drain_remaining_>1&&end<job["order"].size()){
            json next_ids=json::array();auto next_end=std::min(end+limit.get<size_t>(),job["order"].size());for(size_t i=end;i<next_end;++i){auto f=job["order"][i].get<uint32_t>();if(!construction_memory_->contains(f)&&store_->recall(outcome_key(atom3d_->binding(),f)).is_null())next_ids.push_back(f);}
            if(!next_ids.empty()){joint_prefetch_ids_=next_ids;joint_prefetch_=std::async(std::launch::async,[this,next_ids,backend]{return atom3d_->execute("ATOM3D_CONSTRUCTION_IDS",{{"family_ids",next_ids},{"backend",backend}});});}
        }
        for(auto i=result["complete_minimum_sets"].begin();i!=result["complete_minimum_sets"].end();++i){auto key=set_key(atom3d_->binding(),i.key());if(!joint_saved_sets_.contains(key)){store_->remember(key,i.value());joint_saved_sets_.insert(key);}}
        for(const auto& row:result["rows"]){auto family=row["family_id"].get<uint32_t>();store_->remember(outcome_key(atom3d_->binding(),family),row);outcomes[family]=row;}
        for(auto key:{"gpu_kernel_seconds","gpu_batch_wall_seconds","exact_contexts","wall_seconds"})execution[key]=result[key];
    }
    json feedback=json::array();
    for(size_t i=cursor;i<end;++i){auto family=job["order"][i].get<uint32_t>();const auto& outcome=outcomes.at(family);auto labels=construction_memory_->labels(outcome,starbreaker_->policy());json matches=json::object();
        for(auto target=predictions.at(family).begin();target!=predictions.at(family).end();++target)matches[target.key()]=((rational(target.value()["probability"])>=mpq_class(1,2))==labels.at(target.key()).get<bool>());
        json ref=outcome["origin"]=="ACQUIRED_SIMULATION"?json{{"memory_bundle_sha256",outcome["memory_bundle_sha256"]},{"ordinal",outcome["source_ordinal"]}}:json{{"object",hash(outcome.dump())}};
        feedback.push_back({{"family_id",family},{"origin",outcome["origin"]},{"outcome",ref},{"observed_targets",labels},{"predictions",predictions.at(family)},{"prediction_matches",matches}});
    }
    json batch={{"schema","GEN3_RXT_JOINT_FEEDBACK_V1"},{"job_id",name},{"cursor_begin",cursor},{"cursor_end",end},{"reused_acquired",acquired},{"reused_native",cached},{"newly_computed",fresh.size()},{"rows",feedback},{"execution",execution},{"wall_seconds",std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()},{"source_binding",state_["joint_binding"]},{"policy_updated",false},{"training_state",state_.value("training_state",std::string("READY_FOR_NATIVE_TRAINING"))}};
    auto ref=store_->put(batch);job["batches"].push_back(ref);job["cursor"]=end;
    job["reused_acquired"]=job["reused_acquired"].get<uint64_t>()+acquired;job["reused_native"]=job["reused_native"].get<uint64_t>()+cached;job["newly_computed"]=job["newly_computed"].get<uint64_t>()+fresh.size();
    auto next=state_;next["joint_jobs"][name]=store_->put(job);next["joint_observed_families"]=state_["joint_observed_families"].get<uint64_t>()+end-cursor;auto result=summary(job);result["batch_object"]=ref;result["batch"]=batch;return commit(std::move(next),result);
}
}
