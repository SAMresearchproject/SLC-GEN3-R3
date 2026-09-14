#include "engine.hpp"
#include "starbreaker.hpp"
#include "atom3d.hpp"
#include "training.hpp"
#include "knowledge.hpp"
#include "signed_energy.hpp"
#include <algorithm>
#include <array>
#include <functional>
#include <numeric>

namespace rxt {
namespace {
void need(bool b,const std::string& s){if(!b)throw std::invalid_argument("Domain transfer: "+s);}
struct Example { std::vector<int> x; bool y; int split; json witness; };
mpq_class impurity(int64_t n,int64_t p){return n?mpq_class(mpz_class(2)*p*(n-p),mpz_class(n)):mpq_class(0);}
json tree(const std::vector<Example>& data,const std::vector<int>& ids,int depth,int positive_weight,int negative_weight) {
    int pos=0;for(int i:ids)pos+=data[i].y;
    json node={{"n",ids.size()},{"positive",pos},{"probability",number(mpq_class(pos,ids.size()))}};
    node["witness"]=data[ids.front()].witness;
    if(!depth || pos==0 || pos==int(ids.size()))return node;
    auto cost_of=[&](int n,int p){return impurity(int64_t(p)*positive_weight+int64_t(n-p)*negative_weight,int64_t(p)*positive_weight);};
    mpq_class best=cost_of(ids.size(),pos);int feature=-1,threshold=0;
    for(size_t f=0;f<data[ids[0]].x.size();++f){
        std::map<int,std::pair<int,int>> counts;for(int i:ids){auto& c=counts[data[i].x[f]];c.first++;c.second+=data[i].y;}
        int n=0,p=0;for(const auto& [t,c]:counts){n+=c.first;p+=c.second;if(n==int(ids.size()))break;
            mpq_class cost=cost_of(n,p)+cost_of(ids.size()-n,pos-p);
            if(cost<best){best=cost;feature=int(f);threshold=t;}
        }
    }
    if(feature<0)return node;
    std::vector<int> a,b;for(int i:ids)(data[i].x[feature]<=threshold?a:b).push_back(i);
    node["feature"]=feature;node["threshold"]=threshold;node["left"]=tree(data,a,depth-1,positive_weight,negative_weight);node["right"]=tree(data,b,depth-1,positive_weight,negative_weight);return node;
}
mpq_class predict(const json& t,const std::vector<int>& x){const json* p=&t;while(p->contains("feature"))p=&p->at(x[p->at("feature").get<int>()]<=p->at("threshold").get<int>()?"left":"right");return rational(p->at("probability"));}
json metric(const json& t,const std::vector<Example>& d,int split){int n=0,yes=0,tp=0,tn=0;json examples=json::array();
    for(const auto& r:d)if(r.split==split){bool p=predict(t,r.x)>=rational(t.value("classification_threshold",json("1/2")));++n;yes+=r.y;tp+=p&&r.y;tn+=!p&&!r.y;if(p!=r.y && examples.size()<8)examples.push_back(r.witness);}
    mpq_class score=yes&&n>yes?(mpq_class(tp,yes)+mpq_class(tn,n-yes))/2:n?mpq_class(tp+tn,n):mpq_class(0);
    return {{"rows",n},{"positives",yes},{"correct",tp+tn},{"balanced_accuracy",number(score)},{"exception_witnesses",examples}};
}
json fit(const std::vector<Example>& d){std::vector<int> ids;for(size_t i=0;i<d.size();++i)if(d[i].split==0)ids.push_back(i);need(!ids.empty(),"No training source rows");
    int positives=0;for(int i:ids)positives+=d[i].y;int negatives=int(ids.size())-positives;
    bool both=positives>0&&negatives>0;
    json selected;mpq_class best=-1;int depth=0;
    for(int k=0;k<=3;++k){auto t=tree(d,ids,k,both?negatives:1,both?positives:1);t["classification_threshold"]=both?number(mpq_class(positives,ids.size())):json("1/2");auto dev=metric(t,d,1);mpq_class score=rational(dev["balanced_accuracy"]);if(score>best){best=score;selected=t;depth=k;}}
    return {{"tree",selected},{"depth",depth},{"training",metric(selected,d,0)},{"development",metric(selected,d,1)},
        {"test_rows_reserved",std::count_if(d.begin(),d.end(),[](const auto& r){return r.split==2;})},
        {"fit","NATIVE_CPP_EXACT_GMP_CLASS_BALANCED_CART"},{"class_weights",{{"positive",both?negatives:1},{"negative",both?positives:1}}},{"selection","development balanced accuracy; shallower on tie"}};
}
void rules(const json& t,json path,json& out){if(!t.contains("feature")){auto row=t;row["conditions"]=path;row["all_probability_ties_retained"]=true;out.push_back(row);return;}
    for(auto side:{"left","right"}){auto p=path;p.push_back({{"feature",t["feature"]},{"comparison",std::string(side)=="left"?"<=":">"},{"threshold",t["threshold"]}});rules(t[side],p,out);}}
std::vector<int> features(const SBPolicyIR& ir,uint32_t f){int64_t x[32];sb_features(ir,f,x);return std::vector<int>(x,x+32);}
}

json Engine::transfer(const std::string& op,const json& p){
    need(bool(store_)&&bool(starbreaker_)&&bool(atom3d_),"Attach the native joint domains first");
    auto commit=[&](json next,json result){auto ref=store_->put({{"operation",op},{"request",p},{"result",result}});next["transfer_log_head"]=ref;next["sequence"]=state_["sequence"].get<uint64_t>()+1;auto root=store_->commit(next);state_=std::move(next);result["checkpoint"]={{"root",root},{"record",ref}};return result;};
    if(op=="GEN3_TRANSFER_FIT_CHECK"){
        std::vector<Example> fixtures;
        for(int split=0;split<3;++split)for(int i=0;i<100;++i)fixtures.push_back({{i<30?1:0},i<10,split,{{"row",i},{"split",split}}});
        auto learned=fit(fixtures);need(rational(learned["development"]["balanced_accuracy"])==mpq_class(8,9) && learned["test_rows_reserved"]==100,"Balanced native tree fixture differs");
        return {{"status","PASS"},{"model",learned},{"checks",3}};
    }
    if(op=="GEN3_TRANSFER_STATUS")return {{"engine",VERSION},{"SB_domain_update","SB-GEN3-RXT-R2"},{"A3D41_domain_update","A3D41-RXT-R3"},{"learning",state_.value("domain_transfer",json::object())},{"rh_transfer",state_.value("rh_domain_transfer",json::object())}};
    if(op=="GEN3_TRANSFER_ENERGY")return signed_energy(p.at("left"),p.at("right"),rational(p.at("a")),rational(p.at("b")));
    if(op=="ATOM3D_COMMON_MINIMA"){
        auto f=p.at("family_id").get<uint32_t>();auto row=joint("ATOM3D_CONSTRUCTION_RESULT",{{"family_id",f}});need(row["status"]=="EXACT_OUTCOME","Compute the family's native contexts first");
        const auto& cs=row["outcome"]["contexts"];const auto& a=cs[3];const auto& b=cs[11];
        auto ar=joint("ATOM3D_CONSTRUCTION_MINIMUM_SET",{{"sha256",a["set"]}}),br=joint("ATOM3D_CONSTRUCTION_MINIMUM_SET",{{"sha256",b["set"]}});
        std::string ah=ar.at("bits_hex"),bh=br.at("bits_hex"),raw(32768,'\0'),hex(65536,'0');need(ah.size()==65536&&bh.size()==65536,"Incomplete minimum sets");
        auto nib=[](char c){need((c>='0'&&c<='9')||(c>='a'&&c<='f'),"Invalid bitmap encoding");return c<='9'?c-'0':c-'a'+10;};
        json states=json::array();const char* digits="0123456789abcdef";
        for(size_t i=0;i<32768;++i){unsigned byte=((nib(ah[2*i])<<4)|nib(ah[2*i+1]))&((nib(bh[2*i])<<4)|nib(bh[2*i+1]));raw[i]=char(byte);hex[2*i]=digits[byte>>4];hex[2*i+1]=digits[byte&15];for(unsigned j=0;j<8;++j)if(byte&(1u<<j))states.push_back(8*i+j);}
        auto digest=hash(raw);store_->remember("A3D41_COMMON_MINIMA:"+digest,{{"bits_hex",hex},{"sha256",digest}});
        json result={{"revision","A3D41-RXT-R3"},{"family_id",f},{"source",atom3d_->binding()},{"contexts",{3,11}},
            {"native_minima",{a,b}},{"common_minimum_count",states.size()},{"intersection_sha256",digest},{"complete_intersection_retained",true},
            {"sum_lower_bound",number(rational(a.at("minimum"))+rational(b.at("minimum")))},{"sum_lower_bound_attained",!states.empty()},
            {"rule",states.empty()?"No common minimizer: positive joint excess on this finite source":"Joint lower bound attained exactly on the complete intersection"}};
        if(p.value("include_states",false))result["all_minimizing_states"]=states;
        return result;
    }
    if(op=="GEN3_TRANSFER_OBSERVE"){
        train("TRAIN_STATUS",json::object());auto next=state_;auto d=next.value("domain_transfer",json::object());
        if(!d.contains("observations"))d["observations"]=json::object();
        json families=json::array(),accounts=json::array();
        for(const auto& f:p.value("family_ids",json::array())){auto id=f.get<uint32_t>();need(id<4800000,"Family outside source");auto row=transfer("ATOM3D_COMMON_MINIMA",{{"family_id",id}});row["features"]=features(starbreaker_->policy_ir(),id);row["split"]=training_->pattern_split[id/7680];auto ref=store_->put(row);d["observations"]["A3D41:"+std::to_string(id)]=ref;families.push_back({{"family_id",id},{"common_minimum_count",row["common_minimum_count"]},{"split",row["split"]},{"observation",ref}});}
        for(const auto& name:p.value("accounts",json::array())){auto read=starbreaker_->execute("SB_READOUT",{{"account",name}},state_,store_.get());need(read.contains("signed_energy"),"Run this SB history on the updated domain first");auto rho=read["source_binding"]["rho"].get<int>();int split=rho%5==0?1:rho%5==1?2:0;
            auto row=json{{"account",name},{"source",read["source_binding"]},{"quantity",read["signed_energy"]},{"split",split}};auto ref=store_->put(row);d["observations"]["SB:"+name.get<std::string>()]=ref;accounts.push_back({{"account",name},{"observation",ref}});}
        d["revision"]="GEN3_NATIVE_DOMAIN_TRANSFER_R1";d["source_binding"]={{"a3d41",atom3d_->binding()},{"starbreaker",starbreaker_->binding()}};next["domain_transfer"]=d;
        return commit(next,{{"status","OBSERVED"},{"families",families},{"accounts",accounts},{"unique_observations",d["observations"].size()}});
    }
    if(op=="GEN3_TRANSFER_FIT"){
        std::vector<Example> a,s;for(auto it=state_.at("domain_transfer").at("observations").begin();it!=state_["domain_transfer"]["observations"].end();++it){auto row=store_->get(it.value().get<std::string>());int split=row["split"];
            if(it.key().rfind("A3D41:",0)==0)a.push_back({row["features"].get<std::vector<int>>(),row["sum_lower_bound_attained"],split,{{"family_id",row["family_id"]},{"native_minima",row["native_minima"]},{"intersection",row["intersection_sha256"]}}});
            else for(const auto& edge:row["quantity"]["edges_per_cycle"])s.push_back({edge["features"].get<std::vector<int>>(),edge["positive_gain"],split,{{"account",row["account"]},{"phase",edge["phase"]},{"source",row["source"]},{"gain",edge["gain"]}}});
        }
        json models={{"A3D41_COMMON_MINIMUM",fit(a)},{"SB_POSITIVE_SIGNED_ENERGY_GAIN",fit(s)}};
        for(auto& m:models){m["rules"]=json::array();rules(m["tree"],json::array(),m["rules"]);}
        models["A3D41_COMMON_MINIMUM"]["features"]="Original 32 source-construction features, in retained policy order";
        models["SB_POSITIVE_SIGNED_ENERGY_GAIN"]["features"]={"signed_inner_product_sign","left_support_le_right","left_norm_le_right"};
        auto next=state_;next["domain_transfer"]["models"]=store_->put(models);return commit(next,{{"status","TRAINED_AND_INSTALLED"},{"models",models}});
    }
    if(op=="GEN3_TRANSFER_PLAN"){
        auto models=store_->get(state_.at("domain_transfer").at("models").get<std::string>());json candidates=p.at("family_ids");need(candidates.size()<=4096,"Bounded candidate pool required");
        std::map<mpq_class,json,std::greater<mpq_class>> groups;for(const auto& f:candidates){auto id=f.get<uint32_t>();need(id<4800000,"Family outside source");auto score=predict(models["A3D41_COMMON_MINIMUM"]["tree"],features(starbreaker_->policy_ir(),id));if(!groups.contains(score))groups[score]=json::array();groups[score].push_back(id);}
        json order=json::array(),ties=json::array();for(auto& [score,ids]:groups){ties.push_back({{"probability",number(score)},{"family_ids",ids}});for(const auto& id:ids)order.push_back(id);}
        std::string ranking_source="NEW_COMMON_MINIMUM_MODEL";
        if(p.value("use_acquired_policy",false)||!models["A3D41_COMMON_MINIMUM"]["tree"].contains("feature")){
            auto legacy=starbreaker_->execute("SB_CONSTRUCTION_POLICY",{{"family_ids",candidates},{"source_contract","A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1"},{"targets",{"shared_four_state_orbit","channel_minimum_sets_agree"}},{"backend","cpu"}},state_,store_.get());
            order=json::array();ties=legacy["ranked_tie_groups"];for(const auto& group:ties)for(const auto& id:group["family_ids"])order.push_back(id);
            ranking_source="ACQUIRED_ORBIT_AND_CHANNEL_POLICY_FALLBACK";
        }
        auto sb=starbreaker_->campaign_requests(p.value("sb_start",uint64_t(1000000)),p.value("sb_count",size_t(64)),p.value("prefix",std::string("TRANSFER")));
        return {{"ranking_source",ranking_source},{"family_ids",order},{"ranked_tie_groups",ties},{"all_ties_retained",true},{"SB_requests",sb},{"model_object",state_["domain_transfer"]["models"]}};
    }
    if(op=="GEN3_TRANSFER_SB_REQUESTS"){need(p.at("count").get<size_t>()<=4096,"Bounded SB requests required");return {{"requests",starbreaker_->campaign_requests(p.at("start").get<uint64_t>(),p.at("count").get<size_t>(),p.at("prefix").get<std::string>())}};}
    if(op=="GEN3_TRANSFER_RH"){
        auto path=std::filesystem::path(p.at("native_trace_path").get<std::string>());need(file_sha256(path)==p.at("sha256").get<std::string>(),"RH native trace source differs");auto source=read_json(path);need(source.at("status")=="COMPLETED","Completed native RH trace required");
        auto models=store_->get(state_.at("domain_transfer").at("models").get<std::string>());const auto& sb=models["SB_POSITIVE_SIGNED_ENERGY_GAIN"]["tree"];
        std::vector<Example> rows;json priorities=json::array();size_t checks=0;std::map<mpq_class,json,std::greater<mpq_class>> ranks;
        for(const auto& c:source.at("cases")){mpq_class a=rational(c["base_Q"]);auto x=c["base_G"];int gain_count=0,stages=0;
            for(const auto& e:c["prime_trace"]){mpq_class q=rational(e["Q"]),b=q-a;need(e["children"][0]==x,"RH child chain differs");auto energy=signed_energy(json::array({x}),json::array({e["children"][1]}),a,b);
                need(rational(energy["repayment"])==rational(e["repayment"])&&rational(energy["gain"])==rational(e["gain"]),"RH exact trace identity differs");checks+=2;
                auto s=c["s"].get<uint64_t>();int split=s==8388608?1:0;rows.push_back({energy["features"].get<std::vector<int>>(),energy["positive_gain"],split,{{"s",c["s"]},{"t",c["t"]},{"prime",e["prime"]}}});gain_count+=energy["positive_gain"].get<bool>();++stages;a=q;x=e["G"];
            }
            mpq_class score=rational(c.at("positive_variation_after_minimum"));auto row=json{{"s",c["s"]},{"t",c["t"]},{"positive_stages",gain_count},{"stages",stages},{"post_minimum_variation",number(score)}};
            if(!ranks.contains(score))ranks[score]=json::array();ranks[score].push_back(row);
        }
        for(auto& [score,rs]:ranks)priorities.push_back({{"score",number(score)},{"source_cases",rs}});
        json result={{"status","TRANSFERRED_AND_RH_TRAINED"},{"native_source_sha256",p["sha256"]},{"exact_identity_checks",checks},{"RH_rows",rows.size()},
            {"SB_model_on_RH_training_scales",metric(sb,rows,0)},{"SB_model_on_RH_largest_scale",metric(sb,rows,1)},
            {"RH_model",fit(rows)},{"next_full_trace_priority_groups",priorities},
            {"shared_rule","gain=right_energy-repayment; repayment=norm(b*x+a*y)^2/(a*b*(a+b))"},
            {"quantity_mapping","SB: two-dimensional receiver vectors with unit phase supports. RH: signed counts with native Q supports."}};
        result["RH_model"]["rules"]=json::array();rules(result["RH_model"]["tree"],json::array(),result["RH_model"]["rules"]);
        auto next=state_;next["rh_domain_transfer"]={{"result",store_->put(result)},{"SB_model_source",state_["domain_transfer"]["models"]},{"native_source_sha256",p["sha256"]}};return commit(next,result);
    }
    throw std::invalid_argument("Unknown native domain transfer operation: "+op);
}
}
