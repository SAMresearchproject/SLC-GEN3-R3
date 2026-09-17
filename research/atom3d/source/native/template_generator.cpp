#include <nlohmann/json.hpp>
#include <algorithm>
#include <array>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using J=nlohmann::json;
void need(bool x,const char* m){if(!x)throw std::runtime_error(m);}
void exact(const J& value){need(!value.is_number_float(),"floating input is not admitted");if(value.is_array()||value.is_object())for(auto&v:value)exact(v);}
struct Source {
 J edges,actions;
 std::array<std::vector<int>,100> adj;
 std::map<std::pair<int,int>,int> edge;
 Source(const J& p):edges(p.at("edges")),actions(p.at("actions")){
  for(size_t i=0;i<edges.size();++i){int a=edges[i]["u"],b=edges[i]["v"];need(a>=0&&b<100&&a<b,"source role edge");edge[{a,b}]=i;adj[a].push_back(b);adj[b].push_back(a);}
  need(actions.size()==48,"source action count");
 }
 int edge_id(int a,int b)const {if(a>b)std::swap(a,b);auto i=edge.find({a,b});return i==edge.end()?-1:i->second;}
 int inverse(int i)const {
  const auto&a=actions.at(i);int hit=-1;
  for(size_t j=0;j<actions.size();j++){const auto&b=actions[j];
   if(a["source_site"]==b["target_site"]&&a["target_site"]==b["source_site"]&&a["octahedral_vertex"]==b["octahedral_vertex"]&&a["action"]!=b["action"]){need(hit<0,"ambiguous inverse");hit=j;}}
  need(hit>=0,"missing inverse");return hit;
 }
 void validate(const J& n)const {
  const auto&o=n.at("objects");need(o.size()>=3&&o.size()<=8,"template extent");std::set<int>rs,ss;int z=0,nn=0;
  for(auto&v:o){int r=v.at("role"),s=v.at("site");need(r>=0&&r<100&&s>=0&&s<8,"object address");need(rs.insert(r).second&&ss.insert(s).second,"repeated object address");std::string k=v.at("kind");need(k=="proton"||k=="neutron","matter kind");z+=k=="proton";nn+=k=="neutron";}
  need(n.at("Z")==z&&n.at("N")==nn&&n.at("electrons")==z,"derived matter inventory");
  need(n.at("cycles").size()==o.size()-1,"path cycle extent");std::set<std::pair<int,int>>links;
  for(auto&c:n.at("cycles")){
   int u=c.at("u"),v=c.at("v");need(u>=0&&v>=0&&u<int(o.size())&&v<int(o.size())&&u!=v,"cycle endpoint");
   need(c.at("edge")==edge_id(o[u]["role"],o[v]["role"]),"cycle role incidence");need(c.at("edge").get<int>()>=0,"absent role edge");
   int f=c.at("forward"),r=c.at("reverse");need(f>=0&&f<int(actions.size())&&r==inverse(f),"reciprocal action");auto a=actions[f],b=actions[r];
   need(a["source_site"]==o[u]["site"]&&a["target_site"]==o[v]["site"],"cycle site incidence");
   int qi=a["source_frame_q"],qo=a["target_frame_q"],d=a["local_displacement"],sigma=a["sigma_chi"];
   need((qi+d+4)%4==qo&&b["source_frame_q"]==qo&&b["target_frame_q"]==qi,"phase return");
   need(b["local_displacement"]==-d&&b["sigma_chi"]==-sigma,"signed reciprocal return");links.insert(std::minmax(u,v));
  }
  for(int i=1;i<int(o.size());i++)need(links.count({i-1,i}),"append path connectivity");
 }
 std::vector<int> features(const J& n)const {
  std::set<int>used;int mask=0;for(auto&o:n["objects"]){used.insert(o["role"].get<int>());mask|=1<<o["site"].get<int>();}
  int role=n["objects"].back()["role"],site=n["objects"].back()["site"],rf=0,sf=0,isolated=0,leaves=0,components=0,visited=mask;
  for(int r:adj[role]){rf+=!used.count(r);}
  for(int b:{1,2,4}){sf+=!(mask&(1<<(site^b)));}
  for(int s=0;s<8;s++)if(!(mask&(1<<s))){int degree=0;for(int b:{1,2,4})degree+=!(mask&(1<<(s^b)));isolated+=degree==0;leaves+=degree==1;
   if(!(visited&(1<<s))){components++;std::vector<int>q{s};visited|=1<<s;for(size_t k=0;k<q.size();k++)for(int b:{1,2,4}){int t=q[k]^b;if(!(visited&(1<<t))){visited|=1<<t;q.push_back(t);}}}}
  return {int(n["objects"].size()),mask,site,rf,sf,components,isolated,leaves,int(adj[role].size())};
 }
 bool completion(const J& n)const {
  std::array<bool,100>used{};int mask=0;for(auto&o:n["objects"]){used[o["role"].get<int>()]=true;mask|=1<<o["site"].get<int>();}
  int remaining=8-n["objects"].size();
  std::function<bool(int,int)>rolepath=[&](int r,int left){if(!left)return true;for(int v:adj[r])if(!used[v]){used[v]=true;bool ok=rolepath(v,left-1);used[v]=false;if(ok)return true;}return false;};
  std::function<bool(int,int)>sitepath=[&](int s,int m){if(m==255)return true;for(int b:{1,2,4}){int v=s^b;if(!(m&(1<<v))&&sitepath(v,m|(1<<v)))return true;}return false;};
  return sitepath(n["objects"].back()["site"],mask)&&rolepath(n["objects"].back()["role"],remaining);
 }
 J extend(const J& p,const J& q)const {
  validate(p);int role=q.at("role"),site=q.at("site"),f=q.at("forward");std::string kind=q.at("kind");
  J n=p;int u=n["objects"].size()-1,v=u+1;
  n["objects"].push_back({{"role",role},{"site",site},{"kind",kind}});
  n["Z"]=p["Z"].get<int>()+(kind=="proton");n["N"]=p["N"].get<int>()+(kind=="neutron");n["electrons"]=n["Z"];
  n["cycles"].push_back({{"u",u},{"v",v},{"edge",edge_id(p["objects"].back()["role"],role)},
   {"forward",f},{"reverse",inverse(f)},{"origin",q.at("id")},{"parent_terminal",p.at("terminal")}});
  n["terminal"]=q.at("id").get<std::string>()+":reciprocal";n["parent"]=p.at("id");n.erase("id");
  validate(n);return n;
 }
 J proposals(const J& parents)const {
  J out=J::array();for(auto&p:parents){validate(p);if(p["objects"].size()==8)continue;std::set<int>usedr,useds;for(auto&o:p["objects"]){usedr.insert(o["role"].get<int>());useds.insert(o["site"].get<int>());}
   int r=p["objects"].back()["role"],s=p["objects"].back()["site"];
   for(int role:adj[r])if(!usedr.count(role))for(size_t f=0;f<actions.size();f++)if(actions[f]["source_site"]==s){int site=actions[f]["target_site"];if(useds.count(site))continue;
    for(std::string kind:{"neutron","proton"}){J q={{"id",p["id"].get<std::string>()+":"+std::to_string(role)+":"+std::to_string(site)+":"+std::to_string(f)+":"+kind},{"parent",p["id"]},{"role",role},{"site",site},{"forward",f},{"kind",kind}};
     // Features use the hypothetical extension; no completion label is evaluated here.
     J n=extend(p,q);q["features"]=features(n);q["Z"]=n["Z"];q["N"]=n["N"];J roles=J::array();for(auto&o:n["objects"])roles.push_back(o["role"]);std::sort(roles.begin(),roles.end());q["split_group"]={{"roles",roles},{"last_role",role},{"site_mask",q["features"][1]},{"last_site",site}};out.push_back(q);
    }
   }
  }return out;
 }
 J interface(const J& n)const {
  validate(n);int a=n["objects"].size();J placements=J::array();std::vector<int>v(a);std::function<void(int,int)>walk=[&](int k,int mask){if(k==a){placements.push_back(v);return;}for(int s=0;s<8;s++)if(!(mask&(1<<s))&&(k==0||__builtin_popcount(unsigned(s^v[k-1]))==1)){v[k]=s;walk(k+1,mask|(1<<s));}};walk(0,0);
  J lap=J::array();for(int i=0;i<a;i++){J row=J::array();for(int j=0;j<a;j++)row.push_back(i==j?(i==0||i==a-1?1:2):std::abs(i-j)==1?-1:0);lap.push_back(row);}
  return {{"objects",a},{"role_order",n["objects"]},{"placements",placements},{"connector_laplacian",lap},{"interface","Injective cube embeddings of this executed source path; each edge has the two source reciprocal action choices."},{"old_four_template_membership_reused",false}};
 }
};
int main(){try{
 J p;std::cin>>p;exact(p);Source s(p);std::string mode=p.at("mode");J out;
 if(mode=="PROPOSE")out={{"proposals",s.proposals(p.at("parents"))}};
 else if(mode=="EXTEND"){
  std::map<std::string,J>parents;for(auto&n:p.at("parents"))parents[n.at("id")]=n;J rows=J::array();
  for(auto&q:p.at("proposals")){auto n=s.extend(parents.at(q.at("parent")),q);rows.push_back({{"proposal",q.at("id")},{"node",n},{"can_complete_eight",s.completion(n)}});}out={{"rows",rows}};
 }else if(mode=="INTERFACE")out=s.interface(p.at("node"));
 else throw std::runtime_error("unknown template operation");
 std::cout<<out.dump()<<'\n';
}catch(std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
