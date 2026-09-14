#include <nlohmann/json.hpp>
#include <gmpxx.h>
#include <openssl/sha.h>
#include <array>
#include <map>
#include <set>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <algorithm>
using J=nlohmann::json; using Q=mpq_class;
void need(bool b,const std::string& m){if(!b)throw std::runtime_error(m);}
Q rat(long n,long d=1){Q v(n,d);v.canonicalize();return v;}
Q parse(const J& j){need(j.is_string(),"Exact rationals must be strings");Q v(j.get<std::string>());v.canonicalize();return v;}
std::string str(Q v){v.canonicalize();return v.get_str();}
Q sq(const Q& v){return v*v;}
Q power(Q v,unsigned p){Q r=1;while(p--)r*=v;return r;}
std::string digest(const std::string& x){unsigned char b[SHA256_DIGEST_LENGTH];SHA256((const unsigned char*)x.data(),x.size(),b);std::ostringstream o;for(auto v:b)o<<std::hex<<std::setw(2)<<std::setfill('0')<<unsigned(v);return o.str();}
std::string read(const std::string& p){std::ifstream f(p);need(bool(f),"Missing source: "+p);std::ostringstream s;s<<f.rdbuf();return s.str();}
J reference(const J& r){auto b=read(r.at("path"));need(digest(b)==r.at("sha256").get<std::string>(),"Source digest mismatch");return J::parse(b);}

// Exact multivariate polynomial kernel. a,b are positive supports; x,y signed.
using Exp=std::array<unsigned,4>;
struct Poly {std::map<Exp,Q> terms;};
Poly constant(Q q){Poly p;if(q!=0)p.terms[{0,0,0,0}]=q;return p;}
Poly var(unsigned k){Poly p;Exp e{};e[k]=1;p.terms[e]=1;return p;}
Poly add(Poly a,const Poly& b,Q scale=1){for(auto [e,c]:b.terms){a.terms[e]+=scale*c;if(a.terms[e]==0)a.terms.erase(e);}return a;}
Poly mul(const Poly& a,const Poly& b){Poly r;for(auto [ea,ca]:a.terms)for(auto [eb,cb]:b.terms){Exp e{};for(unsigned k=0;k<4;++k)e[k]=ea[k]+eb[k];r.terms[e]+=ca*cb;}for(auto i=r.terms.begin();i!=r.terms.end();)if(i->second==0)i=r.terms.erase(i);else ++i;return r;}
bool equal(const Poly& a,const Poly& b){return add(a,b,-1).terms.empty();}
J encode(const Poly& p){J out=J::array();for(auto [e,c]:p.terms)out.push_back({{"exponents",e},{"coefficient",str(c)}});return out;}
Q eval(const Poly& p,const std::array<Q,4>& x){Q r=0;for(auto [e,c]:p.terms){for(unsigned k=0;k<4;++k)c*=power(x[k],e[k]);r+=c;}return r;}
J square_search(){
 auto a=var(0),b=var(1),x=var(2),y=var(3);
 // Clear the known positive denominator a*b*(a+b) of child energies minus parent energy.
 auto numerator=add(mul(add(a,b),add(mul(b,mul(x,x)),mul(a,mul(y,y)))),mul(mul(a,b),mul(add(x,y,-1),add(x,y,-1))),-1);
 std::array<Poly,4> basis={mul(a,x),mul(a,y),mul(b,x),mul(b,y)};
 J matches=J::array();unsigned tried=0;
 for(int i=-2;i<=2;++i)for(int j=-2;j<=2;++j)for(int k=-2;k<=2;++k)for(int l=-2;l<=2;++l){
  std::array<int,4> c={i,j,k,l};int first=0,nz=0;for(int v:c)if(v){if(!first)first=v;++nz;}if(first<=0||nz>2)continue;
  Poly p;for(unsigned n=0;n<4;++n)p=add(p,basis[n],Q(c[n]));++tried;
  if(equal(mul(p,p),numerator))matches.push_back({{"coefficients",c},{"square",encode(p)},{"expanded_square",encode(mul(p,p))}});
 }
 need(!matches.empty(),"No exact square found in bounded grammar");
 return {{"rule","ENUMERATE_SQUARE_AND_COMPARE_ALL_COEFFICIENTS"},{"variables",{"a","b","x","y"}},
 {"basis",{"a*x","a*y","b*x","b*y"}},{"search_coefficients",{-2,-1,0,1,2}},
 {"max_nonzero_terms",2},{"candidates_evaluated",tried},{"target_numerator",encode(numerator)},{"certificates",matches},
 {"assumptions",{"a>0","b>0","x,y real"}},{"denominator","a*b*(a+b)"},
 {"conclusion","x^2/a+y^2/b-(x-y)^2/(a+b) is the generated square divided by a*b*(a+b)"},
 {"scope","UNIVERSAL_ALGEBRAIC_IDENTITY; no RH growth conclusion assigned"}};
}

