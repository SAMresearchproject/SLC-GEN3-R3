#define main retained_derivation_main
#include "prior.cpp"
#undef main
using Z=mpz_class;
struct Basis {long s,m;std::vector<std::vector<Z>> p;std::vector<Z>d;};
Basis basis(long s,long m){
 Basis b{s,m,{}, {}};b.p.resize(m+1,std::vector<Z>(s));b.d.resize(m+1);b.d[0]=s;
 for(long i=0;i<s;++i)b.p[0][i]=1;
 if(m){for(long i=0;i<s;++i)b.p[1][i]=s-1-2*i;}
 for(long k=1;k<=m;++k){b.d[k]=b.d[k-1]*k*k*(s*s-k*k)*(2*k-1);need(mpz_divisible_ui_p(b.d[k].get_mpz_t(),2*k+1),"Integer norm division");b.d[k]/=2*k+1;
  if(k<m)for(long i=0;i<s;++i)b.p[k+1][i]=(2*k+1)*(s-1-2*i)*b.p[k][i]-k*k*(s*s-k*k)*b.p[k-1][i];}
 return b;
}
std::vector<int> source(long s,long t){auto mu=mobius(2*s);std::vector<int>a(s);for(long i=0;i<t;++i)a[i]=mu[s+i];return a;}
Q full(const std::vector<int>&a){long s=a.size(),M=0,P=0;for(int v:a)M+=v;Q q=rat(M*M,s);for(long r=1;r<s;++r){P+=a[r-1];q+=sq(Q(P)-rat(r*M,s))*rat(1,r*(s-r));}return q;}
J evaluate(const Basis&b,const std::vector<int>&a){
 long s=b.s,m=b.m,M=0,N=0;std::string bytes;for(int v:a){M+=v;N+=v*v;bytes+=std::to_string(v)+",";}
 Q F=0,mass=0;J moments=J::array(),energies=J::array();
 for(long k=0;k<=m;++k){Z A=0;for(long i=0;i<s;++i)A+=a[i]*b.p[k][i];Q z=Q(A*A)/b.d[k],e=k?Q(z/(k*(k+1))):z;mass+=z;F+=e;moments.push_back(A.get_str());energies.push_back(str(e));}
 Q q=full(a),tail=q-F,upper=m==s-1?Q(0):Q((Q(N)-mass)/((m+1)*(m+2))),simple=m==s-1?Q(0):rat(N,(m+1)*(m+2));
 need(tail>=0&&tail<=upper&&upper<=simple,"Spectral tail enclosure");
 return {{"s",s},{"m",m},{"M",M},{"N",N},{"source_sha256",digest(bytes)},{"source_encoding","stopped length-s mu vector; signed decimal entries each followed by comma"},{"moments",moments},{"mode_energies",energies},{"full_Q",str(q)},{"low_energy",str(F)},{"mode_mass",str(mass)},{"actual_tail",str(tail)},{"tail_upper",str(upper)},{"simple_tail_upper",str(simple)}};
}
J returns(const std::vector<int>&a){long s=a.size(),M=0,P=0,z=0;for(long i=0;i<s;++i){P+=a[i];if(P==0)z=i+1;}M=P;Q E=0,A=0;P=0;for(long r=1;r<z;++r){P+=a[r-1];E+=rat(P*P,r*(s-r));A+=rat(P,s-r);}auto open=a;for(long i=0;i<z;++i)open[i]=0;Q qo=full(open),coupling=-rat(2*M,s)*A;need(full(a)==qo+E+coupling,"Weighted return identity");return {{"last_zero",z},{"open_Q",str(qo)},{"closed_energy",str(E)},{"signed_area",str(A)},{"open_coupling",str(coupling)}};}
J divisor(const Basis&b,long t,long maxk){long s=b.s,u=root(2*s-1);need(s>u,"Divisor support range");auto mu=mobius(2*s);J out=J::array();for(long k=0;k<=std::min(maxk,b.m);++k){Z direct=0,rebuild=0;for(long i=0;i<t;++i)direct+=mu[s+i]*b.p[k][i];for(long a=1;a<=u;++a)if(mu[a])for(long c=1;c<=u;++c)if(mu[c]){long d=a*c;for(long v=(s+d-1)/d;v<=(s+t-1)/d;++v)rebuild-=mu[a]*mu[c]*b.p[k][d*v-s];}need(rebuild==direct,"Smaller-source signed mode identity");out.push_back({{"k",k},{"direct",direct.get_str()},{"divisor",rebuild.get_str()}});}return {{"s",s},{"t",t},{"u",u},{"modes",out}};}
J qualify(){long eigen=0,norms=0,orth=0,energy=0,ret=0,div=0;for(long s=1;s<=16;++s){auto b=basis(s,s-1);Q trace=1;for(long k=1;k<s;++k)trace+=rat(1,k*(k+1));need(trace==2-rat(1,s),"Trace");for(long k=0;k<s;++k){Z d=0;for(long i=0;i<s;++i){Z lap=0;if(i)lap+=i*(s-i)*(b.p[k][i]-b.p[k][i-1]);if(i<s-1)lap+=(i+1)*(s-i-1)*(b.p[k][i]-b.p[k][i+1]);need(lap==k*(k+1)*b.p[k][i],"Polynomial eigenvector");++eigen;d+=b.p[k][i]*b.p[k][i];}need(d==b.d[k],"Norm");++norms;for(long j=0;j<k;++j){Z dot=0;for(long i=0;i<s;++i)dot+=b.p[k][i]*b.p[j][i];need(dot==0,"Orthogonality");++orth;}}
 std::vector<std::vector<int>> fixtures={std::vector<int>(s),std::vector<int>(s,1),std::vector<int>(s,-1),source(s,s),source(s,s/2)};auto a=std::vector<int>(s);a[0]=1;fixtures.push_back(a);if(s>1){a[s-1]=-1;fixtures.push_back(a);a.assign(s,0);a[s/2]=1;fixtures.push_back(a);}
 for(auto a:fixtures){auto x=evaluate(b,a);need(parse(x["full_Q"])==parse(x["low_energy"]),"Full spectral identity");++energy;returns(a);++ret;}
 }
 auto b=basis(32,5);for(long t=0;t<=32;++t){auto d=divisor(b,t,5);div+=d["modes"].size();}
 return {{"eigen_coordinates",eigen},{"norms",norms},{"orthogonal_pairs",orth},{"full_energy_cases",energy},{"return_cases",ret},{"divisor_moments",div},{"status","PASS"}};
}
J anchor(long s,long t){need(s>=1&&s<=16384&&t>=0&&t<=s,"Bounded readout");long m=std::min(s-1,long(root(s)+(root(s)*root(s)<s)));auto b=basis(s,m);auto a=source(s,t);J x=evaluate(b,a);x["t"]=t;x["projected"]=project(s,t);x["returns"]=returns(a);if(s>1)x["divisor_low_modes"]=divisor(b,t,5);Q q=parse(x["full_Q"]),qh=parse(x["projected"]["Qhat"]);need(q>=qh&&q-qh<=8,"Original projection residual");x["projection_residual"]=str(q-qh);return x;}
J scan(){long s=512,m=23;auto b=basis(s,m);auto mu=mobius(2*s);std::vector<Z>A(m+1);long N=0;Q maxX=-1,maxQ=-1,maxUpper=-1;J tx=J::array(),tq=J::array(),tu=J::array();long half_fail=0;auto update=[](Q v,long t,Q& peak,J& ties){if(v>peak){peak=v;ties=J::array({t});}else if(v==peak)ties.push_back(t);};
 for(long t=0;t<=s;++t){if(t){long v=mu[s+t-1];N+=v*v;for(long k=0;k<=m;++k)A[k]+=v*b.p[k][t-1];}Q F=0,mass=0;for(long k=0;k<=m;++k){Q z=Q(A[k]*A[k])/b.d[k];mass+=z;F+=k?Q(z/(k*(k+1))):z;}Q upper=F+(N-mass)/((m+1)*(m+2));auto a=source(s,t);Q q=full(a);need(F<=q&&q<=upper,"Full-prefix enclosure");auto p=project(s,t);Q x=parse(p["positive_X"]);need(x<=upper,"Original positive cross upper bound");if(x>rat(1,2))++half_fail;update(x,t,maxX,tx);update(q,t,maxQ,tq);update(upper,t,maxUpper,tu);}
 J chosen=J::array();std::set<long> stops;for(auto t:tx)stops.insert(t.get<long>());for(auto t:tq)stops.insert(t.get<long>());for(auto t:tu)stops.insert(t.get<long>());for(long t:stops)chosen.push_back(anchor(s,t));
 return {{"s",s},{"prefixes",s+1},{"max_positive_X",str(maxX)},{"positive_X_ties",tx},{"max_full_Q",str(maxQ)},{"full_Q_ties",tq},{"max_certified_upper",str(maxUpper)},{"certified_upper_ties",tu},{"half_bound_failures",half_fail},{"selected_traces",chosen}};
}
int retained_spectral_main(){try{J input;std::cin>>input;auto req=input.at(0);auto p=req.at("payload");for(auto ref:p.at("sources"))reference(ref);std::string op=req.at("op");J result;if(op=="RH_ORIGINAL_KERNEL_QUALIFY_R1")result=qualify();else if(op=="RH_ORIGINAL_KERNEL_SPECTRAL_R1")result=anchor(p.at("s"),p.at("t"));else if(op=="RH_ORIGINAL_KERNEL_SCAN_R1")result=scan();else throw std::runtime_error("Unknown spectral operation");std::cout<<J({{"ok",true},{"result",result}}).dump()<<std::endl;}catch(const std::exception&e){std::cout<<J({{"ok",false},{"error",e.what()}}).dump()<<std::endl;return 1;}}
