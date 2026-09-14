#include "engine.hpp"
#include "knowledge.hpp"
#include "core_binding.hpp"
#include <algorithm>
#include <chrono>
#include <set>

namespace rxt {
namespace {
void need(bool ok,const std::string& text){if(!ok)throw std::invalid_argument("Core memory: "+text);}
void fields(const json& p,const std::set<std::string>& keys){for(auto i=p.begin();i!=p.end();++i)need(keys.count(i.key()),"Unknown field: "+i.key());}
std::string key(const Contract& c,uint32_t q,size_t e){return c.id+":"+std::to_string(q)+":"+std::to_string(e);}
json node_result(const std::string& name,const std::string& id,const json& node){
    json result={{"memory",name},{"node",id}};
    for(auto k:{"candidate_count","choice","selected_label","maximizing_labels","members","target","target_resolved","transcript"})if(node.contains(k))result[k]=node[k];
    return result;
}
}
Trace Engine::learned_run(const Batch& b,json& next,uint64_t& reused,uint64_t& acquired){
    const auto& c=contract();auto start=std::chrono::steady_clock::now();Trace t;t.count=b.count;t.steps=b.steps;
    t.states.resize(b.count*(b.steps+1));t.actions.resize(t.states.size());t.backend="NATIVE_LEARNED_RELATIONS_AND_T18";t.cpu_workers=1;
    std::copy(b.initial.begin(),b.initial.end(),t.states.begin());
    for(size_t step=0;step<=b.steps;++step)for(size_t lane=0;lane<b.count;++lane){
        size_t at=step*b.count+lane;uint32_t before=t.states[at];auto index=c.tables.index[before];need(index>=0,"State outside current source");
        t.actions[at]=c.tables.contacts[index];if(step==b.steps)continue;
        size_t e=b.events[at];need(c.tables.admitted[e*c.tables.addresses.size()+index],"Event is not admitted at this state");
        auto k=key(c,before,e);uint32_t after;
        if(next["knowledge"].contains(k)){
            const auto& r=next["knowledge"][k];need(r["from"]==before&&r["event"]==c.labels[e],"Learned source identity differs");
            after=r.at("to").get<uint32_t>();need(after<ADDRESS_COUNT&&c.tables.index[after]>=0,"Learned target is outside source");++reused;
        }else{
            // Exact packed T18 Write is the acquisition kernel for missing support.
            auto ev=c.tables.events[e];int coordinate=ev.coordinate;
            int phase=(int((before>>coordinate)&1u)+2*int((before>>(coordinate+9))&1u)+ev.direction+4)%4;
            after=before&~((1u<<coordinate)|(1u<<(coordinate+9)));
            after|=(uint32_t(phase&1)<<coordinate)|(uint32_t(phase>>1)<<(coordinate+9));
            need(c.tables.index[after]>=0,"Source Write leaves admitted domain");
            next["knowledge"][k]={{"from",before},{"event",c.labels[e]},{"to",after}};++acquired;
        }
        t.states[at+b.count]=after;
    }
    t.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();return t;
}
json Engine::core(const std::string& op,const json& p){
    need(bool(store_),"Attach a durable store first");
    auto commit=[&](json next,json result){
        next["sequence"]=state_["sequence"].get<uint64_t>()+1;
        json record={{"previous",state_.value("core_log_head",json(nullptr))},{"op",op},{"payload",p},{"result",result}};
        next["core_log_head"]=store_->put(record);auto root=store_->commit(next);state_=std::move(next);
        result["checkpoint"]={{"root",root},{"sequence",state_["sequence"]}};return result;
    };
    if(op=="GEN3_CORE_STATUS"){
        fields(p,{});return {{"version",VERSION},{"installed",state_.contains("core_memory")},{"source",state_.value("core_memory",json(nullptr))},
            {"execution_statistics",state_.value("core_statistics",json::object())},{"encounters",state_.value("core_encounters",json::object()).size()},
            {"compositions",state_.value("core_compositions",json::object()).size()},{"learning","NATIVE_ACQUIRE_REUSE_AND_CHECKPOINT"}};
    }
    if(op=="GEN3_CORE_SYNC"){
        fields(p,{"directory"});auto dir=std::filesystem::absolute(p.at("directory").get<std::string>());
        need(file_sha256(dir/"MANIFEST.json")==CORE_MANIFEST_SHA,"Installed workstation seed manifest differs");
        if(state_.contains("core_memory")){need(state_["core_memory"]["manifest_sha256"]==CORE_MANIFEST_SHA,"Already acquired another core release");return core("GEN3_CORE_STATUS",json::object());}
        json manifest=read_json(dir/"MANIFEST.json"),packages=json::object(),refs=json::object(),counts=json::object();
        for(auto i=manifest.at("files").begin();i!=manifest["files"].end();++i){
            need(i.key().find('/')==std::string::npos&&i.key().find("..") == std::string::npos,"Invalid package path");
            need(file_sha256(dir/i.key())==i.value().at("sha256").get<std::string>(),"Package checksum differs: "+i.key());
            std::string name=std::filesystem::path(i.key()).stem();auto value=read_json(dir/i.key());
            auto memory=value.value("memory",value);
            if(memory.contains("nodes"))for(auto n=memory["nodes"].begin();n!=memory["nodes"].end();++n){
                std::set<std::string> observations;
                for(const auto& branch:n.value().at("branches")){
                    need(memory["nodes"].contains(branch.at("target").get<std::string>()),"Branch destination missing");
                    need(observations.insert(branch.at("observation").dump()).second,"Ambiguous acquired observation");
                }
            }
            counts[name]={{"nodes",memory.value("nodes",json::object()).size()},{"tasks",memory.value("tasks",json::object()).size()}};
            refs[name]=store_->put(value);packages[name]=std::move(value);
        }
        Contract c(packages.at("observations").at("contract"),resources_);auto next=state_;uint64_t imported=0;
        const auto& transitions=packages.at("relations").at("knowledge").at("transitions");
        for(const auto& row:transitions){
            need(row.at("contract_id")==manifest.at("relation_import").at("source_contract_id"),"Original relation source differs");
            Batch batch=c.batch({{"initial",json::array({row.at("from")})},{"programs",json::array({json::array({row.at("event")})})}});
            auto result=run_cpu(c.tables,batch,1);auto before=result.states[0],after=result.states[1];
            need(c.decode(after)==row.at("to")&&result.actions[0]==row.at("action_before")&&result.actions[1]==row.at("action_after"),"Imported relation fails native source admission");
            auto k=key(c,before,batch.events[0]);json relation={{"from",before},{"event",row.at("event")},{"to",after}};
            need(!next["knowledge"].contains(k)||next["knowledge"][k]==relation,"Existing relation conflicts with import");next["knowledge"][k]=relation;++imported;
        }
        need(imported==192,"Core relation count differs");
        next["core_memory"]={{"manifest_sha256",CORE_MANIFEST_SHA},{"packages",refs},{"package_counts",counts},
            {"relations_admitted",imported},{"basis","SLC-GEN3-R3"},{"source_contract_id",manifest["relation_import"]["source_contract_id"]},{"native_contract_id",c.id}};
        next["core_statistics"]={{"imported_relations",imported},{"learned_events_executed",0},{"native_events_acquired",0},{"observation_branches_executed",0}};
        next["core_encounters"]=json::object();next["core_compositions"]=json::object();
        return commit(std::move(next),{{"status","ACQUIRED_AND_NATIVE_ADMITTED"},{"relations",imported},{"packages",counts},{"source",c.describe()}});
    }
    need(state_.contains("core_memory"),"Synchronize installed core seeds first");
    auto memory=[&](const std::string& name){auto package=store_->get(state_.at("core_memory").at("packages").at(name).get<std::string>());return package.value("memory",package);};
    if(op=="GEN3_MEMORY_PACKAGE"){
        fields(p,{"memory"});auto name=p.at("memory").get<std::string>();return {{"memory",name},{"package",store_->get(state_["core_memory"]["packages"].at(name).get<std::string>())},{"source_manifest_sha256",CORE_MANIFEST_SHA}};
    }
    if(op=="GEN3_MEMORY_NODE"||op=="GEN3_MEMORY_START"){
        fields(p,op=="GEN3_MEMORY_START"?std::set<std::string>{"memory","node","encounter"}:std::set<std::string>{"memory","node"});
        auto name=p.at("memory").get<std::string>();auto m=memory(name);json chosen=p.value("node",m.value("root",json(nullptr)));
        need(chosen.is_string()&&m.at("nodes").contains(chosen.get<std::string>()),"Supply an acquired node in this scoped memory");
        auto id=chosen.get<std::string>();auto result=node_result(name,id,m["nodes"][id]);if(op=="GEN3_MEMORY_NODE")return result;
        auto encounter=p.at("encounter").get<std::string>();need(!encounter.empty()&&!state_["core_encounters"].contains(encounter),"Use a new nonempty encounter identity");
        auto next=state_;next["core_encounters"][encounter]={{"memory",name},{"node",id},{"actual_reports",json::array()}};result["encounter"]=encounter;return commit(std::move(next),result);
    }
    need(op=="GEN3_MEMORY_APPLY","Unknown native core operation");fields(p,{"encounter","observation","evidence"});
    need(p.size()==3&&!p.at("evidence").is_null()&&!p.at("evidence").empty()&&p.at("evidence")!=false,"Actual observation and explicit source evidence required");
    auto encounter=p.at("encounter").get<std::string>();auto item=state_.at("core_encounters").at(encounter);auto name=item.at("memory").get<std::string>();auto m=memory(name);
    auto id=item.at("node").get<std::string>();const auto& node=m.at("nodes").at(id);json match;
    for(const auto& branch:node.at("branches"))if(branch.at("observation").dump()==p.at("observation").dump()){need(match.is_null(),"Ambiguous observation branch");match=branch;}
    if(match.is_null()){auto result=node_result(name,id,node);result["status"]="OUTSIDE_ACQUIRED_BRANCH_SUPPORT";result["encounter"]=encounter;result["actual_observation"]=p.at("observation");return result;}
    auto target=match.at("target").get<std::string>();item["actual_reports"].push_back({{"from",id},{"to",target},{"choice",node.value("choice",json(nullptr))},{"observation",p["observation"]},{"evidence",p["evidence"]}});item["node"]=target;
    auto next=state_;next["core_encounters"][encounter]=item;next["core_statistics"]["observation_branches_executed"]=next["core_statistics"]["observation_branches_executed"].get<uint64_t>()+1;
    auto result=node_result(name,target,m["nodes"][target]);result["status"]="APPLIED_ACTUAL_REPORT";result["encounter"]=encounter;return commit(std::move(next),result);
}
}