// Nonnegative-polynomial substitution on the source packet's actual two reductions.
using HP=std::vector<Q>;
HP hpadd(HP a,const HP& b){a.resize(std::max(a.size(),b.size()));for(size_t i=0;i<b.size();++i)a[i]+=b[i];return a;}
HP hpmul(const HP&a,const HP&b){HP r(a.size()+b.size()-1);for(size_t i=0;i<a.size();++i)for(size_t j=0;j<b.size();++j)r[i+j]+=a[i]*b[j];return r;}
J hpenc(const HP& p){J a=J::array();for(auto q:p)a.push_back(str(q));return a;}
HP hpdec(const J& j){need(j.is_array()&&!j.empty()&&j.size()<=8,"Polynomial bound");HP p;for(auto x:j){Q q=parse(x);need(q>=0,"Substitution multiplier must be nonnegative on H>=0");p.push_back(q);}return p;}
J compose(const J& premises){
 auto A=hpdec(premises.at("gamma_from_rho")),B=hpdec(premises.at("gamma_budget")),C=hpdec(premises.at("rho_from_gamma")),D=hpdec(premises.at("rho_budget"));
 auto loop=hpmul(A,C),budget=hpadd(hpmul(A,D),B);
 bool contract=loop[0]<1;for(size_t i=1;i<loop.size();++i)if(loop[i]!=0)contract=false;
 return {{"rule","NONNEGATIVE_POLYNOMIAL_SUBSTITUTION"},{"parents",premises},{"self_coefficient",hpenc(loop)},
 {"budget_coefficient",hpenc(budget)},{"can_isolate_uniform_upper_bound",contract},
 {"frontier",contract?"CONSTANT_CONTRACTION_AVAILABLE":"NEED_SOURCE_ESTIMATE_ELIMINATING_NONCONTRACTIVE_SELF_TERM"}};
}

