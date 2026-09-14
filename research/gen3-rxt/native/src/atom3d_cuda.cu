#include "atom3d_backend.hpp"
#include <cuda_runtime.h>
#include <chrono>
#include <stdexcept>
#include <algorithm>
#include <climits>

namespace rxt {
namespace {
using Clock=std::chrono::steady_clock;
void ck(cudaError_t e) { if(e!=cudaSuccess) throw std::runtime_error(std::string("ATOM3D CUDA: ")+cudaGetErrorString(e)); }
template<class T> struct Device {
    T* p=nullptr; size_t n=0;
    ~Device(){if(p)cudaFree(p);}
    void allocate(size_t size){if(n>=size)return;if(p){ck(cudaFree(p));p=nullptr;n=0;}T* next=nullptr;ck(cudaMalloc((void**)&next,size*sizeof(T)));p=next;n=size;}
    void upload(const std::vector<T>& v,cudaStream_t stream){allocate(v.size());ck(cudaMemcpyAsync(p,v.data(),v.size()*sizeof(T),cudaMemcpyHostToDevice,stream));}
};
struct Timer {
    cudaEvent_t begin=nullptr,end=nullptr;
    Timer(){ck(cudaEventCreate(&begin));ck(cudaEventCreate(&end));}
    ~Timer(){if(begin)cudaEventDestroy(begin);if(end)cudaEventDestroy(end);}
    double finish(cudaStream_t stream){ck(cudaEventRecord(end,stream));ck(cudaEventSynchronize(end));float ms;ck(cudaEventElapsedTime(&ms,begin,end));return ms*.001;}
};
__device__ int part(unsigned address,int e,int side,int kind){
    unsigned q=((address>>e)&1u)+2*((address>>(e+9))&1u);
    int x=side==0?int(q==0)-int(q==2):int(q==1)-int(q==3);
    return kind?abs(x):x;
}
__global__ void phase_features(A3DGeometry g,int8_t* currents,int16_t* features){
    size_t row=size_t(blockIdx.x)*blockDim.x+threadIdx.x;if(row>=A3D_ROWS)return;
    unsigned address=unsigned(row/8);int kind=(row/4)%2,mask=row%4;
    int j[12]={},ph[18];
    for(int e=0;e<9;++e){
        int u=g.endpoints[2*e],v=g.endpoints[2*e+1];
        for(int s=0;s<2;++s){int x=part(address,e,s,kind)*g.masks[mask*9+e];ph[s*9+e]=x;j[s*6+u]-=x;j[s*6+v]+=x;}
    }
    for(int i=0;i<12;++i)currents[row*12+i]=int8_t(j[i]);
    for(int e=0;e<3;++e){int k=g.centers[e],u=g.endpoints[k*2],v=g.endpoints[k*2+1];int x=j[u]-j[v],y=j[u+6]-j[v+6];
        features[(e*3+0)*A3D_ROWS+row]=x*x;features[(e*3+1)*A3D_ROWS+row]=2*x*y;features[(e*3+2)*A3D_ROWS+row]=y*y;}
    for(int e=0;e<9;++e){int u=g.endpoints[e*2],v=g.endpoints[e*2+1],x=j[u]-j[v],y=j[u+6]-j[v+6];features[(9+e)*A3D_ROWS+row]=x*x+y*y;}
    for(int c=0;c<5;++c){int x=0,y=0;for(int e=0;e<9;++e){x+=g.cycles[c*9+e]*ph[e];y+=g.cycles[c*9+e]*ph[e+9];}features[(18+c)*A3D_ROWS+row]=x*x+y*y;}
}
__global__ void gather(const int16_t* features,const uint32_t* reps,int16_t* out,size_t rows,int width,int offset){
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;if(i<rows*width)out[i]=features[(offset+i%width)*A3D_ROWS+reps[i/width]];
}
__global__ void contract(const int16_t* features,const uint32_t* reps,const int64_t* coefficients,
                         int64_t* out,size_t rows,int width,int columns,int offset){
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;if(i>=rows*columns)return;
    size_t row=reps[i/columns],col=i%columns;int64_t value=0;
    for(int f=0;f<width;++f)value+=int64_t(features[(offset+f)*A3D_ROWS+row])*coefficients[f*columns+col];
    out[i]=value;
}
__global__ void energy_readout(const int8_t* currents,const int32_t* matrices,int16_t* out,int* error){
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;if(i>=A3D_ROWS*4)return;
    size_t row=i/4;int form=i%4,mask=row%4,value=0;
    for(int side=0;side<2;++side)for(int u=0;u<6;++u)for(int v=0;v<6;++v)
        value+=int(currents[row*12+side*6+u])*matrices[(mask*4+form)*36+u*6+v]*int(currents[row*12+side*6+v]);
    if(value<0||value>32767)atomicExch(error,1);
    out[i]=int16_t(value);
}
__global__ void contact_readout(const A3DContactTask* tasks,const int64_t* forms,int64_t* out,size_t rows){
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;if(i>=rows*24)return;
    auto t=tasks[i/24];unsigned a=t.address;
    for(int k=0;k<t.prefix;++k){int c=t.writes[k*2];unsigned low=(a>>c)&1;a^=(1u<<c)|((low^unsigned(t.writes[k*2+1]<0))<<(c+9));}
    int before[6],after[6];for(int s=0;s<2;++s)for(int k=0;k<3;++k){int c=1+3*k;before[s*3+k]=t.absolute?0:part(t.address,c,s,t.kind);after[s*3+k]=part(a,c,s,t.kind);}
    int64_t value=0;int f=0;for(int u=0;u<6;++u)for(int v=u;v<6;++v,++f)value+=forms[f*24+i%24]*int64_t((u==v?1:2)*(after[u]*after[v]-before[u]*before[v]));out[i]=value;
}
__device__ A3DWide wide_action(int64_t center,int64_t motif){
    // Exact two's-complement signed 128-bit multiply-add. Center may be signed.
    uint64_t u=uint64_t(center),lo=u*576u;int64_t hi=int64_t(__umul64hi(u,576u))-(center<0?576:0);
    uint64_t result=lo+uint64_t(motif);hi+=(motif<0?-1:0)+int64_t(result<lo);return {result,hi};
}
__device__ bool less(A3DWide a,A3DWide b){return a.hi<b.hi||(a.hi==b.hi&&a.lo<b.lo);}
__device__ bool equal(A3DWide a,A3DWide b){return a.hi==b.hi&&a.lo==b.lo;}
__device__ void reduce(A3DWide* values,uint32_t* counts){
    for(int d=128;d;d/=2){__syncthreads();int t=threadIdx.x;if(t<d){auto other=values[t+d];if(less(other,values[t])){values[t]=other;counts[t]=counts[t+d];}else if(equal(other,values[t]))counts[t]+=counts[t+d];}}__syncthreads();
}
__global__ void query_minimum(const int16_t* features,A3DQuery query,A3DWide* all,A3DWide* blocks,uint32_t* counts){
    __shared__ A3DWide v[256];__shared__ uint32_t n[256];
    unsigned state=blockIdx.x*blockDim.x+threadIdx.x;size_t row=size_t(state)*8+query.kind*4+query.mask;
    int64_t c=0,m=0;for(int f=0;f<9;++f)c+=int64_t(features[f*A3D_ROWS+row])*query.center[f];
    for(int f=0;f<14;++f)m+=int64_t(features[(9+f)*A3D_ROWS+row])*query.motif[f];
    auto value=wide_action(c,m);all[state]=value;v[threadIdx.x]=value;n[threadIdx.x]=1;reduce(v,n);
    if(threadIdx.x==0){blocks[blockIdx.x]=v[0];counts[blockIdx.x]=n[0];}
}
__global__ void minimum_finish(A3DWide* blocks,uint32_t* counts,A3DWide* final,uint32_t* total){
    __shared__ A3DWide v[256];__shared__ uint32_t n[256];int t=threadIdx.x;v[t]={UINT64_MAX,INT64_MAX};n[t]=0;
    for(int i=t;i<1024;i+=256){if(less(blocks[i],v[t])){v[t]=blocks[i];n[t]=counts[i];}else if(equal(blocks[i],v[t]))n[t]+=counts[i];}
    reduce(v,n);if(t==0){*final=v[0];*total=n[0];}
}
__global__ void minimum_bits(const A3DWide* all,const A3DWide* best,uint32_t* bits){
    unsigned state=blockIdx.x*blockDim.x+threadIdx.x;unsigned mask=__ballot_sync(0xffffffff,equal(all[state],*best));if(threadIdx.x%32==0)bits[state/32]=mask;
}
__global__ void batch_minimum(const int16_t* features,const A3DQuery* queries,A3DWide* all,A3DWide* blocks,uint32_t* counts){
    __shared__ A3DWide v[256];__shared__ uint32_t n[256];
    size_t index=blockIdx.y;auto query=queries[index];unsigned state=blockIdx.x*256+threadIdx.x;
    size_t row=size_t(state)*8+query.kind*4+query.mask;
    int64_t c=0,m=0;
    for(int f=0;f<9;++f)c+=int64_t(features[f*A3D_ROWS+row])*query.center[f];
    for(int f=0;f<14;++f)m+=int64_t(features[(9+f)*A3D_ROWS+row])*query.motif[f];
    auto value=wide_action(c,m);all[index*ADDRESS_COUNT+state]=value;v[threadIdx.x]=value;n[threadIdx.x]=1;reduce(v,n);
    if(threadIdx.x==0){blocks[index*1024+blockIdx.x]=v[0];counts[index*1024+blockIdx.x]=n[0];}
}
__global__ void batch_finish(const A3DWide* blocks,const uint32_t* counts,A3DWide* final,uint32_t* total){
    __shared__ A3DWide v[256];__shared__ uint32_t n[256];int t=threadIdx.x;size_t offset=size_t(blockIdx.x)*1024;
    v[t]={UINT64_MAX,INT64_MAX};n[t]=0;
    for(int i=t;i<1024;i+=256){if(less(blocks[offset+i],v[t])){v[t]=blocks[offset+i];n[t]=counts[offset+i];}else if(equal(blocks[offset+i],v[t]))n[t]+=counts[offset+i];}
    reduce(v,n);if(t==0){final[blockIdx.x]=v[0];total[blockIdx.x]=n[0];}
}
__global__ void batch_bits(const A3DWide* all,const A3DWide* best,uint32_t* bits){
    unsigned state=blockIdx.x*256+threadIdx.x;size_t index=blockIdx.y;
    unsigned mask=__ballot_sync(0xffffffff,equal(all[index*ADDRESS_COUNT+state],best[index]));
    if(threadIdx.x%32==0)bits[index*(ADDRESS_COUNT/32)+state/32]=mask;
}
}

struct A3DCuda::Impl {
    A3DGeometry geometry;size_t nc=0,ng=0,na=0,nt=0;
    Device<uint32_t> cr,gr,ar;
    Device<int64_t> cc,gc,ac,forms;
    Device<int32_t> energy;Device<A3DContactTask> tasks;
    Device<int8_t> currents;Device<int16_t> features;
    std::map<std::string,Device<uint8_t>> outputs;
    std::map<std::string,A3DTable> layouts;
    Device<int> error;
    Device<A3DWide> all,blocks,best;Device<uint32_t> counts,total,bits;
    Device<A3DQuery> batch_queries;
    Device<A3DWide> batch_all,batch_blocks,batch_best;
    Device<uint32_t> batch_counts,batch_total,batch_set;
    std::vector<A3DBitBuffer> batch_host;
    A3DBitBuffer host_buffer(size_t n){
        for(auto& b:batch_host)if(b.length==n&&b.storage.use_count()==1)return b;
        char* ptr=nullptr;ck(cudaHostAlloc(reinterpret_cast<void**>(&ptr),n,cudaHostAllocPortable));
        A3DBitBuffer b; b.storage=std::shared_ptr<char>(ptr,[](char* p){cudaFreeHost(p);});b.length=n;batch_host.push_back(b);return b;
    }
    cudaStream_t stream=nullptr;bool ready=false;
    ~Impl(){if(stream){cudaStreamSynchronize(stream);cudaStreamDestroy(stream);}}
    double initialize(bool refresh){
        if(ready&&!refresh)return 0;currents.allocate(A3D_ROWS*12);features.allocate(A3D_ROWS*A3D_FEATURES);
        Timer timer;ck(cudaEventRecord(timer.begin,stream));phase_features<<<A3D_ROWS/256,256,0,stream>>>(geometry,currents.p,features.p);ck(cudaGetLastError());double seconds=timer.finish(stream);ready=true;return seconds;
    }
};
static std::vector<int64_t> transpose(const std::vector<int64_t>& v,int columns,int width){std::vector<int64_t> out(v.size());for(int c=0;c<columns;++c)for(int f=0;f<width;++f)out[f*columns+c]=v[c*width+f];return out;}
A3DCuda::A3DCuda(const A3DInputs& in):p_(new Impl){
    try{auto& p=*p_;ck(cudaStreamCreateWithFlags(&p.stream,cudaStreamNonBlocking));p.geometry=in.geometry;
        p.nc=in.center_rep.size();p.ng=in.grammar_rep.size();p.na=in.assembly_rep.size();p.nt=in.contact.size();
        p.cr.upload(in.center_rep,p.stream);p.gr.upload(in.grammar_rep,p.stream);p.ar.upload(in.assembly_rep,p.stream);
        // Synchronize each temporary coefficient upload before releasing its host storage.
        auto upload=[&](auto& target,const auto& data){target.upload(data,p.stream);ck(cudaStreamSynchronize(p.stream));};
        upload(p.cc,transpose(in.center_coeff,384,9));upload(p.gc,transpose(in.grammar_coeff,87,14));upload(p.ac,transpose(in.assembly_coeff,768,9));upload(p.forms,transpose(in.forms,24,21));
        upload(p.energy,in.energy);upload(p.tasks,in.contact);p.error.allocate(1);
    }catch(...){delete p_;p_=nullptr;throw;}
}
A3DCuda::~A3DCuda(){delete p_;}
A3DTable A3DCuda::table(const std::string& name,bool download,bool refresh){
    auto start=Clock::now();auto& p=*p_;A3DTable out;void* ptr=nullptr;size_t bytes=0;
    if(name=="CURRENTS"){
        out.reused=p.ready&&!refresh;out.kernel_seconds=p.initialize(refresh);out.shape={ADDRESS_COUNT,2,4,2,6};out.element_size=1;ptr=p.currents.p;bytes=A3D_ROWS*12;
    }else{
        if(name!="CONTACT")out.kernel_seconds=p.initialize(false);
        if(name=="CONTACT"){out.shape={p.nt,24};out.element_size=8;}
        else if(name=="CENTER"){out.shape={p.nc,384};out.element_size=8;}
        else if(name=="GRAMMAR"){out.shape={p.ng,87};out.element_size=8;}
        else if(name=="ASSEMBLY"){out.shape={p.na,6,128};out.element_size=8;}
        else if(name=="ENERGY"){out.shape={ADDRESS_COUNT,2,4,4};out.element_size=2;}
        else if(name=="CENTER_FEATURES"){out.shape={p.nc,9};out.element_size=2;}
        else if(name=="GRAMMAR_FEATURES"){out.shape={p.ng,14};out.element_size=2;}
        else throw std::invalid_argument("Unknown ATOM3D table");
        bytes=out.element_size;for(auto n:out.shape)bytes*=n;auto& device=p.outputs[name];out.reused=device.n&&!refresh;device.allocate(bytes);ptr=device.p;
        if(!out.reused){Timer timer;ck(cudaEventRecord(timer.begin,p.stream));size_t n=bytes/out.element_size;
            if(name=="CONTACT")contact_readout<<<(n+255)/256,256,0,p.stream>>>(p.tasks.p,p.forms.p,(int64_t*)ptr,p.nt);
            else if(name=="CENTER")contract<<<(n+255)/256,256,0,p.stream>>>(p.features.p,p.cr.p,p.cc.p,(int64_t*)ptr,p.nc,9,384,0);
            else if(name=="GRAMMAR")contract<<<(n+255)/256,256,0,p.stream>>>(p.features.p,p.gr.p,p.gc.p,(int64_t*)ptr,p.ng,14,87,9);
            else if(name=="ASSEMBLY")contract<<<(n+255)/256,256,0,p.stream>>>(p.features.p,p.ar.p,p.ac.p,(int64_t*)ptr,p.na,9,768,0);
            else if(name=="ENERGY"){ck(cudaMemsetAsync(p.error.p,0,sizeof(int),p.stream));energy_readout<<<(n+255)/256,256,0,p.stream>>>(p.currents.p,p.energy.p,(int16_t*)ptr,p.error.p);}
            else gather<<<(n+255)/256,256,0,p.stream>>>(p.features.p,name=="CENTER_FEATURES"?p.cr.p:p.gr.p,(int16_t*)ptr,out.shape[0],out.shape[1],name=="CENTER_FEATURES"?0:9);
            ck(cudaGetLastError());out.kernel_seconds+=timer.finish(p.stream);
            if(name=="ENERGY"){int error=0;ck(cudaMemcpy(&error,p.error.p,sizeof(error),cudaMemcpyDeviceToHost));if(error)throw std::runtime_error("Native source-energy storage bound exceeded");}
        }
    }
    if(download){out.bytes.resize(bytes);ck(cudaMemcpyAsync(out.bytes.data(),ptr,bytes,cudaMemcpyDeviceToHost,p.stream));ck(cudaStreamSynchronize(p.stream));}
    out.wall_seconds=std::chrono::duration<double>(Clock::now()-start).count();return out;
}
A3DMinimum A3DCuda::minimum(const A3DQuery& query){
    auto start=Clock::now();auto& p=*p_;A3DMinimum out;out.kernel_seconds=p.initialize(false);
    p.all.allocate(ADDRESS_COUNT);p.blocks.allocate(1024);p.counts.allocate(1024);p.best.allocate(1);p.total.allocate(1);p.bits.allocate(ADDRESS_COUNT/32);
    Timer timer;ck(cudaEventRecord(timer.begin,p.stream));query_minimum<<<1024,256,0,p.stream>>>(p.features.p,query,p.all.p,p.blocks.p,p.counts.p);ck(cudaGetLastError());
    minimum_finish<<<1,256,0,p.stream>>>(p.blocks.p,p.counts.p,p.best.p,p.total.p);ck(cudaGetLastError());
    minimum_bits<<<1024,256,0,p.stream>>>(p.all.p,p.best.p,p.bits.p);ck(cudaGetLastError());out.kernel_seconds+=timer.finish(p.stream);
    out.bits.resize(ADDRESS_COUNT/8);ck(cudaMemcpyAsync(&out.value,p.best.p,sizeof(out.value),cudaMemcpyDeviceToHost,p.stream));
    ck(cudaMemcpyAsync(&out.count,p.total.p,sizeof(out.count),cudaMemcpyDeviceToHost,p.stream));ck(cudaMemcpyAsync(out.bits.data(),p.bits.p,out.bits.size(),cudaMemcpyDeviceToHost,p.stream));ck(cudaStreamSynchronize(p.stream));
    out.wall_seconds=std::chrono::duration<double>(Clock::now()-start).count();return out;
}
A3DBatchMinimum A3DCuda::minimum_batch(const std::vector<A3DQuery>& queries){
    if(queries.empty()||queries.size()>20480)throw std::invalid_argument("Construction batch requires 1..20480 queries");
    ck(cudaSetDevice(0));auto start=Clock::now();auto& p=*p_;A3DBatchMinimum out;
    out.kernel_seconds=p.initialize(false);size_t n=queries.size();
    p.batch_queries.upload(queries,p.stream);p.batch_all.allocate(n*ADDRESS_COUNT);p.batch_blocks.allocate(n*1024);
    p.batch_best.allocate(n);p.batch_counts.allocate(n*1024);p.batch_total.allocate(n);p.batch_set.allocate(n*(ADDRESS_COUNT/32));
    Timer timer;ck(cudaEventRecord(timer.begin,p.stream));
    batch_minimum<<<dim3(1024,unsigned(n)),256,0,p.stream>>>(p.features.p,p.batch_queries.p,p.batch_all.p,p.batch_blocks.p,p.batch_counts.p);ck(cudaGetLastError());
    batch_finish<<<unsigned(n),256,0,p.stream>>>(p.batch_blocks.p,p.batch_counts.p,p.batch_best.p,p.batch_total.p);ck(cudaGetLastError());
    batch_bits<<<dim3(1024,unsigned(n)),256,0,p.stream>>>(p.batch_all.p,p.batch_best.p,p.batch_set.p);ck(cudaGetLastError());out.kernel_seconds+=timer.finish(p.stream);
    out.values.resize(n);out.counts.resize(n);out.bits=p.host_buffer(n*(ADDRESS_COUNT/8));
    ck(cudaMemcpyAsync(out.values.data(),p.batch_best.p,n*sizeof(A3DWide),cudaMemcpyDeviceToHost,p.stream));
    ck(cudaMemcpyAsync(out.counts.data(),p.batch_total.p,n*sizeof(uint32_t),cudaMemcpyDeviceToHost,p.stream));
    ck(cudaMemcpyAsync(out.bits.data(),p.batch_set.p,out.bits.size(),cudaMemcpyDeviceToHost,p.stream));ck(cudaStreamSynchronize(p.stream));
    out.wall_seconds=std::chrono::duration<double>(Clock::now()-start).count();return out;
}
size_t A3DCuda::resident_bytes()const{auto& p=*p_;size_t n=p.currents.n+p.features.n*2+(p.cr.n+p.gr.n+p.ar.n)*4+(p.cc.n+p.gc.n+p.ac.n+p.forms.n)*8+p.energy.n*4+p.tasks.n*sizeof(A3DContactTask)+(p.all.n+p.blocks.n+p.best.n)*sizeof(A3DWide)+(p.counts.n+p.total.n+p.bits.n)*4+4;n+=p.batch_queries.n*sizeof(A3DQuery)+(p.batch_all.n+p.batch_blocks.n+p.batch_best.n)*sizeof(A3DWide)+(p.batch_counts.n+p.batch_total.n+p.batch_set.n)*4;for(auto& item:p.outputs)n+=item.second.n;return n;}
}
