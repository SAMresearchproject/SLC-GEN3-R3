#pragma once
#include "engine.hpp"
#include <array>
#include <utility>
namespace operator_log {
using R=mpq_class;
using J=nlohmann::json;
using rxt::need;
// Exact polynomial in one explicitly named formal parameter: ell or g.
struct Poly { std::map<int,R> c; Poly(R x=0){if(x!=0)c[0]=x;} };
Poly operator+(Poly a,const Poly&b){for(auto [k,v]:b.c){a.c[k]+=v;if(a.c[k]==0)a.c.erase(k);}return a;}
Poly operator-(Poly a,const Poly&b){for(auto [k,v]:b.c){a.c[k]-=v;if(a.c[k]==0)a.c.erase(k);}return a;}
Poly operator*(const Poly&a,const Poly&b){Poly r;for(auto [i,x]:a.c)for(auto [j,y]:b.c)r.c[i+j]+=x*y;for(auto it=r.c.begin();it!=r.c.end();)if(it->second==0)it=r.c.erase(it);else ++it;return r;}
Poly sc(Poly a,R r){return a*Poly(r);}
Poly xp(int n){Poly p;p.c[n]=1;return p;}
R ev(const Poly&a,R x){R r=0;for(auto [k,v]:a.c){R t=1;for(int i=0;i<k;i++)t*=x;r+=v*t;}return r;}
inline int dimension=0;
using M=std::vector<std::vector<Poly>>;
M zero(){return M(dimension,std::vector<Poly>(dimension));}
M id(){M a=zero();for(int i=0;i<dimension;i++)a[i][i]=Poly(1);return a;}
M add(M a,const M&b){for(int i=0;i<dimension;i++)for(int j=0;j<dimension;j++)a[i][j]=a[i][j]+b[i][j];return a;}
M scale(M a,Poly b){for(auto&r:a)for(auto&v:r)v=v*b;return a;}
M neg(M a){return scale(a,Poly(-1));}
M mul(const M&a,const M&b){M c=zero();for(int i=0;i<dimension;i++)for(int j=0;j<dimension;j++)for(int k=0;k<dimension;k++)c[i][j]=c[i][j]+a[i][k]*b[k][j];return c;}
M comm(const M&a,const M&b){return add(mul(a,b),neg(mul(b,a)));}
bool nil(const M&a){for(auto&r:a)for(auto&v:r)if(!v.c.empty())return false;return true;}
bool same(const M&a,const M&b){return nil(add(a,neg(b)));}
M perm(const J&p){M a=zero();for(int j=0;j<dimension;j++)a[p[j].get<int>()][j]=Poly(1);return a;}
J js(const M&a){J out=J::array();for(auto&r:a){J row=J::array();for(auto&v:r){J q=J::object();for(auto [k,x]:v.c)q[std::to_string(k)]=x.get_str();row.push_back(q);}out.push_back(row);}return out;}
M unused_rational_matrix(const J&a){M m=zero();for(int i=0;i<dimension;i++)for(int j=0;j<dimension;j++){R r(a[i][j].get<std::string>());r.canonicalize();m[i][j]=Poly(r);}return m;}
using Key=std::pair<int,int>;
using Jet=std::map<Key,M>;
Jet ja(Jet a,const Jet&b){for(auto [ij,m]:b){if(!a.count(ij))a[ij]=zero();a[ij]=add(a[ij],m);}return a;}
Jet scalej(Jet a,R r){for(auto &[ij,m]:a)m=scale(m,Poly(r));return a;}
Jet jm(const Jet&a,const Jet&b,int d=3){Jet c;for(auto &[ij,m]:a)for(auto &[kl,n]:b)if(ij.first+ij.second+kl.first+kl.second<=d){Key k={ij.first+kl.first,ij.second+kl.second};if(!c.count(k))c[k]=zero();c[k]=add(c[k],mul(m,n));}return c;}
Jet ji(const Jet&a,int d=3){if(!same(a.at({0,0}),id()))throw std::runtime_error("inverse needs identity constant");Jet h=a;h.erase({0,0});Jet p={{{0,0},id()}},r=p;for(int k=1;k<=d;k++){p=jm(p,h,d);r=ja(r,scalej(p,k%2?-1:1));}return r;}
Jet jl(const Jet&a,int d=3){if(!same(a.at({0,0}),id()))throw std::runtime_error("log needs identity constant");Jet h=a;h.erase({0,0});Jet p={{{0,0},id()}},r;for(int k=1;k<=d;k++){p=jm(p,h,d);r=ja(r,scalej(p,R(k%2?1:-1,k)));}return r;}
Jet du(const Jet&a){Jet r;for(auto [ij,m]:a)if(ij.first)r[{ij.first-1,ij.second}]=scale(m,Poly(ij.first));return r;}
bool jzero(const Jet&a){for(auto &[ij,m]:a)if(!nil(m))return false;return true;}
long fact(int n){long r=1;for(int k=2;k<=n;k++)r*=k;return r;}
Jet expj(const M&A,int kind){Jet r;M power=id();for(int n=0;n<=3;n++){M c=scale(power,Poly(R(1,fact(n))));if(kind==0)r[{n,0}]=c;else if(kind==1)r[{0,n}]=c;else for(int k=0;k<=n;k++)r[{k,n-k}]=scale(c,Poly(R(fact(n),fact(k)*fact(n-k))));power=mul(power,A);}return r;}
Jet bare(const M&P,int kind){Jet r={{{0,0},id()}};if(kind!=1)r[{1,0}]=P;if(kind!=0)r[{0,1}]=P;return r;}
Jet dressed(const M&A,const M&P,int kind){auto e=expj(A,kind);return jm(jm(e,bare(P,kind)),e);}

// Matrix inputs are sparse scalar polynomials: {"degree":"rational"}.
M read_matrix(const J& a){
 need(a.is_array()&&a.size()==size_t(dimension),"Matrix dimension differs from basis");M m=zero();
 for(int i=0;i<dimension;i++){
  need(a[i].is_array()&&a[i].size()==size_t(dimension),"Square matrix required");
  for(int j=0;j<dimension;j++){
   const auto& cell=a[i][j];need(cell.is_object(),"Polynomial cell object required; exact zero is {}");
   for(auto it=cell.begin();it!=cell.end();++it){
    auto key=it.key();need(key.size()==1&&key[0]>='0'&&key[0]<='8',"Input polynomial degree must be 0..8");
    R q=rxt::rational(it.value());if(q!=0)m[i][j].c[key[0]-'0']=q;
   }
  }
 }
 return m;
}
void set_dimension(const J&p){need(p.at("dimension").is_number_integer()&&p["dimension"]>=1&&p["dimension"]<=16,"Matrix dimension must be 1..16");dimension=p["dimension"].get<int>();}
M read_perm(const J&a){need(a.is_array()&&a.size()==size_t(dimension),"Permutation dimension differs");std::set<int> seen;for(const auto&x:a){need(x.is_number_integer()&&x>=0&&x<dimension,"Permutation index outside basis");need(seen.insert(x.get<int>()).second,"Permutation is not bijective");}return perm(a);}
M coefficient(const Jet&j,Key k){auto p=j.find(k);return p==j.end()?zero():p->second;}
J obstruction(const J&p){
 set_dimension(p);M A=read_matrix(p.at("phase_generator")),P=read_perm(p.at("P")),Q=read_perm(p.at("Q"));
 need(same(mul(P,P),id())&&same(mul(Q,Q),id()),"P and Q must be involutions");
 need(same(mul(mul(P,Q),P),mul(mul(Q,P),Q)),"P and Q must satisfy the braid relation");
 auto L=jm(jm(dressed(A,P,0),dressed(A,Q,2)),dressed(A,P,1));
 auto Rj=jm(jm(dressed(A,Q,1),dressed(A,P,2)),dressed(A,Q,0));
 auto defect=jl(jm(L,ji(Rj)));J coefficients=J::array();int leading=4;
 for(int n=0;n<=3;n++)for(int u=0;u<=n;u++){M m=coefficient(defect,{u,n-u});if(!nil(m))leading=std::min(leading,n);coefficients.push_back({{"u",u},{"v",n-u},{"matrix",js(m)}});}
 auto mixed=scale(comm(P,Q),Poly(R(1,2)));
 return {{"dimension",dimension},{"order",3},{"coefficient_variables",{"u","v"}},{"coefficients",coefficients},{"leading_total_degree",leading==4?J(nullptr):J(leading)},{"obstructed_through_order",leading<=3},{"remainder","O_total_degree_4"},{"ordered_mixed_log",js(mixed)},{"interpretation","Exact finite jet; zero does not assert all-order compatibility"}};
}
J commuting_log(const J&p){
 set_dimension(p);need(p.at("order").is_number_integer()&&p["order"]>=1&&p["order"]<=8,"Log order must be 1..8");int order=p["order"].get<int>();
 const auto& input=p.at("moments");need(input.is_array()&&input.size()==size_t(order+1),"Supply exactly M0 through M_order");
 std::vector<M> moments;for(auto&a:input)moments.push_back(read_matrix(a));need(same(moments[0],id()),"M0 must equal identity exactly");
 int pairs=0;for(int i=1;i<=order;i++)for(int j=i+1;j<=order;j++){need(nil(comm(moments[i],moments[j])),"Moments do not commute; recurrence admission rejected");pairs++;}
 std::vector<M> c(order+1,zero());J coeffs=J::array();for(int n=1;n<=order;n++){
  c[n]=moments[n];for(int k=1;k<n;k++)c[n]=add(c[n],scale(mul(c[k],moments[n-k]),Poly(R(-k,n))));coeffs.push_back(js(c[n]));
 }
 return {{"dimension",dimension},{"order",order},{"log_coefficients",coeffs},{"constant_coefficient",js(zero())},{"commutator_pairs_checked",pairs},{"method","EXACT_COMMUTING_LOG_RECURRENCE"},{"remainder","O(s^"+std::to_string(order+1)+")"},{"scope","Formal jet from supplied commuting moments; higher moments unspecified"}};
}
} // namespace operator_log
