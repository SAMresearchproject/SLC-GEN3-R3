#include "signed_energy.hpp"
#include "trees.hpp"
#include "operator_log.hpp"
#include "spectral_log.hpp"
#include "source_algebra.hpp"
#include <iostream>
using namespace rxt;
static std::vector<int> feature_vector(const json& a){need(a.is_array()&&!a.empty()&&a.size()<=128,"Feature vector width 1..128 required");std::vector<int> out;for(auto& v:a){need(v.is_number_integer()&&v>=-2147483647&&v<=2147483647,"Bounded integer feature required");out.push_back(v.get<int>());}return out;}
static void validate_tree(const json& t,size_t width,int depth=0){need(depth<=32&&t.is_object(),"Bounded tree required");need(t.contains("probability"),"Missing node probability");auto p=rational(t["probability"]);need(p>=0&&p<=1,"Probability outside unit interval");if(t.contains("classification_threshold")){auto q=rational(t["classification_threshold"]);need(q>=0&&q<=1,"Invalid classification threshold");}if(t.contains("feature")){need(t["feature"].is_number_integer()&&t["feature"]>=0&&t["feature"]<width&&t["threshold"].is_number_integer(),"Invalid split");validate_tree(t.at("left"),width,depth+1);validate_tree(t.at("right"),width,depth+1);}}
json execute(const json& request){auto op=request.at("op").get<std::string>();const auto& p=request.at("payload");
 if(op=="SOURCE_OPERATOR_WORD"||op=="SOURCE_SUBSPACE"||op=="NATIVE_PAIR_ROOTS"||op=="BLOCK_SOURCE_RECURRENCE"||op=="SOURCE_SPECTRAL_CREATION"||op=="SOURCE_WORD_EXCHANGE"||op=="SOURCE_TERMINAL_ACTION")return source_algebra::execute(op,p);
 if(op=="SPECTRAL_ADMIT")return spectral_log::build(p,false);
 if(op=="SPECTRAL_EXTEND")return spectral_log::build(p,true);
 if(op=="SCALAR_LOG")return spectral_log::scalar(p);
 if(op=="DIRECT_SCALAR_LOG")return spectral_log::scalar(p,true);
 if(op=="SPECTRAL_LOG")return spectral_log::profile(p);
 if(op=="TRANSPORT_LOG")return spectral_log::transport(p);
 if(op=="OPERATOR_OBSTRUCTION")return operator_log::obstruction(p);
 if(op=="COMMUTING_LOG")return operator_log::commuting_log(p);
 if(op=="CONSTRUCTION_FEATURES"){
  const auto& ids=p.at("family_ids");const auto& table=p.at("feature_table");const auto& inventory=p.at("inventory_counts");need(ids.is_array()&&!ids.empty()&&ids.size()<=4096,"Bounded family pool required");json rows=json::array();std::set<uint32_t>seen;
  for(auto& value:ids){need(value.is_number_integer()&&value>=0&&value<4800000,"Family outside source");uint32_t id=value.get<uint32_t>();need(seen.insert(id).second,"Duplicate family");uint32_t a=id;std::vector<int> out(32);out[7]=a%128+1;a/=128;out[6]=a%6;a/=6;out[4]=a%5;a/=5;out[5]=a%2;a/=2;auto pattern=a;for(int i=0;i<4;++i){out[i]=a%5;a/=5;}out[8]=inventory.at(pattern).at(out[4]).at(out[5]);for(int j=0;j<23;++j)out[j+9]=table.at(pattern).at(j);rows.push_back({{"id",id},{"features",out}});}
  return rows;
 }
 if(op=="SIGNED_ENERGY"){need(p["left"].size()<=262144,"Vector admission limit");return signed_energy(p.at("left"),p.at("right"),rational(p.at("a")),rational(p.at("b")));}
 if(op=="COMMON_MINIMA"){
  const auto& states=p.at("states");const auto& left=p.at("left");const auto& right=p.at("right");need(states.is_array()&&!states.empty()&&states.size()<=262144&&left.is_array()&&right.is_array()&&states.size()==left.size()&&states.size()==right.size(),"Complete paired finite cost tables required");
  std::set<std::string> seen;std::vector<mpq_class>a,b;mpq_class amin,bmin,jmin;json ai=json::array(),bi=json::array(),both=json::array(),joint=json::array();
  for(size_t i=0;i<states.size();++i){need(states[i].is_string()||states[i].is_number_integer(),"Scalar state identity required");need(seen.insert(states[i].dump()).second,"Duplicate source state");a.push_back(rational(left[i]));b.push_back(rational(right[i]));mpq_class sum=a.back()+b.back();if(i==0||a.back()<amin)amin=a.back();if(i==0||b.back()<bmin)bmin=b.back();if(i==0||sum<jmin)jmin=sum;}
  for(size_t i=0;i<states.size();++i){if(a[i]==amin)ai.push_back(states[i]);if(b[i]==bmin)bi.push_back(states[i]);if(a[i]==amin&&b[i]==bmin)both.push_back(states[i]);if(a[i]+b[i]==jmin)joint.push_back(states[i]);}
  mpq_class gap=jmin-amin-bmin;need(gap>=0&&((gap==0)==!both.empty()),"Complete minimum intersection identity");
  return {{"left_minimum",number(amin)},{"right_minimum",number(bmin)},{"left_states",ai},{"right_states",bi},{"common_states",both},{"common_minimum_count",both.size()},{"joint_minimum",number(jmin)},{"joint_states",joint},{"sum_lower_bound",number(mpq_class(amin+bmin))},{"joint_excess",number(gap)},{"sum_lower_bound_attained",gap==0},{"complete_supplied_roster",true},{"states_evaluated",states.size()}};
 }
 if(op=="TREE_FIT"){
  const auto& rows=p.at("rows");need(rows.is_array()&&!rows.empty()&&rows.size()<=20000,"Bounded explicit training/development/test rows required");std::vector<Example>d;size_t width=0;bool training=false,development=false;
  for(auto& r:rows){auto x=feature_vector(r.at("features"));if(!width)width=x.size();need(x.size()==width,"Feature width differs");need(r["label"].is_number_integer()&&(r["label"]==0||r["label"]==1),"Binary label required");need(r["split"].is_number_integer()&&r["split"]>=0&&r["split"]<=2,"Split 0/1/2 required");int split=r["split"];training|=split==0;development|=split==1;d.push_back({x,r["label"].get<int>()!=0,split,r.at("witness")});}
  need(training&&development,"Training and development rows required");auto model=fit(d);model["rules"]=json::array();rules(model["tree"],json::array(),model["rules"]);model["feature_count"]=width;return model;
 }
 if(op=="TREE_PREDICT"){
  const auto& rows=p.at("rows");need(rows.is_array()&&!rows.empty()&&rows.size()<=4096,"Bounded candidate rows required");const auto& model=p.at("model");size_t width=model.at("feature_count");validate_tree(model.at("tree"),width);json out=json::array();std::map<mpq_class,json,std::greater<mpq_class>>groups;std::set<std::string>ids;
  for(auto& row:rows){need(row["id"].is_string()||row["id"].is_number_integer(),"Candidate identity required");need(ids.insert(row["id"].dump()).second,"Duplicate candidate identity");auto x=feature_vector(row.at("features"));need(x.size()==width,"Candidate feature width differs");auto probability=predict(model["tree"],x);mpq_class threshold=rational(model["tree"].value("classification_threshold",json("1/2")));out.push_back({{"id",row["id"]},{"probability",number(probability)},{"positive",probability>=threshold}});if(!groups.count(probability))groups[probability]=json::array();groups[probability].push_back(row["id"]);}
  json ties=json::array();for(auto& [score,group]:groups)ties.push_back({{"probability",number(score)},{"ids",group}});return {{"predictions",out},{"ranked_tie_groups",ties},{"all_ties_retained",true}};
 }
 throw std::invalid_argument("Unknown capability operation");
}
int main(){std::string line;while(std::getline(std::cin,line)){try{auto r=execute(json::parse(line));std::cout<<json({{"ok",true},{"result",r}}).dump()<<std::endl;}catch(const std::exception& e){std::cout<<json({{"ok",false},{"error",e.what()}}).dump()<<std::endl;}}}
