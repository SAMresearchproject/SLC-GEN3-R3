#include "engine.hpp"
#include "starbreaker.hpp"
#include "core_binding.hpp"
#include "horizon_binding.hpp"
#include <chrono>
#include <set>

namespace rxt {
namespace {
void need(bool b,const std::string& s){if(!b)throw std::invalid_argument("Native campaign: "+s);}
uint64_t epoch(){return uint64_t(std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count());}
std::string padded(uint64_t n){auto s=std::to_string(n);return std::string(8-s.size(),'0')+s;}
}
json Engine::campaign(const std::string& op,const json& p){
    need(bool(store_)&&bool(starbreaker_)&&state_.contains("horizon_source")&&state_.contains("core_memory")&&state_.contains("training_source"),"Load all native sources before opening the campaign");
    auto name=p.at("campaign_id").get<std::string>();need(!name.empty()&&name.size()<=48,"Use a campaign ID of 1..48 bytes");
    if(op=="CAMPAIGN_OPEN"){
        const auto& plan=p.at("plan");auto start=plan.at("start_ordinal").get<uint64_t>(),limit=plan.at("family_limit").get<uint64_t>(),duration=plan.at("duration_seconds").get<uint64_t>();
        need(start>=541568&&start<4800000&&limit>0&&limit<=4800000-start,"New construction range outside source inventory");need(duration>=60&&duration<=604800,"Duration outside 1 minute..7 days");
        auto width=plan.at("batch_families").get<uint64_t>();need(plan.at("pool_families")==4096&&(width==256||width==512||width==640),"Native pipeline uses pools of 4096 and CUDA batches of 256, 512 or 640");
        auto sb=plan.at("sb_cases_per_pool").get<size_t>(),h=plan.at("horizon_cases_per_pool").get<size_t>();need(sb>0&&sb<=256&&h>0&&h<=256,"Source case count outside native batch limits");
        auto id=hash(plan.dump());if(state_.contains("campaigns")&&state_["campaigns"].contains(name)){auto c=state_["campaigns"][name];need(c["plan_sha256"]==id,"Campaign ID has another plan");return c;}
        json row={{"campaign_id",name},{"plan",plan},{"plan_sha256",id},{"basis_core_manifest_sha256",CORE_MANIFEST_SHA},{"horizon_bundle_sha256",HORIZON_BUNDLE_SHA},
            {"status","READY"},{"created_at_unix",epoch()},{"completed_pools",0},{"new_construction_families",0},{"sb_histories",0},{"horizon_cases",0},{"horizon_event_receipts",0},{"formed_horizons",0},{"native_lessons",0},{"model_promotions",0},{"gpu_construction_seconds",0.0}};
        auto next=state_;next["campaigns"][name]=row;store_->commit(next);state_=std::move(next);return row;
    }
    need(state_.contains("campaigns")&&state_["campaigns"].contains(name),"Open the campaign first");auto c=state_["campaigns"][name];
    if(op=="CAMPAIGN_STATUS")return c;need(op=="CAMPAIGN_STEP","Unknown campaign operation");const auto& plan=c.at("plan");
    if(c["new_construction_families"].get<uint64_t>()>=plan["family_limit"].get<uint64_t>()||epoch()-c["created_at_unix"].get<uint64_t>()>=plan["duration_seconds"].get<uint64_t>()){
        c["status"]="COMPLETE";auto next=state_;next["campaigns"][name]=c;store_->commit(next);state_=std::move(next);return c;
    }
    auto pool=c["completed_pools"].get<uint64_t>(),cursor=c["new_construction_families"].get<uint64_t>();auto prefix=name+"."+padded(pool);auto started=epoch();
    auto run=[&](const std::string& phase,const std::string& operation,json payload){
        std::string key=prefix+"."+phase;
        if(state_.contains("campaign_stages")&&state_["campaign_stages"].contains(key))return store_->get(state_["campaign_stages"][key].get<std::string>());
        auto next=state_;next["campaigns"][name]["phase"]=phase;next["campaigns"][name]["status"]="RUNNING";store_->commit(next);state_=std::move(next);
        if(operation=="SB_J4_BATCH"||operation=="SB_HORIZON_SWEEP")payload["batch_id"]=key;
        auto result=execute({{"op",operation},{"payload",payload}});result.erase("checkpoint");auto ref=store_->put(result);
        next=state_;next["campaign_stages"][key]=ref;next["campaign_log_head"]=store_->put({{"previous",state_.value("campaign_log_head",json(nullptr))},{"campaign_id",name},{"stage",key},{"operation",operation},{"payload",payload},{"result",ref},{"execution_engine",VERSION}});store_->commit(next);state_=std::move(next);return result;
    };
    auto sb_count=plan["sb_cases_per_pool"].get<size_t>();auto requests=starbreaker_->campaign_requests(pool*sb_count,sb_count,prefix+".SB");
    auto sb=run("STARBREAKER","SB_J4_BATCH",{{"requests",requests},{"backend","cuda"}});
    auto count=std::min<uint64_t>(4096,plan["family_limit"].get<uint64_t>()-cursor),first=plan["start_ordinal"].get<uint64_t>()+cursor;json families=json::array();
    for(uint64_t i=0;i<count;++i)families.push_back(((first+i)*15485863+1060912)%4800000);
    bool feedback_rank=state_.contains("domain_transfer") && state_["domain_transfer"].contains("models");
    if(feedback_rank)families=transfer("GEN3_TRANSFER_PLAN",{{"family_ids",families},{"sb_count",0}})["family_ids"];
    std::string target=(pool%4==0)?"shared_four_state_orbit":starbreaker_->target_names().at(size_t(pool%45));
    auto job=prefix+".A3D";run("SUBMIT","JOINT_SUBMIT",{{"job_id",job},{"family_ids",families},{"source_contract","A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1"},{"targets",json::array({target})},{"ranking",feedback_rank?"NONE":pool%2?"POLICY":"NONE"},{"backend","cuda"}});
    auto width=p.value("batch_families",plan["batch_families"].get<uint64_t>());need(width==256||width==512||width==640,"Execution batch width outside the native pod profile");auto a3=run("CONSTRUCTION","JOINT_DRAIN",{{"job_id",job},{"max_families",width},{"max_batches",(count+width-1)/width}});need(a3.at("status")=="COMPLETE","Construction pool did not finish");c["execution_batch_families"]=width;
    auto h_count=plan["horizon_cases_per_pool"].get<size_t>();json hp={{"start",pool*h_count},{"count",h_count}};
    if(pool%2){hp["family_id"]=families[0];hp["starbreaker_account"]=requests[0]["account"];}
    auto horizon_result=run("HORIZON","SB_HORIZON_SWEEP",hp);
    auto learned=run("INGEST","TRAIN_INGEST",{{"job_id",job}});
    json sample=json::array(),accounts=json::array();
    for(size_t i=0;i<families.size();i+=64)sample.push_back(families[i]);
    for(const auto& request:requests)accounts.push_back(request["account"]);
    run("TRANSFER_OBSERVE","GEN3_TRANSFER_OBSERVE",{{"family_ids",sample},{"accounts",accounts}});
    if(pool%8==0)run("TRANSFER_FIT","GEN3_TRANSFER_FIT",json::object());
    c["domain_feedback"]={{"revision","R7"},{"learned_ranking",feedback_rank},{"observed_families",sample.size()},{"observed_SB_accounts",accounts.size()}};
    int config=starbreaker_->policy().at("models").at(target).at("model").at("config").at("index");
    bool deferred=plan.value("defer_fit",false);auto fit=deferred?json{{"status","DEFERRED_TO_REVIEW"},{"promoted",false},{"wall_seconds",0},{"development",nullptr}}:run("TRAIN","TRAIN_FIT",{{"index",config}});
    c["completed_pools"]=pool+1;c["new_construction_families"]=cursor+count;c["sb_histories"]=c["sb_histories"].get<uint64_t>()+sb_count;c["horizon_cases"]=c["horizon_cases"].get<uint64_t>()+h_count;
    c["horizon_event_receipts"]=c["horizon_event_receipts"].get<uint64_t>()+horizon_result["event_receipts"].get<uint64_t>();c["formed_horizons"]=c["formed_horizons"].get<uint64_t>()+horizon_result["formed_horizons"].get<uint64_t>();
    c["native_lessons"]=c["native_lessons"].get<uint64_t>()+uint64_t(!deferred);c["model_promotions"]=c["model_promotions"].get<uint64_t>()+uint64_t(fit["promoted"].get<bool>());c["gpu_construction_seconds"]=c["gpu_construction_seconds"].get<double>()+a3["gpu_kernel_seconds"].get<double>();
    c["last_pool"]={{"kind",pool%2?"STARBREAKER_A3D41_COUPLED":"A3D41_SOURCE_ORDER"},{"training_target",target},{"native_fit_seconds",fit["wall_seconds"]},{"development",fit["development"]},{"pool_wall_seconds",epoch()-started},{"dataset",learned.value("dataset",json(nullptr))}};
    c["phase"]="POOL_COMPLETE";c["status"]="RUNNING";auto next=state_;next["campaigns"][name]=c;auto root=store_->commit(next);state_=std::move(next);c["checkpoint"]={{"root",root}};return c;
}
}
