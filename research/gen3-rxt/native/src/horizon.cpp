#include "engine.hpp"
#include "knowledge.hpp"
#include "starbreaker.hpp"
#include "horizon_binding.hpp"
#include <map>
#include <set>
#include <chrono>

namespace rxt {
namespace {
void need(bool b,const std::string& s){if(!b)throw std::invalid_argument(s);}
std::string frac(mpq_class q){q.canonicalize();return q.get_num().get_str()+"/"+q.get_den().get_str();}
mpq_class pos(const json& q,const std::string& name){auto x=rational(q);need(x>0,name+" must be strict positive");return x;}
std::string seal(const json& q){return hash(q.dump(-1,' ',true)+"\n");}
json balances(const std::map<std::string,mpq_class>& b){json out=json::object();for(const auto& [k,v]:b)if(v!=0)out[k]=frac(v);return out;}
mpq_class sum(const std::map<std::string,mpq_class>& b){mpq_class v=0;for(const auto& i:b)v+=i.second;return v;}
struct Formation {
    std::string source,phase="OPEN";mpq_class origin,m_form=0,r_form=0,parent_loss=0;
    bool closed=false;std::map<std::string,mpq_class> inside,outside;json captured=json::object(),history=json::array(),packets=json::array(),ids=json::array(),seal_id;
    json snapshot() const {mpq_class interior=origin+sum(inside),exterior=sum(outside);return {{"source_id",source},{"phase",phase},{"sealed",closed},{"crossing_allowed",!closed},
        {"interior_balances",balances(inside)},{"exterior_balances",balances(outside)},{"interior_total",frac(interior)},{"exterior_total",frac(exterior)},
        {"captured_packet_refs",captured},{"internal_history",history},{"theta_packets",packets},{"event_ids",ids},{"m_form",closed?json(frac(m_form)):json(nullptr)},
        {"r_form",closed?json(frac(r_form)):json(nullptr)},{"seal_event_id",seal_id},{"parent_mass_loss",frac(parent_loss)},{"total_mass",frac(closed?mpq_class(m_form+exterior):mpq_class(interior))},{"w_state","W8/W8/X1=0"}};}
    json apply(const json& event){
        auto id=event.value("event_id",std::string()),op=event.value("operation",std::string());need(!id.empty(),"event_id must be nonempty");need(std::find(ids.begin(),ids.end(),id)==ids.end(),"duplicate event_id: "+id);
        static const std::set<std::string> pre={"CONTACT_WRITE","PRE_CLOSE_CAPTURE","APPROACH_A1","SEAL_HOME"},post={"EXTERIOR_ARRIVAL","POST_CLOSE_IN_ATTEMPT","OUT_SELECTED","OUT_QUANTUM_REALIZED"};
        need(pre.count(op)||post.count(op),"unsupported operation: "+op);auto radius=pos(event.value("radius",json(0)),"radius"),rs=pos(event.value("r_s",json(0)),"r_s");mpq_class a=rs/radius;
        auto before=snapshot();std::string status="COMPLETED",phase_event=phase,transient="W8/W8/X1=0";auto matter=event.value("matter_id",json(nullptr)),packet=event.value("matter_packet_ref",json(nullptr));
        auto amount=rational(event.value("amount",json(0)));json theta,parent;bool changed=false;
        if(pre.count(op))need(!closed,op+" is unavailable after Home sealing");else need(closed,op+" requires a sealed Home");
        if(op=="CONTACT_WRITE"){
            need(a<1,"CONTACT_WRITE requires A<1");transient="W8/W9/X1=1";phase="FORMING";history.push_back("CONTACT:"+id+":"+event.value("direction",std::string("FORWARD")));changed=true;
        }else if(op=="PRE_CLOSE_CAPTURE"){
            need(a<1,"PRE_CLOSE_CAPTURE requires A<1");need(matter.is_string()&&!matter.get<std::string>().empty(),"PRE_CLOSE_CAPTURE requires matter_id");amount=pos(event.at("amount"),"amount");auto name=matter.get<std::string>();
            if(!packet.is_null()){
                need(packet.is_object(),"matter_packet_ref must be a typed mapping");auto semantic=packet.value("semantic_sha256",std::string());need(semantic.size()==64&&semantic.find_first_not_of("0123456789abcdef")==std::string::npos,"matter_packet_ref requires a semantic SHA-256");
                need(packet.value("status",std::string())=="EXACT_ATOMIC_ACCUMULATED_WRITE_IDENTITY_ACCEPTED","matter_packet_ref is not an accepted A3D18 identity");need(!captured.contains(name)||captured[name]==packet,"matter_id cannot change atomic packet identity");captured[name]=packet;
            }
            phase="FORMING";inside[name]+=amount;history.push_back("CAPTURE:"+name);changed=true;transient="W8/W9/X1=1";
        }else if(op=="APPROACH_A1"){need(a<1,"APPROACH_A1 requires A<1");phase="FORMING";
        }else if(op=="SEAL_HOME"){
            need(phase=="FORMING","SEAL_HOME requires a prior FORMING state");need(a==1,"SEAL_HOME requires exact A=1");phase_event="CLOSURE";transient="W8/W9/X1=1";m_form=origin+sum(inside);r_form=radius;closed=true;phase="SEALED";seal_id=id;history.push_back("SEAL:"+id);changed=true;
            auto pid="FORM0:"+source+":"+id+":FORMATION_BURST";packets.push_back(pid);theta={{"kind","NON_HAWKING_FORMATION_BURST"},{"packet_id",pid},{"retained_matter_credit","0/1"}};
        }else if(op=="EXTERIOR_ARRIVAL"){
            need(matter.is_string()&&!matter.get<std::string>().empty(),"EXTERIOR_ARRIVAL requires matter_id");amount=pos(event.at("amount"),"amount");phase="POST_FORMATION";outside[matter.get<std::string>()]+=amount;
        }else if(op=="POST_CLOSE_IN_ATTEMPT"){phase="POST_FORMATION";status="IN_FAILED_NO_WRITE";
        }else{
            need(matter.is_string()&&!matter.get<std::string>().empty(),op+" requires matter_id");amount=pos(event.at("amount"),"amount");auto name=matter.get<std::string>();need(outside[name]>=amount,op+" exceeds exterior custody");phase="POST_FORMATION";
            if(op=="OUT_SELECTED")status="OUT_OPTION_RETAINED_NO_DEBIT";
            else{outside[name]-=amount;parent_loss+=amount;parent={{"M_loss",frac(amount)}};status="OUT_QUANTUM_REALIZED";}
        }
        ids.push_back(id);auto after=snapshot();need(!closed||(sum(outside)>=0&&r_form>0&&m_form>0),"post-formation balance invariant failed");
        return {{"A",frac(a)},{"amount",frac(amount)},{"completion_state","W8/W8/X1=0"},{"event_id",id},{"internal_history_changed",changed},{"matter_id",matter},{"matter_packet_ref",packet},
            {"operation",op},{"parent_payload",parent},{"phase_after",phase},{"phase_before",before["phase"]},{"phase_event",phase_event},{"r_s",frac(rs)},{"radius",frac(radius)},
            {"rh_observer",{{"connection_operator",nullptr},{"contact_direction",nullptr},{"formation_current",nullptr},{"source_cone_vector",nullptr},{"surface_operator_after",nullptr},{"surface_operator_before",nullptr},{"status","SCHEMA_RESERVED_DORMANT"}}},
            {"state_after",after},{"state_after_sha256",seal(after)},{"state_before",before},{"state_before_sha256",seal(before)},{"status",status},{"theta_output",theta},{"transient_state",transient}};
    }
};
json formation(const json& spec){
    Formation state;state.source=spec.at("source_id").get<std::string>();need(!state.source.empty(),"source_id must be nonempty");state.origin=pos(spec.at("origin_mass"),"origin_mass");need(spec.at("events").is_array()&&spec["events"].size()<=128,"Limit trace to 128 events");json receipts=json::array(),rejected=json::array();
    for(const auto& event:spec["events"]){auto prior=state;try{receipts.push_back(state.apply(event));}catch(const std::invalid_argument& e){state=prior;if(!spec.value("retain_rejections",false))throw;rejected.push_back({{"event",event},{"status","ADMISSION_REJECTED"},{"reason",e.what()},{"unchanged_state",state.snapshot()}});}}
    auto final=state.snapshot();json trace={{"trace_id",spec.at("trace_id")},{"final_state",final},{"final_state_sha256",seal(final)},{"receipt_count",receipts.size()},{"receipts",receipts}};
    json points=json::array(),edges=json::array();if(receipts.empty())points.push_back({{"id","p0"},{"state",state.snapshot()},{"action",frac(state.origin)}});else points.push_back({{"id","p0"},{"state",receipts[0]["state_before"]},{"action",receipts[0]["state_before"]["total_mass"]}});
    for(size_t i=0;i<receipts.size();++i){auto before="p"+std::to_string(i),after="p"+std::to_string(i+1);points.push_back({{"id",after},{"state",receipts[i]["state_after"]},{"action",receipts[i]["state_after"]["total_mass"]}});edges.push_back({{"id","e"+std::to_string(i)},{"before",before},{"after",after},{"event",{{"label",receipts[i]["operation"]},{"direction",1}}}});}
    auto account=log_account({{"quantity",{{"kind","HOME_TOTAL_MASS"},{"units",{{"native_home_mass",1}}},{"scope","HISTORY"},{"source",HORIZON_BUNDLE_SHA}}},{"source_binding",HORIZON_BUNDLE_SHA},{"points",points},{"edges",edges}});
    json radial;if(state.closed){mpq_class e=sum(state.outside)/state.m_form,rho=1+e;radial={{"e",frac(e)},{"rho_horizon",frac(rho)},{"A_at_horizon","1/1"},{"radius",frac(state.r_form*rho)},{"radius_floor",frac(state.r_form)},{"area_to_formation_ratio",frac(rho*rho)},{"gross_parent_output",frac(state.parent_loss)}};}
    return {{"trace",trace},{"rejected_events",rejected},{"mass_accumulation",account},{"normalized_radius",radial}};
}
json radial_probe(const json& p){
    auto f=pos(p.at("formation_mass"),"formation_mass"),lambda=pos(p.at("radius_per_mass"),"radius_per_mass");auto e=rational(p.at("occupancy_ratio"));need(e>=0,"Negative exterior occupancy");
    json probes=json::array();for(const auto& x:p.at("probe_multipliers")){auto k=pos(x,"horizon_multiplier");mpq_class a=1/k;probes.push_back({{"A",frac(a)},{"horizon_multiplier",frac(k)},{"radius",frac(k*lambda*f*(1+e))},{"region",a==1?"HORIZON":a<1?"EXTERIOR":"INTERIOR_NO_ORDINARY_CROSSING"}});}
    return {{"formation_radius",frac(lambda*f)},{"dimensionless_signature",{{"A_at_horizon","1/1"},{"e",frac(e)},{"rho_horizon",frac(1+e)},{"rho_minus_one_minus_e","0/1"}}},{"probes",probes}};
}
json scenario(uint64_t i){
    auto q=i/8;int mode=int(i%8),depth=int(q%6);q/=6;mpz_class scale=1;for(int k=0;k<depth;++k)scale*=12;
    mpq_class origin(mpz_class(1+q%8),scale);origin.canonicalize();q/=8;mpq_class captured=origin*mpq_class(1+q%8,8);q/=8;
    mpq_class mass=origin+(mode==6?mpq_class(0):captured),external=mass*mpq_class(1+q%17,8);q/=17;unsigned attempts=q%5;mpq_class emitted=(mode==3)?external:mpq_class(external/2);
    json events=json::array();auto event=[&](const std::string& op,const mpq_class& rs,const mpq_class& radius,const mpq_class& amount=mpq_class(0),const std::string& matter=""){json row={{"event_id","E"+std::to_string(events.size())},{"operation",op},{"r_s",frac(rs)},{"radius",frac(radius)}};if(!matter.empty()){row["matter_id"]=matter;row["amount"]=frac(amount);}events.push_back(row);};
    event("CONTACT_WRITE",origin,2*origin);if(mode!=6)event("PRE_CLOSE_CAPTURE",3*origin,4*origin,captured,"FORMING_MATTER");
    event("APPROACH_A1",255*mass,256*mass);
    if(mode==7)event("SEAL_HOME",255*mass,256*mass);
    if(mode!=0){event("SEAL_HOME",mass,mass);event("EXTERIOR_ARRIVAL",mass,mass,external,"EXTERIOR_MATTER");
        for(unsigned k=0;k<=attempts;++k)event("POST_CLOSE_IN_ATTEMPT",mass,mass,external,"EXTERIOR_MATTER");
        event("OUT_SELECTED",mass,mass,emitted,"EXTERIOR_MATTER");
        if(mode!=1)event("OUT_QUANTUM_REALIZED",mass,mass,emitted,"EXTERIOR_MATTER");
        if(mode==4)event("EXTERIOR_ARRIVAL",mass,mass,external,"LATER_ARRIVAL");
        if(mode==5)event("PRE_CLOSE_CAPTURE",mass,2*mass,captured,"CLOSED_CAPTURE_ATTEMPT");
    }
    return {{"trace_id","HORIZON_"+std::to_string(i)},{"source_id","NATIVE_FORM0_AR1_SWEEP"},{"origin_mass",frac(origin)},{"events",events},{"retain_rejections",true}};
}
}
json Engine::horizon(const std::string& op,const json& p){
    need(bool(store_),"Attach native custody before horizon work");
    if(op=="SB_HORIZON_COMPILE"){
        auto directory=std::filesystem::absolute(p.at("directory").get<std::string>());need(file_sha256(directory/"BUNDLE.json")==HORIZON_BUNDLE_SHA,"Horizon source bundle differs");auto b=read_json(directory/"BUNDLE.json");
        for(auto i=b.at("files").begin();i!=b["files"].end();++i){need(i.key().find('/')==std::string::npos&&i.key().find("..") == std::string::npos,"Invalid horizon source filename");need(file_sha256(directory/i.key())==i.value().get<std::string>(),"Horizon source file differs");}
        if(state_.contains("horizon_source"))need(state_["horizon_source"]["bundle_sha256"]==HORIZON_BUNDLE_SHA,"Acquired horizon source differs");
        auto next=state_;next["horizon_source"]={{"directory",directory.string()},{"bundle_sha256",HORIZON_BUNDLE_SHA},{"scope","FORM0_SEALING_AND_AR1_NORMALIZED_RADIUS"}};store_->commit(next);state_=std::move(next);return state_["horizon_source"];
    }
    need(state_.contains("horizon_source"),"Compile native horizon source first");
    if(op=="SB_HORIZON_STATUS")return {{"source",state_["horizon_source"]},{"statistics",state_.value("horizon_statistics",json::object())}};
    if(op=="SB_HORIZON_PROBE")return radial_probe(p);
    need(op=="SB_HORIZON_BATCH"||op=="SB_HORIZON_SWEEP","Unknown native horizon operation");
    auto batch_id=p.value("batch_id",std::string());auto request_sha=hash(p.dump());
    if(!batch_id.empty()&&state_.contains("horizon_batches")&&state_["horizon_batches"].contains(batch_id)){auto saved=state_["horizon_batches"][batch_id];need(saved["request_sha256"]==request_sha,"Horizon batch identity changed");return store_->get(saved["result"].get<std::string>());}
    json specs;
    if(op=="SB_HORIZON_BATCH")specs=p.at("traces");else{auto start=p.at("start").get<uint64_t>(),count=p.at("count").get<size_t>();need(count>0&&count<=256&&start<=100000000-count,"Horizon sweep outside finite admission");specs=json::array();for(size_t i=0;i<count;++i)specs.push_back(scenario(((start+i)*104729)%1000000));}
    need(specs.is_array()&&!specs.empty()&&specs.size()<=256,"Use 1..256 horizon cases");json rows=json::array();uint64_t acquired=0,reused=0,events=0,rejected=0,formed=0;auto start=std::chrono::steady_clock::now();
    json context=json::object();
    if(p.contains("family_id")){auto result=joint("ATOM3D_CONSTRUCTION_RESULT",{{"family_id",p.at("family_id")}});need(result.at("status")=="EXACT_OUTCOME","Coupled construction context must have an actual exact outcome");context["atom3d"]={{"family_id",p["family_id"]},{"outcome_sha256",hash(result.at("outcome").dump())},{"observed_targets",result["observed_targets"]},{"retained_matter_credit","0/1"}};}
    if(p.contains("starbreaker_account")){need(bool(starbreaker_),"Load Starbreaker source");auto name=p.at("starbreaker_account").get<std::string>();auto result=starbreaker_->execute("SB_READOUT",{{"account",name}},state_,store_.get());context["starbreaker"]={{"account",name},{"readout_sha256",hash(result.dump())},{"retained_matter_credit","0/1"}};}
    for(const auto& spec:specs){auto key="HORIZON_TRACE:"+std::string(HORIZON_BUNDLE_SHA)+":"+hash(spec.dump());auto result=store_->recall(key);if(result.is_null()){result=formation(spec);store_->remember(key,result);++acquired;}else ++reused;
        events+=result["trace"]["receipt_count"].get<uint64_t>();rejected+=result["rejected_events"].size();formed+=result["trace"]["final_state"]["sealed"].get<bool>();rows.push_back(std::move(result));}
    json result={{"schema","SB_RXT_HORIZON_EXPERIENCE_V1"},{"source",state_["horizon_source"]},{"cases",rows},{"information_context",context},{"newly_learned_traces",acquired},{"reused_traces",reused},{"event_receipts",events},{"rejected_events",rejected},{"formed_horizons",formed},{"wall_seconds",std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()}};
    auto ref=store_->put(result);auto next=state_;if(!batch_id.empty())next["horizon_batches"][batch_id]={{"request_sha256",request_sha},{"result",ref}};for(const auto& item:{std::pair{"learned_traces",acquired},std::pair{"reused_traces",reused},std::pair{"event_receipts",events},std::pair{"formed_horizons",formed}})next["horizon_statistics"][item.first]=state_.value("horizon_statistics",json::object()).value(item.first,uint64_t(0))+item.second;
    next["horizon_log_head"]=store_->put({{"previous",state_.value("horizon_log_head",json(nullptr))},{"operation",op},{"payload",p},{"result",ref}});next["sequence"]=state_["sequence"].get<uint64_t>()+1;auto root=store_->commit(next);state_=std::move(next);result["result_object"]=ref;result["checkpoint"]={{"root",root},{"sequence",state_["sequence"]}};return result;
}
}