std::vector<int> mobius(unsigned n){std::vector<int> mu(n+1),lp(n+1),pr;mu[1]=1;for(unsigned i=2;i<=n;++i){if(!lp[i]){lp[i]=i;pr.push_back(i);mu[i]=-1;}for(int p:pr){if(uint64_t(i)*p>n)break;lp[i*p]=p;if(i%p==0){mu[i*p]=0;break;}mu[i*p]=-mu[i];}}return mu;}
unsigned root(unsigned n){unsigned r=0;while((r+1)*(r+1)<=n)++r;return r;}
struct Cell {unsigned l,h;Q W,offset;std::vector<Q> beta;};
std::vector<Cell> geometry(unsigned s){
 std::map<std::pair<unsigned,unsigned>,std::vector<unsigned>> groups;
 for(unsigned r=1;r<s;++r){unsigned side=r<=s/2?0:1;groups[{side,root(side?s-r:r)}].push_back(r);}
 std::vector<Cell> out;
 for(auto& [key,cuts]:groups){Cell c{};c.l=cuts.front();c.h=cuts.back();c.beta.resize(c.h-c.l+1);for(unsigned r:cuts){Q w=rat(1,long(r)*(s-r));c.W+=w;c.offset+=rat(r,s)*w;}Q tail=0;for(size_t j=cuts.size();j-->0;){c.beta[cuts[j]-c.l]=tail-c.offset;tail+=rat(1,long(cuts[j])*(s-cuts[j]));}out.push_back(c);}
 return out;
}
J project(unsigned s,unsigned t,bool positive_control=false){
 need(s>=1&&s<=16384&&(s&(s-1))==0&&t<=s,"Bounded original dyadic geometry");
 auto mu=mobius(2*s);std::vector<Q> prefix(t+1),prefix2(t+1);
 for(unsigned i=0;i<t;++i){Q v=positive_control?1:mu[s+i];prefix[i+1]=prefix[i]+v;prefix2[i+1]=prefix2[i]+v*v;}
 Q mean=sq(prefix[t])/s,D=prefix2[t]/s,E=mean;auto cells=geometry(s);
 for(auto c:cells){Q z=0,d=0;for(unsigned i=0;i<t;++i){Q beta=i<c.l?Q(c.W-c.offset):i>=c.h?Q(-c.offset):c.beta[i-c.l];Q v=positive_control?1:mu[s+i];z+=v*beta;d+=v*v*beta*beta;}E+=z*z/c.W;D+=d/c.W;}
 Q X=E-D,H=0;for(unsigned r=1;r<s;++r)H+=rat(1,r);
 need(D>=0&&D<=2-rat(1,s)&&E>=0,"Original trace/energy invariant");
 return {{"s",s},{"t",t},{"Qhat",str(E)},{"D_adm",str(D)},{"X_adm",str(X)},{"positive_X",str(std::max(Q(0),X))},
 {"mean_cross",str(mean-prefix2[t]/s)},{"cut_cross",str(X-mean+prefix2[t]/s)},{"H",str(H)},
 {"source",positive_control?"ALL_POSITIVE_DIAGNOSTIC":"ACTUAL_MOBIUS"},{"positive_part_after_complete_block",true}};
}

