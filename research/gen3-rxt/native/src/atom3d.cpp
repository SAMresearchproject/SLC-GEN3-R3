#include "atom3d.hpp"
#include "atom3d_binding.hpp"
#include <algorithm>
#include <chrono>
#include <cstring>
#include <fstream>
#include <limits>
#include <set>
#include <bit>
#include <fcntl.h>
#include <unistd.h>
#include <omp.h>

namespace rxt {
namespace {
using Clock=std::chrono::steady_clock;
void insist(bool b,const std::string& m){if(!b)throw std::invalid_argument("ATOM3D: "+m);}
std::string bytes(const std::filesystem::path& p){std::ifstream f(p,std::ios::binary);insist(bool(f),"Cannot read "+p.string());return {std::istreambuf_iterator<char>(f),{}};}
template<class T>std::vector<T> binary(const std::filesystem::path& p,size_t n){auto s=bytes(p);insist(s.size()==n*sizeof(T),"Asset shape differs: "+p.string());std::vector<T> out(n);std::memcpy(out.data(),s.data(),s.size());return out;}
template<class T>std::string packed(const std::vector<T>& v){return {reinterpret_cast<const char*>(v.data()),v.size()*sizeof(T)};}
int integer(const json& p,const char* key,int fallback,int lo,int hi){auto v=p.value(key,json(fallback));insist(v.is_number_integer()&&!v.is_boolean(),std::string(key)+" must be an integer");auto n=v.get<int64_t>();insist(n>=lo&&n<=hi,std::string(key)+" outside source domain");return int(n);}
bool boolean(const json& p,const char* key,bool fallback){auto v=p.value(key,json(fallback));insist(v.is_boolean(),std::string(key)+" must be Boolean");return v.get<bool>();}
std::string backend(const json& p){auto b=p.value("backend",std::string("cuda"));insist(b=="cuda"||b=="cpu","backend must be cpu or cuda");return b;}
mpz_class z64(int64_t n){return mpz_class(std::to_string(n));}
mpq_class q64(int64_t n,int64_t d=1){mpq_class q(z64(n),z64(d));q.canonicalize();return q;}
std::string frac(const mpq_class& q){return q.get_str();}
mpz_class wide_z(A3DWide x){mpz_class z(std::to_string(x.hi));z<<=64;z+=mpz_class(std::to_string(x.lo));return z;}
A3DWide wide(__int128 x){return {uint64_t(x),int64_t(x>>64)};}
void bound(const std::vector<int64_t>& coefficients,int width,int feature_bound){
    for(size_t i=0;i<coefficients.size();i+=width){mpz_class value=0;for(int f=0;f<width;++f)value+=abs(z64(coefficients[i+f]))*feature_bound;
        insist(value<=z64(INT64_MAX),"Exact source contraction exceeds int64; requires a wider kernel");}
}
// Independent CPU construction: gather incoming/outgoing terms at each site.
// CUDA scatters each phase into its two endpoints and stores features as SoA.
void cpu_row(const A3DGeometry& g,uint32_t address,int kind,int mask,int8_t* j,int16_t* f){
    int phase[18];
    for(int e=0;e<9;++e){int q=int((address>>e)&1)+2*int((address>>(e+9))&1);int re[4]={1,0,-1,0},im[4]={0,1,0,-1};phase[e]=kind?std::abs(re[q]):re[q];phase[9+e]=kind?std::abs(im[q]):im[q];}
    for(int s=0;s<2;++s)for(int v=0;v<6;++v){int x=0;for(int e=0;e<9;++e)x+=((g.endpoints[e*2+1]==v)-(g.endpoints[e*2]==v))*g.masks[mask*9+e]*phase[s*9+e];j[s*6+v]=int8_t(x);}
    for(int e=0;e<3;++e){int k=g.centers[e],u=g.endpoints[2*k],v=g.endpoints[2*k+1],x=int(j[u])-j[v],y=int(j[u+6])-j[v+6];f[e*3]=x*x;f[e*3+1]=2*x*y;f[e*3+2]=y*y;}
    for(int e=0;e<9;++e){int u=g.endpoints[e*2],v=g.endpoints[e*2+1],x=int(j[u])-j[v],y=int(j[u+6])-j[v+6];f[9+e]=x*x+y*y;}
    for(int c=0;c<5;++c){int x=0,y=0;for(int e=0;e<9;++e){int sign=g.cycles[c*9+e]*g.masks[mask*9+e];x+=sign*phase[e];y+=sign*phase[9+e];}f[18+c]=x*x+y*y;}
}
uint32_t cpu_write(uint32_t a,int c,int direction){int q=((a>>c)&1)+2*((a>>(c+9))&1);q=(q+direction+4)%4;a&=~((1u<<c)|(1u<<(c+9)));return a|((q&1u)<<c)|((unsigned(q)>>1)<<(c+9));}
std::array<int,6> lift(uint32_t a,int kind){std::array<int,6> v{};int re[4]={1,0,-1,0},im[4]={0,1,0,-1};for(int k=0;k<3;++k){int c=1+k*3,q=((a>>c)&1)+2*((a>>(c+9))&1);v[k]=kind?std::abs(re[q]):re[q];v[k+3]=kind?std::abs(im[q]):im[q];}return v;}
void write_new(const std::filesystem::path& p,const std::string& data){
    int fd=::open(p.c_str(),O_WRONLY|O_CREAT|O_EXCL|O_CLOEXEC,0600);insist(fd>=0,"Export destination already exists or cannot be created: "+p.string());
    try{size_t at=0;while(at<data.size()){auto n=::write(fd,data.data()+at,data.size()-at);if(n<=0)throw std::runtime_error("Native artifact write failed");at+=size_t(n);}if(fsync(fd)!=0)throw std::runtime_error("Native artifact fsync failed");::close(fd);}catch(...){::close(fd);throw;}
}
json table_record(const A3DTable& t){size_t count=1;for(auto n:t.shape)count*=n;json row={{"shape",t.shape},{"element_bytes",t.element_size},{"values",count},{"bytes",count*t.element_size},{"kernel_seconds",t.kernel_seconds},{"wall_seconds",t.wall_seconds},{"resident_reused",t.reused}};if(!t.bytes.empty())row["sha256"]=hash(t.bytes);return row;}
}

Atom3d::Atom3d(const std::filesystem::path& directory,const Resources& resources):resources_(resources),directory_(std::filesystem::canonical(directory)){
    insist(std::endian::native==std::endian::little,"This source binary layout requires little-endian host");
    auto body=bytes(directory_/"BUNDLE.json");source_id_=hash(body);insist(source_id_==A3D_SOURCE_SHA256,"Source generation differs from this native release");bundle_=json::parse(body);
    insist(bundle_.at("schema")=="GEN_RXT_ATOM3D_SOURCE_V1"&&bundle_.at("domain_revision")=="A3D41-T18-CONTACT-R2","Source binding differs");
    for(auto it=bundle_.at("files").begin();it!=bundle_.at("files").end();++it){auto path=std::filesystem::path(it.key());insist(!path.is_absolute(),"Absolute source member");for(const auto& part:path)insist(part!="..","Source member escapes bundle");auto data=bytes(directory_/path);insist(data.size()==it.value().at("bytes").get<size_t>()&&hash(data)==it.value().at("sha256").get<std::string>(),"Source asset differs: "+it.key());}
    // Source admission is CPU-only; ensure_gpu admits the device allocation on demand.
    resources_.admit(768ull<<20);
    grammar_=read_json(directory_/"li6_grammar_source/CONTRACT.json");assembly_=read_json(directory_/"li6_assembly_source/CONTRACT.json");contact_=read_json(directory_/"CONTACT_TASKS.json");build_=read_json(directory_/"li6_construction/BUILD_SHEET.json");
    auto& g=grammar_.at("geometry");auto& in=inputs_;
    insist(g.at("endpoints").size()==9&&g.at("masks").size()==4&&g.at("cycle_incidence").size()==5,"Li-6 source topology shape differs");
    for(int e=0;e<9;++e)for(int side=0;side<2;++side){int v=g["endpoints"][e][side];insist(v>=0&&v<6,"Source endpoint outside six objects");in.geometry.endpoints[e*2+side]=v;}
    for(int m=0;m<4;++m)for(int e=0;e<9;++e){int x=g["masks"][m][e];insist(x==0||x==1,"Non-binary source mask");in.geometry.masks[m*9+e]=x;}
    for(int c=0;c<5;++c)for(int e=0;e<9;++e){int x=g["cycle_incidence"][c][e];insist(std::abs(x)<=1,"Cycle coefficient outside signed incidence");in.geometry.cycles[c*9+e]=x;}
    for(int e=0;e<3;++e){int k=g["center_relation_indices"][e];insist(k>=0&&k<9,"Center relation outside source");in.geometry.centers[e]=k;}
    in.center_rep=binary<uint32_t>(directory_/"li6_grammar_source/CENTER_REPRESENTATIVE.u32le",5143);in.grammar_rep=binary<uint32_t>(directory_/"li6_grammar_source/GRAMMAR_REPRESENTATIVE.u32le",41245);in.assembly_rep=binary<uint32_t>(directory_/"li6_assembly_source/FEATURE_REPRESENTATIVE.u32le",5143);
    for(auto* reps:{&in.center_rep,&in.grammar_rep,&in.assembly_rep})for(auto r:*reps)insist(r<A3D_ROWS,"Feature representative outside source fiber");
    in.center_coeff=binary<int64_t>(directory_/"li6_grammar_source/CENTER_COEFFICIENTS.i64le",384*9);in.grammar_coeff=binary<int64_t>(directory_/"li6_grammar_source/GRAMMAR_COEFFICIENTS.i64le",87*14);in.assembly_coeff=binary<int64_t>(directory_/"li6_assembly_source/COEFFICIENTS.i64le",768*9);in.tensors=binary<int64_t>(directory_/"li6_grammar_source/TMR1.i64le",3*128*3);in.eta_bound=binary<int64_t>(directory_/"li6_assembly_source/FOUR_ETA_MAX.i64le",6*128);
    bound(in.center_coeff,9,128);bound(in.grammar_coeff,14,162);bound(in.assembly_coeff,9,128);
    auto energy=read_json(directory_/"LI6_ENERGY_CONTRACT.json");for(const auto& mask:energy.at("matrices_integer"))for(const auto& form:mask)for(const auto& row:form)for(const auto& x:row)in.energy.push_back(x.get<int32_t>());insist(in.energy.size()==576,"Source energy matrix shape differs");
    for(size_t i=0;i<in.energy.size();i+=36){mpz_class limit=0;for(int k=0;k<36;++k)limit+=abs(z64(in.energy[i+k]))*32;insist(limit<=INT32_MAX,"Energy accumulation bound exceeds int32");}
    insist(contact_.at("forms").size()==24&&contact_.at("tasks").size()==4736,"Current contact packet shape differs");
    for(const auto& form:contact_["forms"]){insist(form.at("denominator")==1&&form.at("numerators").size()==21,"Contact form storage differs");for(auto x:form["numerators"])in.forms.push_back(x.get<int64_t>());}bound(in.forms,21,4);
    for(const auto& t:contact_["tasks"]){A3DContactTask task;task.address=t.at("fiber").at("address");insist(task.address<ADDRESS_COUNT,"Contact address outside T18");task.prefix=integer(t,"readout_prefix",0,0,3);task.kind=t["readout_kind"]=="UNSIGNED_OCCUPANCY";task.absolute=t["stage"]=="ABSOLUTE_CONTACT";
        insist(t["readout_kind"]=="UNSIGNED_OCCUPANCY"||t["readout_kind"]=="NATIVE_SIGNED_PHASE","Unknown contact lift");insist(task.absolute||t["stage"]=="HISTORY","Unknown contact stage");insist(t["fiber"]["writes"].size()==3,"Contact requires three declared writes");
        uint32_t a=task.address;for(int k=0;k<3;++k){int c=t["fiber"]["writes"][k][0],direction=t["fiber"]["writes"][k][1];insist((c==1||c==4||c==7)&&std::abs(direction)==1,"Write outside contact source");task.writes[k*2]=c;task.writes[k*2+1]=direction;if(k<task.prefix)a=cpu_write(a,c,direction);}
        auto before=task.absolute?std::array<int,6>{}:lift(task.address,task.kind);insist(json(before)==t["before"]&&json(lift(a,task.kind))==t["after"],"Contact task phase lift differs from declared write history");in.contact.push_back(task);
    }
    insist(build_.at("objects").size()==6&&build_.at("relations").size()==9&&build_.at("typed_center_placements").size()==6,"Typed Li-6 context shape differs");
    for(int e=0;e<9;++e){auto& row=build_["relations"][e];insist(row["source_object"]==g["object_order"][in.geometry.endpoints[e*2]]&&row["target_object"]==g["object_order"][in.geometry.endpoints[e*2+1]],"Build-sheet incidence differs from the native source");insist(row["ordered_endpoint_receipts"].size()==2&&row["physical_tensor_quantity"].is_null()&&row["physical_tensor_type"].is_null(),"Typed source inventory differs");}
}
json Atom3d::binding()const{return {{"directory",directory_.string()},{"source_sha256",source_id_},{"domain_revision","A3D41-T18-CONTACT-R2"},{"native_revision","A3D41-RXT-R2"}};}
json Atom3d::status()const{return {{"domain_update","A3D41-RXT-R3-COMMON-MINIMA"},{"domain","ATOM3D"},{"domain_revision","A3D41-T18-CONTACT-R2"},{"native_revision","A3D41-RXT-R2"},{"source_sha256",source_id_},{"implementation","NATIVE_CPP_CUDA"},{"cpu_workers",resources_.cpu_threads},{"gpu_resident_bytes",gpu_?gpu_->resident_bytes():0},{"cpu_resident_bytes",cpu_currents_.size()+cpu_features_.size()*2},{"minimum_cache_entries",minima_.size()},{"source_rows",A3D_ROWS},{"phase_states",ADDRESS_COUNT},{"operations",{"A3D41_CONTACT","LI6_PHASE_CENSUS","LI6_GRAMMAR","LI6_GRAMMAR_READOUT","LI6_MINIMUM_SET","LI6_HISTORY","LI6_ASSEMBLY","LI6_ASSEMBLY_RECEIVER","LI6_SOURCE_ENERGY","LI6_BUILD","ATOM3D_EXPORT","ATOM3D_VALIDATE","ATOM3D_BENCH","ATOM3D_CONSTRUCTION","ATOM3D_CONSTRUCTION_IDS"}}};}
void Atom3d::ensure_gpu(){if(!gpu_){resources_.admit(256ull<<20,512ull<<20);gpu_=std::make_unique<A3DCuda>(inputs_);}}
void Atom3d::phase_cpu(bool refresh){
    if(!cpu_features_.empty()&&!refresh)return;cpu_currents_.resize(A3D_ROWS*12);cpu_features_.resize(A3D_ROWS*A3D_FEATURES);auto& g=inputs_.geometry;
    #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static)
    for(size_t row=0;row<A3D_ROWS;++row)cpu_row(g,row/8,(row/4)%2,row%4,cpu_currents_.data()+row*12,cpu_features_.data()+row*A3D_FEATURES);
}
A3DTable Atom3d::table(const std::string& name,const std::string& device,bool download,bool refresh){
    if(device=="cuda"){ensure_gpu();return gpu_->table(name,download,refresh);}insist(device=="cpu","Unknown backend");
    auto start=Clock::now();A3DTable out;
    if(name=="CURRENTS"){out.reused=!cpu_features_.empty()&&!refresh;phase_cpu(refresh);out.shape={ADDRESS_COUNT,2,4,2,6};out.element_size=1;if(download)out.bytes=packed(cpu_currents_);}
    else if(name=="CONTACT"){
        std::vector<int64_t> values(inputs_.contact.size()*24);
        #pragma omp parallel for num_threads(2) schedule(static)
        for(size_t row=0;row<inputs_.contact.size();++row){auto t=inputs_.contact[row];uint32_t a=t.address;for(int k=0;k<t.prefix;++k)a=cpu_write(a,t.writes[k*2],t.writes[k*2+1]);auto before=t.absolute?std::array<int,6>{}:lift(t.address,t.kind),after=lift(a,t.kind);int coeff[21];int k=0;for(int u=0;u<6;++u)for(int v=u;v<6;++v)coeff[k++]=(u==v?1:2)*(after[u]*after[v]-before[u]*before[v]);for(int c=0;c<24;++c){int64_t val=0;for(int f=0;f<21;++f)val+=coeff[f]*inputs_.forms[c*21+f];values[row*24+c]=val;}}
        out.shape={inputs_.contact.size(),24};out.element_size=8;if(download)out.bytes=packed(values);
    }else if(name=="ENERGY"){
        phase_cpu();std::vector<int16_t> values(A3D_ROWS*4);int error=0;
        #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static) reduction(|:error)
        for(size_t row=0;row<A3D_ROWS;++row)for(int f=0;f<4;++f){int64_t val=0;auto* j=cpu_currents_.data()+row*12;for(int s=0;s<2;++s)for(int u=0;u<6;++u)for(int v=0;v<6;++v)val+=int64_t(j[s*6+u])*inputs_.energy[((row%4)*4+f)*36+u*6+v]*j[s*6+v];if(val<0||val>32767)error=1;values[row*4+f]=int16_t(val);}
        insist(!error,"Energy storage bound exceeded");out.shape={ADDRESS_COUNT,2,4,4};out.element_size=2;if(download)out.bytes=packed(values);
    }else{
        insist(name=="CENTER"||name=="GRAMMAR"||name=="ASSEMBLY"||name=="CENTER_FEATURES"||name=="GRAMMAR_FEATURES","Unknown table");phase_cpu();bool grammar=name=="GRAMMAR"||name=="GRAMMAR_FEATURES",feature=name=="CENTER_FEATURES"||name=="GRAMMAR_FEATURES";
        auto& reps=name=="ASSEMBLY"?inputs_.assembly_rep:grammar?inputs_.grammar_rep:inputs_.center_rep;int width=grammar?14:9,offset=grammar?9:0,columns=feature?width:name=="ASSEMBLY"?768:grammar?87:384;
        out.shape=name=="ASSEMBLY"?std::vector<size_t>{reps.size(),6,128}:std::vector<size_t>{reps.size(),size_t(columns)};out.element_size=feature?2:8;
        if(feature){std::vector<int16_t> values(reps.size()*width);for(size_t row=0;row<reps.size();++row)for(int f=0;f<width;++f)values[row*width+f]=cpu_features_[size_t(reps[row])*A3D_FEATURES+offset+f];if(download)out.bytes=packed(values);}
        else{auto& coeff=name=="ASSEMBLY"?inputs_.assembly_coeff:grammar?inputs_.grammar_coeff:inputs_.center_coeff;std::vector<int64_t> values(reps.size()*columns);
            #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static)
            for(size_t row=0;row<reps.size();++row){const auto* features=cpu_features_.data()+size_t(reps[row])*A3D_FEATURES+offset;for(int c=0;c<columns;++c){int64_t value=0;for(int f=0;f<width;++f)value+=int64_t(features[f])*coeff[c*width+f];values[row*columns+c]=value;}}if(download)out.bytes=packed(values);}
    }
    out.wall_seconds=std::chrono::duration<double>(Clock::now()-start).count();return out;
}
A3DMinimum Atom3d::minimum_cpu(const A3DQuery& q){
    auto start=Clock::now();phase_cpu();std::vector<__int128> values(ADDRESS_COUNT);__int128 best=__int128(1)<<126;
    #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static) reduction(min:best)
    for(size_t state=0;state<ADDRESS_COUNT;++state){size_t row=state*8+q.kind*4+q.mask;auto* f=cpu_features_.data()+row*A3D_FEATURES;__int128 c=0,m=0;for(int k=0;k<9;++k)c+=__int128(f[k])*q.center[k];for(int k=0;k<14;++k)m+=__int128(f[9+k])*q.motif[k];values[state]=c*576+m;best=std::min(best,values[state]);}
    A3DMinimum out;out.value=wide(best);out.bits.resize(ADDRESS_COUNT/8);for(size_t state=0;state<ADDRESS_COUNT;++state)if(values[state]==best){out.bits[state/8]|=1u<<(state%8);++out.count;}out.wall_seconds=std::chrono::duration<double>(Clock::now()-start).count();return out;
}

json Atom3d::readout(const json& p){
    int state=integer(p,"state",0,0,ADDRESS_COUNT-1),kind=integer(p,"kind",0,0,1),mask=integer(p,"mask",3,0,3),cover=integer(p,"cover",3,0,4),assignment=integer(p,"assignment",0,0,5),rho=integer(p,"rho",1,1,128);
    bool hidden=boolean(p,"hidden_loop",true);auto channel=p.value("channel",std::string("observed")),receiver=p.value("receiver",std::string("CIRCULATION")),device=backend(p);insist(channel=="native"||channel=="observed","Unknown grammar channel");insist(receiver=="CIRCULATION"||receiver=="ENDPOINT","Unknown grammar receiver");
    auto& g=grammar_["geometry"];int motif=-1,lift_index=-1;json probes=json::object();
    for(auto& row:grammar_["output_metadata"]){if(row["type"]=="MOTIF_ACTION"&&row["mask"]==mask&&row["cover"]==g["covers"][cover]["id"]&&row["channel"]==channel&&row["receiver"]==receiver)motif=row["index"];if(row["type"]=="HIDDEN_LIFT_LOOP"&&row["mask"]==mask)lift_index=row["index"];}
    insist(motif>=0&&lift_index>=0,"Missing source operator");A3DQuery q;q.kind=kind;q.mask=mask;
    for(int e=0;e<3;++e){int64_t weight=g["source_assignments"][assignment]["native_account_numerators"][e];for(int k=0;k<3;++k)q.center[e*3+k]=8*weight*inputs_.tensors[(e*128+rho-1)*3+k]*inputs_.geometry.masks[mask*9+inputs_.geometry.centers[e]];}
    for(int f=0;f<14;++f)q.motif[f]=inputs_.grammar_coeff[motif*14+f]+(hidden?inputs_.grammar_coeff[lift_index*14+f]:0);
    bound(std::vector<int64_t>(q.center,q.center+9),9,128);bound(std::vector<int64_t>(q.motif,q.motif+14),14,162);
    int8_t currents[12];int16_t features[23];cpu_row(inputs_.geometry,state,kind,mask,currents,features);
    int64_t center=0;for(int k=0;k<9;++k)center+=int64_t(features[k])*q.center[k];
    auto value=[&](int col){int64_t n=0;for(int f=0;f<14;++f)n+=int64_t(features[9+f])*inputs_.grammar_coeff[col*14+f];return q64(n,576);};
    mpq_class m=value(motif),l=hidden?value(lift_index):mpq_class(0),action=q64(center)+m+l;
    for(auto& row:grammar_["output_metadata"]){std::string type=row["type"];if(type=="PHI_MINUS"||type=="PHI_PLUS"||type=="SIGNED_PAIR_SURFACE")probes[type]=frac(value(row["index"]));}
    std::string key=json({kind,mask,cover,assignment,rho,hidden,channel,receiver,device}).dump();bool cached=boolean(p,"cache",true)&&minima_.contains(key);A3DMinimum minimum;
    if(cached)minimum=minima_.at(key);else{if(device=="cuda"){ensure_gpu();minimum=gpu_->minimum(q);}else minimum=minimum_cpu(q);if(minima_.size()>=64)minima_.erase(minima_.begin());minima_[key]=minimum;}
    mpq_class min_value(wide_z(minimum.value),mpz_class(576));min_value.canonicalize();
    json out={{"status","PASS"},{"operation","LI6_GRAMMAR_READOUT"},{"state",state},{"kind",kind},{"mask",g["mask_names"][mask]},{"cover",g["covers"][cover]["id"]},{"channel",channel},{"triad_receiver",receiver},{"hidden_loop",hidden},{"assignment",assignment},{"rho",rho},{"source_action",frac(action)},{"center_action",std::to_string(center)},{"motif_action",frac(m)},{"hidden_lift_action",frac(l)},{"minimum_source_action",frac(min_value)},{"state_is_minimum",action==min_value},{"minimum_state_count",minimum.count},{"minimum_state_set_sha256",hash(packed(minimum.bits))},{"signed_column_probes",probes},{"output_unit","CANDIDATE_SOURCE_ACTION"},{"physical_prediction_computed",false},{"native_execution",{{"backend",device},{"cache_hit",cached},{"kernel_seconds",cached?0:minimum.kernel_seconds},{"wall_seconds",cached?0:minimum.wall_seconds},{"accumulator_bits",128},{"all_minimum_states_retained",true}}}};
    insist(bool(minimum.bits[state/8]&(1u<<(state%8)))==(action==min_value),"Exact minimum membership differs from direct source readout");
    if(boolean(p,"include_minimum_states",false)){out["minimum_states"]=json::array();for(uint32_t a=0;a<ADDRESS_COUNT;++a)if(minimum.bits[a/8]&(1u<<(a%8)))out["minimum_states"].push_back(a);}
    return out;
}
json Atom3d::receiver(const json& p){
    int a=integer(p,"assignment",0,0,5),r=integer(p,"rho",1,1,128)-1,state=integer(p,"state",0,0,ADDRESS_COUNT-1);auto fraction=rational(p.value("eta_fraction",json("1/2")));insist(fraction>=0,"eta_fraction must be nonnegative");mpq_class maximum=q64(inputs_.eta_bound[a*128+r],4),eta=fraction*maximum;
    int8_t currents[12];int16_t features[23];cpu_row(inputs_.geometry,state,0,3,currents,features);mpq_class matrix[12][12];
    for(int e=0;e<3;++e){int edge=inputs_.geometry.centers[e],u=inputs_.geometry.endpoints[edge*2],v=inputs_.geometry.endpoints[edge*2+1];int64_t weight=assembly_["assignments"][a]["native_account_numerators"][e];auto* t=inputs_.tensors.data()+(e*128+r)*3;for(int s=0;s<2;++s)for(int k=0;k<2;++k){mpq_class z=q64(t[s+k]*weight);matrix[u+6*s][u+6*k]+=z;matrix[v+6*s][v+6*k]+=z;matrix[u+6*s][v+6*k]-=z;matrix[v+6*s][u+6*k]-=z;}}
    for(int s=0;s<2;++s){matrix[4+6*s][4+6*s]+=eta;matrix[5+6*s][5+6*s]+=eta;matrix[4+6*s][5+6*s]-=eta;matrix[5+6*s][4+6*s]-=eta;}
    mpq_class value=0;json terms=json::array();for(int u=0;u<12;++u)for(int v=u;v<12;++v){mpq_class coefficient=q64((u==v?1:2)*int(currents[u])*int(currents[v])),term=coefficient*matrix[u][v];value+=term;terms.push_back({{"coordinates",{u,v}},{"coefficient",frac(coefficient)},{"matrix_entry",frac(matrix[u][v])},{"contribution",frac(term)}});}
    return {{"status","PASS"},{"operation","LI6_ASSEMBLY_RECEIVER"},{"assignment",a},{"rho",r+1},{"state",state},{"eta",frac(eta)},{"eta_upper_bound",frac(maximum)},{"in_exact_ground_selection_interval",fraction>0&&fraction<1},{"center_response_blocks",3},{"center_source_leaf_instances",4},{"exterior_response_blocks",1},{"physical_prediction_computed",false},{"exact_value",frac(value)},{"currents",std::vector<int>(currents,currents+12)},{"coordinate_terms",terms},{"coefficient_unit","ASSEMBLY_SOURCE_COORDINATE"},{"source_unit","NATIVE_CURRENT"}};
}
json Atom3d::history(const json& p){
    insist(p.contains("writes")&&p["writes"].is_array()&&p["writes"].size()<=4096,"History requires at most 4096 ordered writes");
    std::vector<Event> program;
    for(const auto& pair:p["writes"]){
        insist(pair.is_array()&&pair.size()==2,"Write requires [coordinate, direction]");
        json event={{"coordinate",pair[0]},{"direction",pair[1]}};
        int c=integer(event,"coordinate",0,0,8),d=integer(event,"direction",0,-1,1);
        insist(d!=0,"Write direction must be +1 or -1");program.push_back({c,d});
    }
    json query=p;query.erase("writes");query.erase("include_histories");
    uint32_t state=integer(p,"state",0,0,ADDRESS_COUNT-1);json points=json::array(),edges=json::array(),readouts=json::array();
    mpq_class initial,maximum;json ties=json::array();
    for(size_t k=0;k<=program.size();++k){
        if(k){auto event=program[k-1];state=cpu_write(state,event.coordinate,event.direction);edges.push_back({{"id","e"+std::to_string(k-1)},{"before","p"+std::to_string(k-1)},{"after","p"+std::to_string(k)},{"event",{{"coordinate",event.coordinate},{"direction",event.direction}}}});}
        query["state"]=state;query["cache"]=true;auto row=readout(query);auto action=rational(row["source_action"]);
        if(k==0){initial=action;maximum=action;}if(action>maximum){maximum=action;ties=json::array();}if(action==maximum)ties.push_back(k);
        points.push_back({{"id","p"+std::to_string(k)},{"state",state},{"action",row["source_action"]}});readouts.push_back(row);
    }
    json account={{"quantity",{{"kind","SOURCE_ACTION"},{"units",{{"candidate_source_action",1}}},{"scope","HISTORY"}}},{"source_binding",source_id_},{"points",points},{"edges",edges}};
    return {{"status","PASS"},{"operation","LI6_HISTORY"},{"source_sha256",source_id_},{"history",account},{"readouts",readouts},{"barrier",frac(maximum-initial)},{"maximum_action",frac(maximum)},{"all_maximum_prefixes",ties},{"log",log_account(account)},{"full_ordered_history_retained",true}};
}
json Atom3d::contact(const json& p){
    auto t=table("CONTACT",backend(p));const auto* values=reinterpret_cast<const int64_t*>(t.bytes.data());
    json histories=json::object(),absolute=json::object();std::vector<std::string> history_order;int column=-1;for(size_t i=0;i<contact_["forms"].size();++i)if(contact_["forms"][i]["id"]=="N100_CONTACT")column=i;insist(column>=0,"Contact operator missing");
    for(size_t i=0;i<inputs_.contact.size();++i){auto& task=contact_["tasks"][i];std::string kind=task["readout_kind"];auto val=values[i*24+column];if(task["stage"]=="ABSOLUTE_CONTACT"){absolute[kind].push_back({{"phases",task["initial_phases"]},{"value",val}});continue;}
        std::string id=task["history_id"];if(!histories.contains(id)){history_order.push_back(id);json path=json::array();auto& ct=inputs_.contact[i];uint32_t a=ct.address;path.push_back(a);for(int k=0;k<3;++k){a=cpu_write(a,ct.writes[k*2],ct.writes[k*2+1]);path.push_back(a);}histories[id]={{"id",id},{"initial_phases",task["initial_phases"]},{"orientation",task["native_orientation"]},{"order",task["order"]},{"trajectory",path},{"readouts",json::object()}};}
        auto& h=histories[id]["readouts"];if(!h.contains(kind))h[kind]={{"prefix_deltas",{0,0,0,0}},{"barrier",0}};h[kind]["prefix_deltas"][task["readout_prefix"].get<size_t>()]=val;
    }
    json groups=json::object();for(auto& h:histories){for(auto& v:h["readouts"])v["barrier"]=*std::max_element(v["prefix_deltas"].begin(),v["prefix_deltas"].end());std::string key=json({h["initial_phases"],h["orientation"]}).dump();groups[key].push_back(h);}
    json orders=json::array();int changed=0;for(auto& group:groups){json views=json::object();for(const auto& kind:{"NATIVE_SIGNED_PHASE","UNSIGNED_OCCUPANCY"}){int64_t best=INT64_MAX;for(auto& h:group)best=std::min(best,h["readouts"][kind]["barrier"].get<int64_t>());json choices=json::array();for(auto& h:group)if(h["readouts"][kind]["barrier"]==best)choices.push_back(h["order"]);std::sort(choices.begin(),choices.end());views[kind]={{"minimum_barrier",best},{"minimizing_orders",choices}};}if(views["NATIVE_SIGNED_PHASE"]["minimizing_orders"]!=views["UNSIGNED_OCCUPANCY"]["minimizing_orders"])++changed;orders.push_back({{"initial_phases",group[0]["initial_phases"]},{"orientation",group[0]["orientation"]},{"readouts",views}});}
    json minima=json::object();for(auto it=absolute.begin();it!=absolute.end();++it){int64_t best=INT64_MAX;for(auto& r:it.value())best=std::min(best,r["value"].get<int64_t>());json phases=json::array();for(auto& r:it.value())if(r["value"]==best)phases.push_back(r["phases"]);minima[it.key()]={{"minimum_contact",best},{"minimizing_phases",phases}};}
    json overlap=json::array();for(auto& a:minima["NATIVE_SIGNED_PHASE"]["minimizing_phases"])for(auto& b:minima["UNSIGNED_OCCUPANCY"]["minimizing_phases"])if(a==b)overlap.push_back(a);
    json summary={{"domain_revision","A3D41-T18-CONTACT-R2"},{"native_histories",histories.size()},{"state_direction_families",groups.size()},{"changed_minimizing_order_families",changed},{"minima",minima},{"minimizing_state_overlap",overlap},{"physical_energy_scale","OPEN"},{"physical_isotope_incidence","OPEN"}};
    json out={{"status","PASS"},{"operation","A3D41_CONTACT"},{"table",table_record(t)},{"summary",summary}};if(boolean(p,"include_histories",true)){out["history_results"]=json::array();for(auto& id:history_order)out["history_results"].push_back(histories[id]);out["order_choices"]=orders;}return out;
}

json Atom3d::validate(const std::filesystem::path& reference){
    json rows=json::array();uint64_t count=0;auto expected=read_json(reference/"HASHES.json");
    for(auto it=expected.begin();it!=expected.end();++it){auto cpu=table(it.key(),"cpu",true,true),gpu=table(it.key(),"cuda",true,true);insist(cpu.shape==gpu.shape&&cpu.bytes==gpu.bytes,"CPU/CUDA exact values differ: "+it.key());auto digest=hash(gpu.bytes);insist(digest==it.value()["sha256"].get<std::string>()&&gpu.bytes.size()==it.value()["bytes"].get<size_t>(),"Installed A3D41 exact values differ: "+it.key());count+=gpu.bytes.size()/gpu.element_size;auto row=table_record(gpu);row["table"]=it.key();row["status"]="PASS";row["cpu_wall_seconds"]=cpu.wall_seconds;rows.push_back(row);}
    auto c=contact({{"backend","cuda"}});insist(c["summary"]==read_json(reference/"CONTACT_SUMMARY.json"),"Contact summary differs");auto h=read_json(reference/"CONTACT_HISTORY.json");insist(c["history_results"]==h["history_results"],"Ordered contact histories or barriers differ");insist(c["order_choices"]==h["order_choices"],"Complete minimizing order choices differ");
    size_t queries=0,cpu_queries=0;for(auto& row:read_json(reference/"READOUTS.json")){json p=row["params"];p["backend"]="cuda";p["cache"]=false;auto result=readout(p);result.erase("native_execution");insist(result==row["result"],"Installed grammar readout or complete minimum set differs at case "+std::to_string(queries));if(queries<8){p["backend"]="cpu";auto cpu=readout(p);cpu.erase("native_execution");insist(cpu==result,"CPU/CUDA complete minimum differs");++cpu_queries;}++queries;}
    size_t receivers=0;for(auto& row:read_json(reference/"RECEIVERS.json")){auto result=receiver(row["params"]);auto expected=row["result"];for(auto key:{"eta","eta_upper_bound","in_exact_ground_selection_interval"})insist(result[key]==expected[key],"Assembly receiver parameter differs");const auto& v=expected["exact_receiver"].at("signed_change").at("rational");mpq_class value(mpz_class(v[0].get<std::string>()),mpz_class(v[1].get<std::string>()));insist(value==rational(result["exact_value"]),"Exact assembled receiver differs");++receivers;}
    return {{"status","PASS"},{"source",binding()},{"exact_bulk_values",count},{"tables",rows},{"ordered_contact_histories",768},{"all_contact_forms",113664},{"installed_readout_and_minimum_comparisons",queries},{"independent_cpu_complete_minima",cpu_queries},{"exact_assembly_receivers",receivers},{"source_runtime_loaded",false},{"status_after",status()}};
}
json Atom3d::benchmark(const json& p){
    int repeats=integer(p,"repeats",3,1,10);json rows=json::array();
    for(auto name:{"CURRENTS","CENTER","GRAMMAR","ASSEMBLY","ENERGY","CONTACT"}){
        table(name,"cuda",false);table(name,"cpu",false);json samples=json::array();for(int i=0;i<repeats;++i){auto cpu=table(name,"cpu",false,true),gpu=table(name,"cuda",false,true);auto downloaded=table(name,"cuda",true,false);samples.push_back({{"cpu_compute_wall_seconds",cpu.wall_seconds},{"cuda_resident_wall_seconds",gpu.wall_seconds},{"cuda_kernel_seconds",gpu.kernel_seconds},{"cuda_complete_download_seconds",downloaded.wall_seconds},{"cpu_over_cuda_resident",cpu.wall_seconds/gpu.wall_seconds}});}rows.push_back({{"table",name},{"samples",samples}});
    }
    json q={{"state",14336},{"kind",0},{"mask",3},{"cover",3},{"assignment",0},{"rho",1},{"cache",false}};auto first=readout(q);q["cache"]=true;auto start=Clock::now();for(int i=0;i<1000;++i)readout(q);double cached=std::chrono::duration<double>(Clock::now()-start).count()/1000;
    return {{"status","PASS"},{"scope","Same native source; warmed resident inputs; bulk compute and complete download timed separately; JSON and durable commits excluded"},{"tables",rows},{"minimum_scan",first["native_execution"]},{"cached_exact_readout_mean_seconds",cached},{"resources",resources_.describe()},{"resident",status()}};
}
json Atom3d::execute(const std::string& op,const json& p){
    std::set<std::string> allowed={"source_sha256","domain_revision","backend"};
    auto permit=[&](std::initializer_list<const char*> fields){for(auto f:fields)allowed.insert(f);};
    if(op=="A3D41_CONTACT")permit({"include_histories"});
    else if(op=="LI6_GRAMMAR_READOUT"||op=="LI6_MINIMUM_SET"||op=="LI6_HISTORY") {permit({"state","kind","mask","cover","assignment","rho","hidden_loop","channel","receiver","cache","include_minimum_states"});if(op=="LI6_HISTORY")permit({"writes"});}
    else if(op=="LI6_ASSEMBLY_RECEIVER")permit({"assignment","rho","state","eta_fraction"});
    else if(op=="LI6_BUILD")permit({"include_ledger"});
    else if(op=="ATOM3D_VALIDATE")permit({"reference_directory"});
    else if(op=="ATOM3D_BENCH")permit({"repeats"});
    else if(op=="ATOM3D_CONSTRUCTION")permit({"mode","batch_families","duration_seconds","start_ordinal","family_limit","output_directory"});
    else if(op=="ATOM3D_CONSTRUCTION_IDS")permit({"family_ids"});
    else if(op=="ATOM3D_EXPORT")permit({"table","path"});
    else if(op=="LI6_PHASE_CENSUS"||op=="LI6_GRAMMAR"||op=="LI6_ASSEMBLY"||op=="LI6_SOURCE_ENERGY")permit({"digest","refresh"});
    for(auto it=p.begin();it!=p.end();++it)insist(allowed.contains(it.key()),"Unknown request field: "+it.key());
    if(p.contains("source_sha256"))insist(p["source_sha256"]==source_id_,"Request source binding differs");if(p.contains("domain_revision"))insist(p["domain_revision"]=="A3D41-T18-CONTACT-R2","Request domain revision differs");
    if(op=="ATOM3D_STATUS")return status();
    if(op=="A3D41_CONTACT")return contact(p);
    if(op=="LI6_GRAMMAR_READOUT"||op=="LI6_MINIMUM_SET"){auto query=p;if(op=="LI6_MINIMUM_SET")query["include_minimum_states"]=true;return readout(query);}
    if(op=="LI6_ASSEMBLY_RECEIVER")return receiver(p);
    if(op=="LI6_HISTORY")return history(p);
    if(op=="LI6_BUILD"){json result={{"status","PASS"},{"operation",op},{"work","NATIVE_TYPED_SOURCE_ADMISSION"},{"objects",6},{"relations",9},{"ordered_directional_receipts",18},{"typed_center_placements",6},{"source_response_settings",384},{"build_sheet_source_sha256",bundle_["files"]["li6_construction/BUILD_SHEET.json"]["sha256"]},{"physical_tensor_quantities","OPEN_PER_ISOTOPE"},{"physical_prediction_computed",false}};if(boolean(p,"include_ledger",false))result["ledger"]=build_;return result;}
    if(op=="ATOM3D_VALIDATE")return validate(p.at("reference_directory").get<std::string>());
    if(op=="ATOM3D_BENCH")return benchmark(p);
    if(op=="ATOM3D_CONSTRUCTION")return construction(p);
    if(op=="ATOM3D_CONSTRUCTION_IDS")return construction_ids(p);
    if(op=="ATOM3D_EXPORT"){auto name=p.at("table").get<std::string>();auto t=table(name,backend(p));auto path=std::filesystem::absolute(p.at("path").get<std::string>());write_new(path,t.bytes);auto row=table_record(t);row["path"]=path.string();row["source_sha256"]=source_id_;write_new(path.string()+".json",row.dump(2)+"\n");return row;}
    std::vector<std::string> names;if(op=="LI6_PHASE_CENSUS")names={"CURRENTS"};else if(op=="LI6_GRAMMAR")names={"CENTER","GRAMMAR"};else if(op=="LI6_ASSEMBLY")names={"ASSEMBLY"};else if(op=="LI6_SOURCE_ENERGY")names={"ENERGY"};else throw std::invalid_argument("Native ATOM3D operation is not installed: "+op);
    json tables=json::object();for(auto& name:names)tables[name]=table_record(table(name,backend(p),boolean(p,"digest",false),boolean(p,"refresh",false)));
    return {{"status","PASS"},{"operation",op},{"source_sha256",source_id_},{"backend",backend(p)},{"tables",tables},{"complete_source_fiber",true},{"physical_prediction_computed",false},{"residency",status()}};
}
}
