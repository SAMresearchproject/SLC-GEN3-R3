#pragma once
#include "engine.hpp"
// Original integer-polynomial recurrence and norms: completed
// GEN3_RXT_RH_WEEKEND1/extensions/original_kernel_spectral_r1/search.cpp.
// No dense kernel or complete basis matrix is formed.
namespace rxt { namespace spectral_log {
using Q=mpq_class; using Z=mpz_class;
constexpr const char* kernel_id="MEAN_CUT_V1";
inline Q exact(const json& x){need(!x.is_string()||x.get_ref<const std::string&>().size()<=16384,"Exact operand exceeds 16384 characters");return rational(x);}
inline int integer(const json&p,const char*k,int fallback,int lo,int hi){auto v=p.value(k,json(fallback));need(v.is_number_integer()&&v>=lo&&v<=hi,std::string(k)+" outside supported integer bounds");return v.get<int>();}
inline bool flag(const json&p,const char*k,bool fallback){auto v=p.value(k,json(fallback));need(v.is_boolean(),std::string(k)+" must be boolean");return v.get<bool>();}
inline Q value(const json&p,const char*k,const char*d){return exact(p.value(k,json(d)));}
inline Q powq(Q b,int n){Q q=1;while(n){if(n&1)q*=b;b*=b;n>>=1;}return q;}
inline Q eigen(int k){return k?Q(1,k*(k+1)):Q(1);}
inline std::vector<Q> source(const json&p){auto&a=p.at("source");need(a.is_array()&&!a.empty()&&a.size()<=65536,"Structured source dimension must be 1..65536");std::vector<Q>v;v.reserve(a.size());for(auto&x:a)v.push_back(exact(x));return v;}
inline void kernel(const json&p){need(p.value("kernel",std::string(kernel_id))==kernel_id,"Unregistered structured kernel");}
inline json counters(){return {{"new_source_modes",0},{"reused_source_modes",0},{"source_projection_coordinates",0},{"basis_coordinates",0},{"basis_rebuilt_coordinates",0},{"source_norm_coordinates",0},{"direct_energy_cuts",0},{"log_series_terms",0}};}
inline json finish(json r){
 int s=r.at("s"),m=r.at("m");Q mass=0,F=0;for(auto&v:r.at("modes")){Q w=exact(v.at("weight"));mass+=w;F+=w*exact(v.at("eigenvalue"));}
 Q residual=exact(r.at("source_norm_squared"))-mass;need(residual>=0,"Negative exact spectral residual");need(m<s-1||residual==0,"Full spectrum must have zero residual");Q lt=m==s-1?Q(0):eigen(m+1);
 r["retained_energy"]=number(F);r["residual_norm_squared"]=number(residual);r["lambda_tail"]=number(lt);r["tail_upper"]=number(Q(residual*lt));r["retained_mode_count"]=m+1;r["full_spectrum"]=m==s-1;return r;
}
inline json validated(const json&input){
 need(input.is_object(),"Native spectral record required");json r=input;need(r.at("schema")=="GEN3_NATIVE_SPECTRAL_RECORD_V1"&&r.at("kernel")==kernel_id,"Wrong native spectral record schema/kernel");
 int s=integer(r,"s",0,1,65536),m=integer(r,"m",-1,0,std::min(s-1,256));need(r.at("modes").is_array()&&r.at("modes").size()==size_t(m+1),"Noncontiguous spectral record");need(exact(r.at("source_norm_squared"))>=0,"Negative source norm");exact(r.at("mean"));Z d=s;
 for(int k=0;k<=m;++k){auto&v=r["modes"][k];if(k){d*=Z(k)*k*(Z(s)*s-k*k)*(2*k-1);need(mpz_divisible_ui_p(d.get_mpz_t(),2*k+1),"Norm divisibility");d/=2*k+1;}
 need(v.at("k")==k&&exact(v.at("norm"))==Q(d)&&exact(v.at("eigenvalue"))==eigen(k),"Wrong registered basis norm/eigenvalue");Q A=exact(v.at("moment"));need(exact(v.at("weight"))==A*A/d,"Moment/weight mismatch");}
 need(exact(r["modes"][0]["moment"])==exact(r["mean"]),"Mean moment mismatch");auto out=finish(r);
 for(auto k:{"retained_energy","residual_norm_squared","lambda_tail","tail_upper"})need(exact(r.at(k))==exact(out.at(k)),std::string("Inconsistent certificate: ")+k);
 return out;
}
inline json build(const json&p,bool extend){
 kernel(p);auto a=source(p);int s=a.size(),target=integer(p,"max_degree",std::min(s-1,4),0,std::min(s-1,256));int budget=integer(p,"max_new_modes",257,0,257);int work=integer(p,"max_basis_coordinates",4194304,1,16777216);json c=counters(),r;int old=-1;
 if(extend){r=validated(p.at("record"));need(r.at("s")==s,"Source dimension mismatch");old=r.at("m");need(target>=old,"Refinement cannot remove retained modes");c["reused_source_modes"]=old+1;}else{Q n=0,M=0;for(auto&x:a){n+=x*x;M+=x;}r={{"schema","GEN3_NATIVE_SPECTRAL_RECORD_V1"},{"kernel",kernel_id},{"s",s},{"m",-1},{"mean",number(M)},{"source_norm_squared",number(n)},{"modes",json::array()}};c["source_norm_coordinates"]=s;need(budget>=1&&work>=s,"Admission budget must allow mean mode");}
 int m=std::min(target,old+budget);if(m>old)m=std::max(old,std::min(m,work/s-1));
 if(m>old){std::vector<Z>prev(s),cur(s,Z(1));Z d=s;
 for(int k=0;k<=m;++k){
  if(k>old){Q A=0;for(int i=0;i<s;++i)A+=a[i]*cur[i];Q w=A*A/d;r["modes"].push_back({{"k",k},{"moment",number(A)},{"norm",d.get_str()},{"weight",number(w)},{"eigenvalue",number(eigen(k))}});}
  if(k<m){for(int i=0;i<s;++i){Z next=k==0?Z(s-1-2*i):Z((2*k+1)*(s-1-2*i)*cur[i]-Z(k)*k*(Z(s)*s-k*k)*prev[i]);prev[i]=std::move(cur[i]);cur[i]=std::move(next);}int j=k+1;d*=Z(j)*j*(Z(s)*s-j*j)*(2*j-1);need(mpz_divisible_ui_p(d.get_mpz_t(),2*j+1),"Integer norm division");d/=2*j+1;}
 }
 c["new_source_modes"]=m-old;c["source_projection_coordinates"]=(m-old)*s;c["basis_coordinates"]=(m+1)*s;c["basis_rebuilt_coordinates"]=(old+1)*s;
 }
 r["m"]=m;r=finish(r);return {{"record",r},{"counters",c},{"requested_degree",target},{"status",m==target?"REQUESTED_DEGREE_COMPLETE":"CERTIFIED_BUDGET_LIMITED"}};
}
struct Interval{Q lo,hi;};
inline Interval positive_log(Q x,int n,long&terms){
 need(x>0,"Logarithm argument must be positive");if(x==1)return {0,0};bool neg=x<1;if(neg)x=1/x;
 long e=long(mpz_sizeinbase(x.get_num_mpz_t(),2))-long(mpz_sizeinbase(x.get_den_mpz_t(),2));if(e<0)e=0;need(e<=65536,"Logarithm range-reduction budget exceeded");Z two;mpz_ui_pow_ui(two.get_mpz_t(),2,e);Q y=x/two;if(y<1){--e;y*=2;}if(y>=2){++e;y/=2;}need(y>=1&&y<2,"Range reduction failed");
 auto series=[&](Q a){Q z=(a-1)/(a+1),z2=z*z,power=z,sum=0;for(int k=0;k<n;++k){sum+=power/(2*k+1);power*=z2;}terms+=n;Q tail=2*power/((2*n+1)*(1-z2));return Interval{Q(2*sum),Q(2*sum+tail)};};
 auto iy=series(y);if(e){auto i2=series(Q(2));iy.lo+=e*i2.lo;iy.hi+=e*i2.hi;}return neg?Interval{-iy.hi,-iy.lo}:iy;
}
inline json interval_json(const Interval&i){return {{"lower",number(i.lo)},{"upper",number(i.hi)},{"width",number(Q(i.hi-i.lo))}};}
inline Q epsilon(const json&p){Q e=value(p,"epsilon","1/1000000");need(e>0,"Positive absolute tolerance required");return e;}
inline json scalar(const json&p,bool direct=false){
 json c=counters();Q F,tail;if(direct){kernel(p);auto a=source(p);long s=a.size();Q M=0,P=0;for(auto&x:a)M+=x;F=M*M/s;for(long i=1;i<s;++i){P+=a[i-1];Q q=P-Q(i)*M/s;F+=q*q/(Q(i)*(s-i));}tail=0;c["direct_energy_cuts"]=s-1;}else{auto r=validated(p.at("record"));F=exact(r.at("retained_energy"));tail=exact(r.at("tail_upper"));c["reused_source_modes"]=r.at("retained_mode_count");}
 Q ref=value(p,"reference","1"),rho=value(p,"rho","1000001/1000000"),eps=epsilon(p);need(ref>0&&rho>1,"Positive reference and rho>1 required");Q lower=1+F/ref,upper=1+(F+tail)/ref,ratio=upper/lower;
 json out={{"kind","CERTIFIED_SCALAR_LOG1P"},{"reference",number(ref)},{"energy_lower",number(F)},{"energy_upper",number(Q(F+tail))},{"lower_argument",number(lower)},{"upper_argument",number(upper)},{"width_ratio",number(ratio)},{"rho",number(rho)},{"formal_tolerance_met",ratio<=rho},{"formal_enclosure",{{"lower",{{"op","log"},{"argument",number(lower)}}},{"upper",{{"op","log"},{"argument",number(upper)}}}}}};
 out["status"]=tail==0?"EXACT_SYMBOLIC":ratio<=rho?"CERTIFIED_WITHIN_TOLERANCE":"CERTIFIED_BUDGET_LIMITED";
 if(flag(p,"numerical",false)){int n=integer(p,"max_terms",64,1,512);long terms=0;auto l=positive_log(lower,n,terms),u=positive_log(upper,n,terms);Interval total{l.lo,u.hi};auto num=interval_json(total);num["epsilon"]=number(eps);num["evaluation_width"]=number(Q((l.hi-l.lo)+(u.hi-u.lo)));num["mode_tail_upper"]=number(Q(tail/(ref+F)));num["tolerance_met"]=total.hi-total.lo<=eps;out["numerical"]=num;out["status"]=total.hi-total.lo<=eps?"CERTIFIED_WITHIN_TOLERANCE":"CERTIFIED_BUDGET_LIMITED";c["log_series_terms"]=terms;}
 out["counters"]=c;return out;
}
inline json profile(const json&p){
 auto r=validated(p.at("record"));Q tau=value(p,"tau","1"),eps=epsilon(p);need(tau>=0,"tau must be nonnegative");int order=integer(p,"coefficient_order",4,1,32);Q residual=exact(r.at("residual_norm_squared")),lt=exact(r.at("lambda_tail")),delta=exact(r.at("tail_upper"));json c=counters();c["reused_source_modes"]=r.at("retained_mode_count");json terms=json::array(),coeff=json::array();Q deriv=0;std::vector<Q>sums(order+1,Q(0));
 bool numeric=flag(p,"numerical",false);int n=integer(p,"max_terms",64,1,512);long count=0;Interval retained{0,0};
 // Equal arguments share one numerical node; the mode list remains complete.
 std::map<Q,Interval> cache;
 for(auto&v:r.at("modes")){int k=v.at("k");Q w=exact(v.at("weight")),lambda=exact(v.at("eigenvalue")),arg=1+tau*lambda;terms.push_back({{"k",k},{"weight",number(w)},{"argument",number(arg)},{"moment",v.at("moment")}});deriv+=w*lambda/arg;Q pow=lambda;for(int j=1;j<=order;++j){sums[j]+=w*pow;pow*=lambda;}
  if(numeric&&w!=0){if(!cache.count(arg))cache.emplace(arg,positive_log(arg,n,count));auto z=cache.at(arg);retained.lo+=w*z.lo;retained.hi+=w*z.hi;}
 }
 Q dt=residual*lt/(1+tau*lt);for(int j=1;j<=order;++j){Q v=sums[j]/j,b=residual*powq(lt,j)/j;bool positive=j%2;Q signedv=positive?v:Q(-v);coeff.push_back({{"order",j},{"retained",number(signedv)},{"absolute_tail",number(b)},{"lower",number(positive?v:Q(-v-b))},{"upper",number(positive?Q(v+b):Q(-v))}});}
 Q linear=tau*delta;json out={{"kind","CERTIFIED_SOURCE_SPECTRAL_LOG"},{"tau",number(tau)},{"terms",terms},{"tail",{{"log_weight",number(residual)},{"log_argument",number(Q(1+tau*lt))},{"linear_upper",number(linear)}}},{"derivative",{{"lower",number(deriv)},{"upper",number(Q(deriv+dt))},{"tail_upper",number(dt)}}},{"coefficients",coeff},{"formal_series",{{"center","0"},{"order",order},{"sufficient_convergence_domain","abs(tau)<1"}}},{"epsilon",number(eps)},{"symbolic_tail_tolerance_met",linear<=eps},{"tail_decision","tau_times_energy_tail_le_epsilon"}};
 out["status"]=linear==0?"EXACT_SYMBOLIC":linear<=eps?"CERTIFIED_WITHIN_TOLERANCE":"CERTIFIED_BUDGET_LIMITED";
 if(numeric){Q tailupper=linear;if(residual!=0&&tau!=0&&lt!=0){Q bound=residual*positive_log(Q(1+tau*lt),n,count).hi;if(bound<tailupper)tailupper=bound;}Interval total{retained.lo,Q(retained.hi+tailupper)};json num=interval_json(total);num["evaluation_width"]=number(Q(retained.hi-retained.lo));num["mode_tail_upper"]=number(tailupper);num["epsilon"]=number(eps);num["tolerance_met"]=total.hi-total.lo<=eps;out["numerical"]=num;out["status"]=total.hi-total.lo<=eps?"CERTIFIED_WITHIN_TOLERANCE":"CERTIFIED_BUDGET_LIMITED";}
 c["log_series_terms"]=count;out["counters"]=c;return out;
}
inline json transport(const json&p){
 Q initial=exact(p.at("initial_energy")),current=initial,ref=value(p,"reference","1");need(initial>=0&&ref>0,"Nonnegative initial energy and positive reference required");auto&inc=p.at("increments");need(inc.is_array()&&inc.size()<=4096,"Transport chain limit 4096");json rows=json::array();Q product=1;int n=integer(p,"max_terms",64,1,512);bool numeric=flag(p,"numerical",false);long count=0;Q eps=epsilon(p);
 for(auto&step:inc){Q E=exact(step.at("E")),R=exact(step.at("R")),J=exact(step.at("J"));int endpoint=integer(step,"epsilon_0",0,0,1);Q next=current+E+R+endpoint*J;need(next>=0,"Negative reconstructed transport energy");need(step.contains("Q_next")&&exact(step.at("Q_next"))==next,"Signed transport exact-total mismatch");Q ratio=(ref+next)/(ref+current);product*=ratio;json row=step;row["Q_current"]=number(current);row["Q_next"]=number(next);row["ratio"]=number(ratio);row["formal_log"]={{"op","log"},{"argument",number(ratio)}};if(numeric)row["numerical"]=interval_json(positive_log(ratio,n,count));rows.push_back(row);current=next;}
 need(product==(ref+current)/(ref+initial),"Transport telescope mismatch");json out={{"kind","EXACT_TOTAL_SIGNED_LOG_TRANSPORT"},{"reference",number(ref)},{"initial_energy",number(initial)},{"final_energy",number(current)},{"increments",rows},{"telescope_ratio",number(product)},{"formal_log",{{"op","log"},{"argument",number(product)}}},{"status","EXACT_SYMBOLIC"}};
 if(numeric){auto z=positive_log(product,n,count);json num=interval_json(z);num["tolerance_met"]=z.hi-z.lo<=eps;num["epsilon"]=number(eps);out["numerical"]=num;out["status"]=z.hi-z.lo<=eps?"CERTIFIED_WITHIN_TOLERANCE":"CERTIFIED_BUDGET_LIMITED";}json c=counters();c["log_series_terms"]=count;out["counters"]=c;return out;
}
}} // namespace rxt::spectral_log