J generated_candidates(){J out=J::array();for(unsigned p=0;p<=4;++p)for(int k=-6;k<=6;++k){Q c=k<0?rat(1,1L<<(-k)):rat(1L<<k);out.push_back({{"id","P"+std::to_string(p)+"_C2pow"+std::to_string(k)},{"p",p},{"c",str(c)},{"cases",0},{"counterexamples",0},{"worst_ratio","0"},{"first_counterexample",nullptr},{"worst_case",nullptr}});}return out;}
J witness(const J& row,Q bound){return {{"s",row["s"]},{"t",row["t"]},{"positive_X",row["positive_X"]},{"bound",str(bound)},{"excess",str(parse(row["positive_X"])-bound)},{"source",row["source"]}};}
void observe(J& candidates,const J& row){need(row.at("source")=="ACTUAL_MOBIUS","Diagnostic sources cannot train actual-source candidates");Q value=parse(row.at("positive_X")),base=1+parse(row.at("H"));for(auto& c:candidates){Q bound=parse(c["c"])*power(base,c["p"]),ratio=value/bound;c["cases"]=c["cases"].get<unsigned>()+1;if(ratio>parse(c["worst_ratio"])){c["worst_ratio"]=str(ratio);c["worst_case"]=witness(row,bound);}if(value>bound){c["counterexamples"]=c["counterexamples"].get<unsigned>()+1;if(c["first_counterexample"].is_null())c["first_counterexample"]=witness(row,bound);}}}
J choose(const J& candidates){for(auto c:candidates)if(c["counterexamples"]==0)return c;return nullptr;}
J theorem_template(const J& c){
 if(c.is_null())return {{"status","NO_SURVIVOR_IN_BOUNDED_GRAMMAR"}};
 return {{"status","CONDITIONAL_UNIFORM_OBLIGATION"},{"candidate_id",c["id"]},
 {"required_new_premise","For every original dyadic s and admissible stop t, [X_adm(s,t)]_+ <= c*(1+H_(s-1))^p for ACTUAL mu, with these fixed c,p"},
 {"c",c["c"]},{"p",c["p"]},{"inference_steps",J::array({
 J{{"rule","SUM_POINTWISE_NONNEGATIVE_BOUNDS"},{"result","V_U <= c * (# original roster) * (1+H_(U-1))^p"}},
 J{{"rule","DYADIC_ROSTER_CARDINALITY"},{"result","# original roster <= 1+floor(log_2 U)"}},
 J{{"rule","HARMONIC_INTEGRAL_BOUND"},{"result","H_(U-1) <= 1+log U for U>=1"}},
 J{{"rule","FIXED_POLYLOG_IS_SUBPOWER"},{"result","For every eta>0 there is C_eta with V_U <= C_eta U^eta"}}
 })},{"source_requirement","Same original roster, baselines and common unbounded sequence; mean and cut cells retained"},
 {"scope","Sufficient candidate family; no claim this stronger all-stop bound is necessary"},
 {"unconditional_target_closed",false}};
}
J selftest(){
 auto a=var(0),b=var(1),x=var(2),y=var(3);auto p=add(mul(b,x),mul(a,y));
 need(eval(mul(p,p),{Q(2),Q(3),Q(-5),Q(7)})==1,"Signed polynomial evaluation");
 auto s=square_search();need(s["certificates"][0]["coefficients"]==J::array({0,1,1,0}),"Generated square coefficients");
 need(!equal(mul(p,p),add(mul(p,p),constant(1))),"Reject altered identity");
 J original={{"gamma_from_rho",{"2","16"}},{"gamma_budget",{"2"}},{"rho_from_gamma",{"2"}},{"rho_budget",{"2"}}};auto c=compose(original);need(c["self_coefficient"]==J::array({"4","32"})&&c["budget_coefficient"]==J::array({"6","32"})&&!c["can_isolate_uniform_upper_bound"].get<bool>(),"Noncontractive source reductions");
 original["gamma_from_rho"]={"1/4"};need(compose(original)["can_isolate_uniform_upper_bound"].get<bool>(),"Positive contraction fixture");
 bool rejected=false;try{original["gamma_from_rho"]={"-1"};compose(original);}catch(...){rejected=true;}need(rejected,"Negative multiplier rejected");
 auto r=project(2,2);need(parse(r["Qhat"])==2&&parse(r["D_adm"])==rat(3,2)&&parse(r["X_adm"])==rat(1,2),"Hand-computed original s2 mu(-1,-1) geometry");
 auto v=project(2,1);need(parse(v["Qhat"])==rat(3,4)&&parse(v["X_adm"])==0,"Stopped signed geometry");
 auto cs=generated_candidates();observe(cs,r);need(cs[0]["counterexamples"]==1,"Counterexample invalidates candidate");auto once=cs;observe(cs,v);need(cs[0]["counterexamples"]==once[0]["counterexamples"],"Passing case cannot erase counterexample");
 rejected=false;try{observe(cs,project(2,2,true));}catch(...){rejected=true;}need(rejected,"Non-Mobius control rejected from training");
 return {{"status","PASS"},{"checks",11},{"scope","Exact algebra, signed geometry, valid/invalid inference, counterexample retention and control separation"}};
}
J run(const J& p){
 need(p.at("schema")=="RH_DERIVATION_SEARCH_R1","Schema");
 auto sources=reference(p.at("source_manifest"));need(sources.at("schema")=="RH_DERIVATION_SOURCES_R1","Source binding");
 for(auto f:sources.at("files"))need(digest(read(f.at("path")))==f.at("sha256").get<std::string>(),"Bound formula changed");
 J state={{"schema","RH_DERIVATION_STATE_R1"},{"round",0},{"source_manifest_sha256",p["source_manifest"]["sha256"]},{"candidates",generated_candidates()},{"cases",J::object()}};
 if(p.contains("previous_state")){state=reference(p["previous_state"]);need(state.at("schema")=="RH_DERIVATION_STATE_R1"&&state.at("source_manifest_sha256")==p["source_manifest"]["sha256"],"Recovered state binding mismatch");}
 auto prior=state;auto selected_before=choose(state["candidates"]);J fresh=J::array();unsigned repeats=0,checks=0;
 need(p.at("questions").size()<=80,"Bounded question budget");
 for(auto q:p.at("questions")){unsigned s=q.at("s"),t=q.at("t");std::string key=std::to_string(s)+":"+std::to_string(t);if(state["cases"].contains(key)){++repeats;continue;}auto row=project(s,t);if(q.contains("reference")){auto expected=reference(q["reference"]);need(expected.at("s")==s&&expected.at("t")==t,"Reference endpoint");for(auto name:{"Qhat","D_adm","X_adm"}){need(parse(expected.at(name))==parse(row.at(name)),"Prior native projection mismatch");++checks;}}observe(state["candidates"],row);state["cases"][key]=row;fresh.push_back(row);}
 auto selected=choose(state["candidates"]);unsigned rejected=0;for(auto c:state["candidates"])rejected+=c["counterexamples"].get<unsigned>()>0;
 state["round"]=state["round"].get<unsigned>()+1;state["selected"]=selected;
 // Keep the per-scale demand frontier: a saturated small base case must not
 // prevent exploration of larger scales. Every priority is generated here.
 J questions=J::array();std::set<std::pair<unsigned,unsigned>> proposed;
 std::map<unsigned,J> frontier;
 for(auto it=state["cases"].begin();it!=state["cases"].end();++it){auto row=it.value();unsigned s=row["s"];if(!frontier.count(s)||parse(row["positive_X"])>parse(frontier[s]["positive_X"]))frontier[s]=row;}
 auto admit=[&](unsigned s,unsigned t,const std::string& why){if(s>8192||t>s||questions.size()>=8)return;auto key=std::to_string(s)+":"+std::to_string(t);if(!state["cases"].contains(key)&&proposed.insert({s,t}).second)questions.push_back({{"s",s},{"t",t},{"reason",why}});};
 for(auto it=frontier.rbegin();it!=frontier.rend();++it){unsigned s=it->first,t=it->second["t"];if(t)admit(s,t-1,"Native per-scale maximum-demand left neighbor");if(t<s)admit(s,t+1,"Native per-scale maximum-demand right neighbor");if(s<8192){admit(2*s,2*t,"Native per-scale maximum-demand scale extension");admit(2*s,s,"Native fresh mid-stop at next scale");}}
 if(questions.empty())for(auto it=frontier.rbegin();it!=frontier.rend();++it)for(unsigned t=0;t<=it->first&&questions.size()<8;++t)admit(it->first,t,"Native unvisited original stop after saturated demand neighborhoods");
 auto control=project(64,64,true);J control_results=J::array();for(auto c:state["candidates"]){Q bound=parse(c["c"])*power(Q(1)+parse(control["H"]),c["p"]);if(parse(control["positive_X"])>bound)control_results.push_back(c["id"]);}
 return {{"status","BOUNDED_SEARCH_COMPLETED"},{"engine","RH-DERIVATION-SEARCH-R1_NATIVE_CPP_GMP"},{"state",state},
 {"new_cases",fresh},{"duplicate_cases_skipped",repeats},{"prior_native_equalities",checks},
 {"candidate_count",state["candidates"].size()},{"rejected_on_actual_source",rejected},{"finite_survivors",state["candidates"].size()-rejected},
 {"selected_before",selected_before},{"selected_after",selected},{"next_questions",questions},
 {"generated_square_certificate",square_search()},{"source_reduction_search",compose(p.at("reduction_premises"))},
 {"uniform_derivation_frontier",theorem_template(selected)},
 {"geometry_only_diagnostic",{{"case",control},{"candidates_excluded_for_unrestricted_signs",control_results},{"used_to_reject_actual_source_candidates",false}}},
 {"target","For every eta>0, sum_original_roster [X_adm]_+ <= C_eta U_j^eta on the SAME original common unbounded sequence"},
 {"unconditional_uniform_estimate_derived",false}};
}
int main(){try{J q;std::cin>>q;need(q.is_array()&&q.size()==1,"One native operation per call");std::string op=q[0].at("op");J result;if(op=="RH_DERIVE_SELFTEST_R1")result=selftest();else{need(op=="RH_DERIVE_R1","Unknown native operation");result=run(q[0].at("payload"));}std::cout<<J({{"ok",true},{"result",result}}).dump()<<'\n';return 0;}catch(const std::exception& e){std::cout<<J({{"ok",false},{"error",e.what()}}).dump()<<'\n';return 1;}}
