#include "rh.hpp"
#include "rh_binding.hpp"
#include "rh_envelope.hpp"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <fstream>
#include <map>
#include <omp.h>
#include <stdexcept>
namespace rxt {
namespace {
using Q=mpq_class;
void need(bool b,const std::string& s){if(!b)throw std::invalid_argument("RH-GXT: "+s);}
Q q(long a,long b=1){Q x(a,b);x.canonicalize();return x;}
Q sq(const Q& x){return x*x;}
Q absq(const Q& x){return x<0?-x:x;}
std::string str(Q x){x.canonicalize();return x.get_str();}
json encoded(const std::map<std::string,Q>& values){json j=json::object();for(const auto& [k,v]:values)j[k]=str(v);return j;}
unsigned isqrt(unsigned n){unsigned r=unsigned(std::sqrt(double(n)));while(uint64_t(r+1)*(r+1)<=n)++r;while(uint64_t(r)*r>n)--r;return r;}
std::vector<int> mobius(unsigned n){
    std::vector<int> mu(n+1),least(n+1),primes;mu[1]=1;
    for(unsigned i=2;i<=n;++i){if(!least[i]){least[i]=int(i);primes.push_back(int(i));mu[i]=-1;}
        for(int p:primes){if(uint64_t(i)*unsigned(p)>n)break;least[i*unsigned(p)]=p;if(i%unsigned(p)==0){mu[i*unsigned(p)]=0;break;}mu[i*unsigned(p)]=-mu[i];}}
    return mu;
}
std::pair<Q,Q> log_bounds(Q x,unsigned terms=32){
    need(x>0,"Positive logarithm argument required");int power=0;
    while(x>=2){x/=2;++power;}while(x<1){x*=2;--power;}
    auto unit=[&](Q value){Q z=(value-1)/(value+1),z2=z*z,term=z,sum=0;
        for(unsigned k=0;k<terms;++k){sum+=term/q(2*k+1);term*=z2;}
        Q lower=2*sum,upper=lower+2*term/(q(2*terms+1)*(1-z2));return std::make_pair(lower,upper);};
    auto a=unit(x),b=unit(Q(2));
    if(power>=0)return {a.first+power*b.first,a.second+power*b.second};
    return {a.first+power*b.second,a.second+power*b.first};
}
json roster(unsigned U,const Q& kappa){
    need(kappa>=1,"Original kappa must be at least one");Q factorial=1,e=1;
    for(unsigned i=1;i<=40;++i){factorial*=i;e+=1/factorial;}
    Q elo=e,ehi=e+q(42,41)/(factorial*41);
    auto lower=log_bounds(elo+U),upper=log_bounds(ehi+U);
    Q cmin=U/(kappa*sq(upper.second)),cmax=U/(kappa*sq(lower.first));
    auto dyadic=[](Q x){unsigned s=1;while(q(2L*s)<=x&&s<(1u<<30))s*=2;return s;};
    unsigned first=dyadic(cmin);need(first==dyadic(cmax),"Original roster cutoff needs a tighter logarithm interval");
    json scales=json::array();Q tau=0;for(unsigned s=first;s<=U;s*=2){scales.push_back(s);tau+=2-q(1,s);if(s>U/2)break;}
    return {{"U",U},{"kappa",str(kappa)},{"scales",scales},{"tau",str(tau)},
            {"log_e_plus_U_interval",json::array({str(lower.first),str(upper.second)})},
            {"cutoff_interval",json::array({str(cmin),str(cmax)})},{"cutoff_backend","EXACT_RATIONAL_LOG_SERIES_INTERVAL"}};
}
struct Cell {unsigned id,l,h;std::vector<unsigned> cuts;std::vector<Q> beta;Q W,offset,before,after,trace;};
std::vector<Cell> geometry(unsigned s,unsigned workers){
    std::map<std::pair<unsigned,unsigned>,std::vector<unsigned>> groups;
    for(unsigned r=1;r<s;++r){unsigned side=r<=s/2?0:1;groups[{side,isqrt(side?s-r:r)}].push_back(r);}
    std::vector<Cell> out(groups.size());std::vector<std::vector<unsigned>> cut_groups;for(const auto& item:groups)cut_groups.push_back(item.second);
    #pragma omp parallel for num_threads(workers) schedule(dynamic)
    for(size_t group=0;group<cut_groups.size();++group){const auto& cuts=cut_groups[group];Cell c{};c.id=group;c.cuts=cuts;c.l=cuts.front();c.h=cuts.back();
        std::vector<Q> weights;for(auto r:cuts){auto w=q(1,long(r)*(s-r));weights.push_back(w);c.W+=w;c.offset+=r*w/q(s);}
        c.before=c.W-c.offset;c.after=-c.offset;c.beta.resize(c.h-c.l+1);Q suffix=0;
        for(size_t j=cuts.size();j-->0;){c.beta[cuts[j]-c.l]=suffix-c.offset;suffix+=weights[j];}
        c.trace=c.l*sq(c.before)+(s-c.h)*sq(c.after);for(unsigned i=c.l;i<c.h;++i)c.trace+=sq(c.beta[i-c.l]);c.trace/=c.W;
        out[group]=std::move(c);}
    return out;
}
struct Projection {std::map<std::string,Q> values;json cells;std::vector<Q> energies,diagonal,feedback;};
Projection project(const std::vector<Q>& source,unsigned s,unsigned t,bool history,unsigned workers,std::atomic<uint64_t>& progress){
    need(source.size()==s,"Full source block required");auto cells=geometry(s,workers);
    std::vector<Q> prefix(t+1),prefix2(t+1);for(unsigned i=0;i<t;++i){prefix[i+1]=prefix[i]+source[i];prefix2[i+1]=prefix2[i]+sq(source[i]);}
    struct Part {Q E,D,Z,full;std::vector<Q> d,f,e;};std::vector<Part> parts(cells.size());std::exception_ptr error;
    #pragma omp parallel for num_threads(workers) schedule(dynamic)
    for(size_t j=0;j<cells.size();++j){try{const auto& c=cells[j];auto& p=parts[j];
        unsigned l=std::min(t,c.l),h=std::min(t,c.h);
        p.Z=c.before*prefix[l]+c.after*(prefix[t]-prefix[h]);
        p.D=sq(c.before)*prefix2[l]+sq(c.after)*(prefix2[t]-prefix2[h]);
        for(unsigned i=l;i<h;++i){p.Z+=c.beta[i-c.l]*source[i];p.D+=sq(c.beta[i-c.l]*source[i]);}
        p.E=sq(p.Z)/c.W;p.D/=c.W;
        Q direct=0;for(unsigned r:c.cuts){Q centered=prefix[std::min(t,r)]-q(r,s)*prefix[t];direct+=centered/q(long(r)*(s-r));p.full+=sq(centered)/q(long(r)*(s-r));}
        need(direct==p.Z,"Ordered weighted contraction differs from original cuts");
        if(history){Q Z=0;p.d.resize(t);p.f.resize(t);p.e.resize(t);
            for(unsigned i=0;i<t;++i){Q b=i<c.l?c.before:i>=c.h?c.after:c.beta[i-c.l];Q a=source[i],d=sq(a*b)/c.W,f=2*a*b*Z/c.W,old=sq(Z)/c.W;Z+=a*b;p.d[i]=d;p.f[i]=f;p.e[i]=sq(Z)/c.W;need(p.e[i]-old==d+f,"Cell accumulation identity");}}
        ++progress;
    }catch(...){
        #pragma omp critical
        {if(!error)error=std::current_exception();}
    }}
    if(error)std::rethrow_exception(error);
    Projection result;auto& v=result.values;Q M=prefix[t],N=prefix2[t],mean=sq(M)/q(s),D=N/q(s),E=mean,full=mean,trace=1,tail=q(1,s),active=0,activecross=0;
    result.cells=json::array();
    for(size_t j=0;j<cells.size();++j){const auto& c=cells[j];const auto& p=parts[j];E+=p.E;D+=p.D;full+=p.full;trace+=c.trace;
        auto region=c.l>=t?"POST_STOP":c.h<t?"PRE_STOP":"STRADDLING";
        if(c.l>=t)tail+=sq(c.before)/c.W;else{active+=p.E;activecross+=p.E-p.D;}
        result.cells.push_back({{"cell",c.id},{"l",c.l},{"h",c.h},{"region",region},{"W",str(c.W)},{"Z",str(p.Z)},{"energy",str(p.E)},{"diagonal",str(p.D)},{"cross",str(p.E-p.D)},{"trace",str(c.trace)},{"tail_factor",str(sq(c.before)/c.W)}});
    }
    Q X=E-D;need(sq(M)*tail+active==E&&(sq(M)-N)*tail+activecross==X,"Complete signed region identity");
    v={{"M",M},{"N",N},{"Q",full},{"Qhat",E},{"residual",full-E},{"D_adm",D},{"X_adm",X},{"positive_X",std::max(Q(0),X)},
       {"mean_energy",mean},{"mean_diagonal",N/q(s)},{"mean_cross",mean-N/q(s)},{"projected_trace",trace},{"full_trace",2-q(1,s)},
       {"known_tail_factor",tail},{"known_mean_tail_energy",sq(M)*tail},{"known_mean_tail_cross",(sq(M)-N)*tail},
       {"active_energy",active},{"active_cross",activecross},{"active_to_one_plus_mean",active/(1+mean)}};
    if(history){result.energies.resize(t+1);result.diagonal.resize(t);result.feedback.resize(t);Q totalD=0,totalF=0;
        for(unsigned i=0;i<t;++i){Q a=source[i],d=sq(a)/q(s),f=2*a*prefix[i]/q(s),direct=sq(prefix[i+1])/q(s);
            for(const auto& p:parts){d+=p.d[i];f+=p.f[i];direct+=p.e[i];}
            totalD+=d;totalF+=f;result.energies[i+1]=result.energies[i]+d+f;result.diagonal[i]=d;result.feedback[i]=f;
            need(result.energies[i+1]==direct&&direct==totalD+totalF,"Full original admission recurrence");++progress;
        }
        need(result.energies.back()==E,"History endpoint differs");}
    return result;
}
json accumulation(const Projection& p,const std::vector<Q>& source,unsigned s,const Q& base){
    need(base>0,"Fixed positive baseline required");Q H=0;for(unsigned k=1;k<s;++k)H+=q(1,k);
    Q up=1,down=1,peak=base,D=0,X=0,Phi=0,maxstrain=-1,minmargin=0;json rows=json::array(),peak_ties=json::array({0}),strain_ties=json::array(),violations=json::array();
    for(unsigned i=0;i<p.diagonal.size();++i){Q before=base+p.energies[i],after=base+p.energies[i+1],delta=p.diagonal[i],F=p.feedback[i],jump=delta+F;
        Q loss=sq(jump)/(2*before*std::max(before,after));Phi+=F/before-loss;D+=delta;X+=F;
        Q ratio=after/before;if(ratio>1)up*=ratio;else if(ratio<1)down/=ratio;
        if(after>peak){peak=after;peak_ties=json::array();}if(after==peak)peak_ties.push_back(i+1);
        Q bound=H*D/base,margin=bound-Phi;if(margin<0)violations.push_back(i+1);minmargin=std::min(minmargin,margin);
        if(D>0){Q strain=base*Phi/(H*D);if(strain>maxstrain){maxstrain=strain;strain_ties=json::array();}if(strain==maxstrain)strain_ties.push_back(i+1);}
        rows.push_back({{"t",i},{"n",s+i},{"mu",str(source[i])},{"d_raw",str(delta)},{"f_raw",str(F)},{"d",str(delta/before)},{"f",str(F/before)},
                       {"D",str(D)},{"X",str(X)},{"Q",str(p.energies[i+1])},{"A_before",str(before)},{"A_after",str(after)},{"loss",str(loss)},{"Phi",str(Phi)},{"C1_margin",str(margin)}});
    }
    Q net=(base+p.energies.back())/base;need(up/down==net,"Exact U-D=L accumulation identity");
    return {{"history_role","ORIGINAL_ADMISSION"},{"fixed_base",str(base)},{"U",log_value(up)},{"D",log_value(down)},{"V",log_value(up*down)},
            {"L",log_value(net)},{"M",log_value(peak/base)},{"maximum_ties",peak_ties},{"Phi",str(Phi)},{"C1_margin",str(H*D/base-Phi)},
            {"C1_minimum_margin",str(minmargin)},{"C1_maximum_strain",str(maxstrain)},{"C1_maximum_strain_ties",strain_ties},{"C1_violating_prefixes",violations},
            {"C1_status",violations.empty()?"PASSES_RETAINED_PREFIXES":"CANDIDATE_COUNTEREXAMPLE"},{"admissions",rows}};
}
std::vector<Q> block(const std::vector<int>& mu,unsigned s){std::vector<Q> b(s);for(unsigned i=0;i<s;++i)b[i]=mu[s+i];return b;}
}

json Riemann::compute(const json& p){
    auto started=std::chrono::steady_clock::now();progress=0;
    unsigned s=p.at("s"),t=p.at("t");need(s>=8&&s<=131072&&!(s&(s-1))&&t<=s,"Use dyadic scales 8..131072 and original stops 0..s");
    std::string route=p.value("route",std::string("WEIGHTED"));need(route=="BASELINE"||route=="WEIGHTED"||route=="ACCUMULATION"||route=="QUARTIC"||route=="COFACTOR"||route=="HARMONIC"||route=="ROSTER","Unknown source approach");
    need(p.contains("question")&&!p["question"].get<std::string>().empty(),"Retain a concrete RH derivation question");
    bool history=route=="ACCUMULATION"||p.value("history",false);need(!history||t<=256,"Use at most 256 exact full-admission prefixes per history operation; endpoint studies retain arbitrary original stops");
    auto mu=mobius(2*s-1);auto original=block(mu,s);std::string source_bytes;for(auto x:mu)source_bytes.push_back(char(x+1));
    auto primary=project(original,s,t,history,workers,progress);need(primary.values["residual"]>=0&&primary.values["residual"]<=8,"Original projection residual exceeds its established bound");
    need(primary.values["D_adm"]<=primary.values["projected_trace"]&&primary.values["projected_trace"]<=2-q(1,s),"Original admission trace identity");
    json result={{"schema","RH_GXT_RESULT_V1"},{"version",RH_VERSION},{"status","PASS"},{"route",route},{"s",s},{"t",t},{"question",p["question"]},
        {"source_binding",{{"bundle_sha256",RH_BUNDLE_SHA},{"mobius_prefix_sha256",hash(source_bytes)},{"source_range",json::array({s,2*s-1})},{"definition","mu(1)=1; sum_(d|n)mu(d)=1_(n=1)"}}},
        {"readouts",encoded(primary.values)},{"cells",primary.cells},{"uniform_bound_status","OPEN"},{"closure_obligation",p.value("closure_obligation",std::string("Original uniform signed-growth estimate"))}};
    if(route=="BASELINE"){
        unsigned U=p.value("original_U",2*s-1);need(U>=s&&U<=262143&&t<=std::min(s,U-s+1),"Original U must contain this endpoint");
        auto r=roster(U,rational(p.value("kappa",json("1"))));need(std::find(r["scales"].begin(),r["scales"].end(),json(s))!=r["scales"].end(),"Original roster must contain studied scale");
        Q b=rational(r["tau"]),H=rh_envelope::harmonic(s),D=primary.values["D_adm"],X=primary.values["X_adm"],N=primary.values["N"],radius=N*D;
        Q a=H/s+q(1,long(s)*s),global=rh_envelope::geometric_factor(s,b);
        Q local=radius/(b+radius)+q(4,3)*(a+2*rh_envelope::root_upper(radius*a))/b,g=std::min(global,local),margin=H*D-X-g*D;
        need(primary.values["Qhat"]<=radius,"Source-count endpoint radius differs");
        result["original_roster"]={{"definition",r},{"baseline_scope","Every B>=original tau; earlier-block energies unnecessary for this certificate"}};
        result["baseline_certificate"]={{"status",margin>=0?"C1_ALL_ADMISSIBLE_BASELINES":"UNRESOLVED_BY_SUFFICIENT_ENDPOINT_BOUND"},{"margin",str(margin)},{"factor",str(g)},
          {"demand",str(D>0?Q((X+g*D)/(H*D)):Q(0))},{"pair_spread",str(radius-primary.values["Qhat"])},{"source_count",str(N)},
          {"derivation","Native G2/G5 source-count endpoint certificate; exact outward rational square-root bound"}};
    }
    if(history||route=="ROSTER"){
        unsigned U=p.value("original_U",2*s-1);need(U>=s&&U<=262143&&t<=std::min(s,U-s+1),"Original final U must contain the studied block prefix");auto r=roster(U,rational(p.value("kappa",json("1"))));
        Q base=rational(r["tau"]),energy=0,positive=0;json blocks=json::array();
        for(const auto& scale:r["scales"]){unsigned a=scale;if(a>s){blocks.push_back({{"s",a},{"t",0},{"role","FUTURE_BLOCK_RETAINED_ZERO"}});continue;}auto z=a==s?primary:project(block(mu,a),a,a,false,workers,progress);
            if(a<s)base+=z.values["Qhat"];energy+=z.values["Qhat"];positive+=z.values["positive_X"];blocks.push_back({{"s",a},{"t",a==s?t:a},{"readouts",encoded(z.values)}});}
        need(std::find(r["scales"].begin(),r["scales"].end(),json(s))!=r["scales"].end(),"Studied block must belong to the original final roster");
        result["original_roster"]={{"definition",r},{"blocks",blocks},{"Qhat_sum",str(energy)},{"positive_signed_interaction_sum",str(positive)},
            {"fixed_base_before_top",str(base)},{"complete_final_roster",r["scales"].back()==s&&t==U-s+1}};
        if(history)result["accumulation"]=accumulation(primary,original,s,base);
    }
    if(route=="QUARTIC"||route=="COFACTOR"){
        unsigned u=isqrt(isqrt(2*s-1)),A=u+1;Q H=0;for(unsigned n=1;n<=u;++n)H+=q(mu[n],n);
        std::vector<Q> f(A+1);for(unsigned n=1;n<=u;++n)f[n]=mu[n];f[A]=-q(A)*H;
        std::map<unsigned,Q> c;for(unsigned a=1;a<=A;++a)for(unsigned b=1;b<=A;++b)c[a*b]+=f[a]*f[b];
        std::vector<Q> low(s),transport(s);
        for(const auto& [k,value]:c)for(unsigned n=((s+k-1)/k)*k;n<2*s;n+=k)low[n-s]+=value;
        for(unsigned i=0;i<s;++i)transport[i]=original[i]+low[i];
        auto lo=project(low,s,t,false,workers,progress),tr=project(transport,s,t,false,workers,progress);
        Q cross=tr.values["Qhat"]-primary.values["Qhat"]-lo.values["Qhat"];
        result["quartic"]={{"u",u},{"A",A},{"auxiliary_f_A",str(f[A])},{"smaller_source_cutoff",(2*s-1)/(A*A)},
            {"quadratic",encoded(lo.values)},{"transport",encoded(tr.values)},{"source_quadratic_cross",str(cross)},
            {"transport_zero_admissions",json::array()},{"identity","R=mu+a2 with the original auxiliary harmonic completion"}};
        for(unsigned i=0;i<t;++i)if(transport[i]==0)result["quartic"]["transport_zero_admissions"].push_back(s+i);
        if(route=="COFACTOR"){
            std::vector<unsigned> primes;for(unsigned n=2;n<=A;++n){bool prime=true;for(unsigned d=2;d*d<=n;++d)if(n%d==0){prime=false;break;}if(prime)primes.push_back(n);}
            std::vector<Q> small(s),large(s);unsigned checks=0;
            for(unsigned i=0;i<s;++i){unsigned n=s+i,m=n;for(unsigned prime:primes)while(m%prime==0)m/=prime;unsigned k=n/m;Q w=0;for(const auto& [d,x]:c)if(k%d==0)w+=x;
                Q value=mu[k]*mu[m]+w;need(value==transport[i],"Exact smooth-cofactor transport identity");++checks;
                if(k<A){need(value==mu[k]*(1+mu[m]),"Small smooth-cofactor support identity");small[i]=value;++checks;}else large[i]=value;}
            auto a=project(small,s,t,false,workers,progress),b=project(large,s,t,false,workers,progress);
            result["cofactor"]={{"small",encoded(a.values)},{"complement",encoded(b.values)},{"cross",str(tr.values["Qhat"]-a.values["Qhat"]-b.values["Qhat"])},{"exact_identities",checks}};
        }
    }
    if(route=="HARMONIC"){
        unsigned u=isqrt(2*s-1);Q H=0;for(unsigned n=1;n<=u;++n)H+=q(mu[n],n);Q density=-H*H;
        std::vector<int> c(2*s),reconstructed(s);
        for(unsigned a=1;a<=u;++a)for(unsigned b=a;b<=u;++b)if(a*b<2*s)c[a*b]+=(a==b?1:2)*mu[a]*mu[b];
        for(unsigned k=1;k<2*s;++k)if(c[k])for(unsigned n=((s+k-1)/k)*k;n<2*s;n+=k)reconstructed[n-s]-=c[k];
        std::vector<Q> drift(s,density),discrepancy(s);for(unsigned i=0;i<s;++i){need(reconstructed[i]==mu[s+i],"Complete harmonic divisor reconstruction");discrepancy[i]=original[i]-density;}
        auto a=project(drift,s,t,false,workers,progress),b=project(discrepancy,s,t,false,workers,progress);
        result["harmonic"]={{"u",u},{"S",str(H)},{"density",str(density)},{"drift",encoded(a.values)},{"discrepancy",encoded(b.values)},
            {"cross",str(primary.values["Qhat"]-a.values["Qhat"]-b.values["Qhat"])},{"exact_source_identities",s}};
    }
    Q feedback=absq(primary.values["X_adm"])/(1+primary.values["D_adm"]);
    if(result.contains("accumulation"))feedback=absq(rational(result["accumulation"]["C1_maximum_strain"]));
    if(result.contains("quartic"))feedback=absq(rational(result["quartic"]["source_quadratic_cross"]))/
        (1+primary.values["Qhat"]+rational(result["quartic"]["quadratic"]["Qhat"]));
    if(result.contains("harmonic"))feedback=absq(rational(result["harmonic"]["cross"]))/
        (1+rational(result["harmonic"]["drift"]["Qhat"])+rational(result["harmonic"]["discrepancy"]["Qhat"]));
    json display=json::object();for(const auto& [key,value]:primary.values)display[key]=value.get_d();
    if(result.contains("accumulation")){display["C1_status"]=result["accumulation"]["C1_status"];display["C1_maximum_strain"]=rational(result["accumulation"]["C1_maximum_strain"]).get_d();display["C1_violating_prefixes"]=result["accumulation"]["C1_violating_prefixes"];}
    if(result.contains("baseline_certificate")){const auto& certificate=result["baseline_certificate"];display["C1_status"]=certificate["status"];display["C1_endpoint_demand"]=rational(certificate["demand"]).get_d();display["C1_endpoint_margin"]=rational(certificate["margin"]).get_d();}
    result["display_approximation"]=display;
    result["feedback"]=str(feedback);result["execution"]={{"backend","NATIVE_CPP_OPENMP_GMP"},{"cpu_workers",workers},{"completed_components",progress.load()},
        {"wall_seconds",std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()}};return result;
}

json Engine::rh(const std::string& op,const json& p){
    need(bool(store_),"Attach the shared durable native machine");
    if(op=="RH_COMPILE"){
        auto path=std::filesystem::path(p.at("directory").get<std::string>());auto bundle=read_json(path/"BUNDLE.json");
        std::ifstream input(path/"BUNDLE.json");std::string bytes((std::istreambuf_iterator<char>(input)),{});need(hash(bytes)==RH_BUNDLE_SHA,"Source bundle differs");
        for(auto it=bundle["inputs"].begin();it!=bundle["inputs"].end();++it){std::ifstream file(path/it.key());std::string data((std::istreambuf_iterator<char>(file)),{});need(hash(data)==it.value()["sha256"].get<std::string>(),"Bound source input differs: "+it.key());}
        if(state_.contains("rh_source"))need(state_["rh_source"]["bundle_sha256"]==RH_BUNDLE_SHA,"Another RH source is already attached");
        auto next=state_;next["rh_source"]={{"directory",path.string()},{"bundle_sha256",RH_BUNDLE_SHA},{"version",RH_VERSION},{"basis","RH-GEN3-GROWTH-V4"}};
        if(!next.contains("rh_results")){next["rh_results"]=json::object();next["rh_learning"]=json::object();next["rh_pending"]=nullptr;}
        store_->commit(next);state_=std::move(next);
    }
    need(state_.contains("rh_source"),"Compile the RH source first");
    if(!rh_)rh_=std::make_unique<Riemann>(std::max(1u,resources_.cpu_threads>3?resources_.cpu_threads-3:resources_.cpu_threads));
    if(op=="RH_COMPILE"||op=="RH_STATUS"){
        json learned=state_["rh_learning"];
        if(p.value("compact",false))for(auto it=learned.begin();it!=learned.end();++it){auto& value=it.value();if(value.contains("reward")){value.erase("reward");value["reward_storage"]="EXACT_NATIVE_LEARNING";}}
        return {{"version",RH_VERSION},{"source",state_["rh_source"]},{"completed_cases",state_["rh_results"].size()},
            {"learning",learned},{"pending",state_["rh_pending"]},{"pending_batch",state_.value("rh_pending_batch",json(nullptr))},{"completed_components",rh_->progress.load()},
            {"cpu_workers",rh_->workers},{"batch_limit",std::min(20u,rh_->workers)},
            {"operations",json::array({"RH_SUBMIT","RH_POLL","RH_RESULT","RH_SELECT","RH_STATUS","RH_BATCH_SUBMIT","RH_BATCH_POLL"})},
            {"objective","RH closure"},{"uniform_bound_status","OPEN"}};
    }
    auto brief=[](const json& r){json out;for(auto key:{"route","s","t","display_approximation","closure_obligation","execution","source_binding"})out[key]=r.at(key);
        if(r.contains("accumulation")){out["accumulation"]=json::object();for(auto key:{"C1_status","C1_maximum_strain_ties","C1_violating_prefixes"})out["accumulation"][key]=r["accumulation"][key];}return out;};
    if(op=="RH_BATCH_SUBMIT"){
        const auto& jobs=p.at("jobs");need(jobs.is_array()&&!jobs.empty()&&jobs.size()<=std::min(20u,rh_->workers),"Bounded native independent batch required");need(state_["rh_pending"].is_null(),"Finish the legacy pending source calculation first");
        std::set<std::string> ids;
        for(const auto& job:jobs){auto id=job.at("job_id").get<std::string>();need(!id.empty()&&id.size()<=120&&ids.insert(id).second,"Distinct bounded batch request identities required");need(!state_["rh_results"].contains(id),"Completed request must be recovered from native results");}
        auto pending=state_.value("rh_pending_batch",json(nullptr));need(pending.is_null()||pending==p,"Another source batch is pending");
        if(!rh_->batch_pending.valid()){
            auto next=state_;next["rh_pending_batch"]=p;store_->commit(next);state_=std::move(next);rh_->progress=0;
            rh_->batch_pending=std::async(std::launch::async,[this,jobs]{std::vector<std::future<json>> lanes;
                for(const auto& job:jobs)lanes.push_back(std::async(std::launch::async,[this,job]{Riemann lane(1);auto result=lane.compute(job);rh_->progress.fetch_add(lane.progress.load());return result;}));
                json answers=json::array();for(auto& lane:lanes)answers.push_back(lane.get());return answers;});
        }
        return {{"status","RUNNING"},{"jobs",jobs.size()},{"cpu_lanes",jobs.size()}};
    }
    if(op=="RH_BATCH_POLL"){
        auto pending=state_.value("rh_pending_batch",json(nullptr));need(!pending.is_null(),"No source batch is pending");
        if(!rh_->batch_pending.valid())return {{"status","NEEDS_RESUME"},{"request",pending}};
        if(rh_->batch_pending.wait_for(std::chrono::seconds(0))!=std::future_status::ready)return {{"status","RUNNING"},{"completed_components",rh_->progress.load()}};
        auto results=rh_->batch_pending.get();auto next=state_;json completed=json::array();
        for(size_t i=0;i<results.size();++i){const auto& request=pending["jobs"][i];const auto& result=results[i];auto id=request["job_id"].get<std::string>(),route=request["route"].get<std::string>(),ref=store_->put(result);
            next["rh_results"][id]={{"request_sha256",hash(request.dump())},{"result",ref},{"summary",store_->put(brief(result))},{"request",request}};auto learned=next["rh_learning"].value(route,json::object());learned["visits"]=learned.value("visits",0u)+1;learned["reward"]=str(rational(result["feedback"]));learned["latest_source_result"]=ref;next["rh_learning"][route]=learned;
            completed.push_back({{"job_id",id},{"result_object",ref},{"summary",brief(result)},{"request",request}});
        }
        next["rh_pending_batch"]=nullptr;next["sequence"]=state_["sequence"].get<uint64_t>()+results.size();auto root=store_->commit(next);state_=std::move(next);
        return {{"status","COMPLETE"},{"results",completed},{"checkpoint",{{"root",root}}}};
    }
    if(op=="RH_RESULT"){auto id=p.at("job_id").get<std::string>();const auto& saved=state_.at("rh_results").at(id);if(p.value("summary",false)){if(saved.contains("summary"))return store_->get(saved["summary"].get<std::string>());return brief(store_->get(saved["result"].get<std::string>()));}return store_->get(saved["result"].get<std::string>());}
    if(op=="RH_SELECT"){
        auto candidates=p.at("candidates");need(candidates.is_array()&&!candidates.empty()&&candidates.size()<=4096,"Supply a bounded pending frontier");unsigned count=p.value("count",1u);need(count>=1&&count<=std::min(20u,rh_->workers),"Bounded independent selection count required");
        std::map<std::string,Q> rewards;std::map<std::string,unsigned> visits;
        for(const auto& candidate:candidates){auto route=candidate.at("route").get<std::string>();if(!rewards.count(route)){auto value=state_["rh_learning"].value(route,json::object());rewards[route]=rational(value.value("reward",json("0")));visits[route]=value.value("visits",0u);}}
        json selected=json::array(),rounds=json::array();
        for(unsigned slot=0;slot<count&&!candidates.empty();++slot){Q best=-1;json ties=json::array();size_t chosen=0;
            std::map<std::string,Q> scores;
            for(size_t i=0;i<candidates.size();++i){const auto& candidate=candidates[i];auto route=candidate.at("route").get<std::string>();
                if(!scores.count(route))scores[route]=(1+rewards.at(route))/(1+q(visits.at(route)));
                const Q& score=scores.at(route);if(score>best){best=score;ties=json::array();chosen=i;}if(score==best)ties.push_back(candidate);
            }
            auto choice=candidates[chosen];selected.push_back(choice);rounds.push_back(ties);auto route=choice["route"].get<std::string>();++visits[route];candidates.erase(candidates.begin()+chosen);
        }
        if(count==1){json out={{"selected",selected[0]},{"ties",rounds[0]},{"policy","Exact acquired route feedback with an exploration denominator"}};
            if(!p.value("compact",false)){json scores=json::array();for(const auto& candidate:p.at("candidates")){auto v=state_["rh_learning"].value(candidate.at("route").get<std::string>(),json::object());scores.push_back(str((1+rational(v.value("reward",json("0"))))/(1+q(v.value("visits",0u)))));}out["scores"]=scores;out["learning"]=state_["rh_learning"];}return out;}

        return {{"selected_jobs",selected},{"round_ties",rounds},{"policy","Exact acquired route feedback with temporary within-batch visit reservations; source rewards update only after native completion"}};
    }
    if(op=="RH_SUBMIT"){
        need(state_.value("rh_pending_batch",json(nullptr)).is_null(),"Finish the independent source batch first");
        auto id=p.at("job_id").get<std::string>();need(!id.empty()&&id.size()<=120,"Bounded job identity required");
        if(state_["rh_results"].contains(id)){need(state_["rh_results"][id]["request_sha256"].get<std::string>()==hash(p.dump()),"Job identity has different source parameters");return {{"status","COMPLETE"},{"job_id",id},{"result_object",state_["rh_results"][id]["result"]}};}
        if(!state_["rh_pending"].is_null())need(state_["rh_pending"]==p,"Another RH job is pending");
        if(!rh_->pending.valid()){auto next=state_;next["rh_pending"]=p;store_->commit(next);state_=std::move(next);rh_->request=p;rh_->pending=std::async(std::launch::async,[this,p]{return rh_->compute(p);});}
        return {{"status","RUNNING"},{"job_id",id},{"cpu_workers",rh_->workers}};
    }
    need(op=="RH_POLL","Unknown RH operation");need(!state_["rh_pending"].is_null(),"No pending RH job");
    if(!rh_->pending.valid())return {{"status","NEEDS_RESUME"},{"request",state_["rh_pending"]}};
    if(rh_->pending.wait_for(std::chrono::seconds(0))!=std::future_status::ready)return {{"status","RUNNING"},{"job_id",state_["rh_pending"]["job_id"]},{"completed_components",rh_->progress.load()}};
    auto request=state_["rh_pending"];auto result=rh_->pending.get();auto ref=store_->put(result),id=request.at("job_id").get<std::string>(),route=request.at("route").get<std::string>();
    auto next=state_;next["rh_results"][id]={{"request_sha256",hash(request.dump())},{"result",ref},{"summary",store_->put(brief(result))},{"request",request}};next["rh_pending"]=nullptr;
    auto learned=next["rh_learning"].value(route,json::object());learned["visits"]=learned.value("visits",0u)+1;learned["reward"]=str(rational(result["feedback"]));learned["latest_source_result"]=ref;
    next["rh_learning"][route]=learned;next["sequence"]=state_["sequence"].get<uint64_t>()+1;auto root=store_->commit(next);state_=std::move(next);
    if(p.value("compact",false))return {{"status","COMPLETE"},{"job_id",id},{"result_object",ref},{"summary",brief(result)},{"request",request},{"checkpoint",{{"root",root}}}};
    return {{"status","COMPLETE"},{"job_id",id},{"result_object",ref},{"result",result},{"checkpoint",{{"root",root}}}};
}
}
