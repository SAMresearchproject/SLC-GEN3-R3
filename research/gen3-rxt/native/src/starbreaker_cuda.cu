#include "starbreaker_backend.hpp"
#include <cuda_runtime.h>
#include <chrono>
#include <stdexcept>
#include <string>

namespace rxt {
namespace {
void ck(cudaError_t e) { if(e!=cudaSuccess) throw std::runtime_error(std::string("Starbreaker CUDA: ")+cudaGetErrorString(e)); }
template<class T> struct Device {
    T* p=nullptr;
    explicit Device(size_t n) { if(n) ck(cudaMalloc(reinterpret_cast<void**>(&p),n*sizeof(T))); }
    ~Device() { if(p) cudaFree(p); }
    Device(const Device&)=delete;
    void load(const std::vector<T>& v) { if(!v.empty()) ck(cudaMemcpy(p,v.data(),v.size()*sizeof(T),cudaMemcpyHostToDevice)); }
};
struct Timer {
    cudaEvent_t a{},b{};
    Timer() { ck(cudaEventCreate(&a)); ck(cudaEventCreate(&b)); }
    ~Timer() { cudaEventDestroy(a); cudaEventDestroy(b); }
    void start() { ck(cudaEventRecord(a)); }
    double end() { ck(cudaGetLastError()); ck(cudaEventRecord(b)); ck(cudaEventSynchronize(b)); float ms=0; ck(cudaEventElapsedTime(&ms,a,b)); return ms/1000.0; }
};
__device__ int64_t feature(uint32_t family,int c,const int64_t* table,const int64_t* inventory) {
    uint32_t a=family, rho=a%128+1; a/=128;
    uint32_t assignment=a%6; a/=6; uint32_t hidden=a%5; a/=5;
    uint32_t pair=a%2; a/=2; uint32_t pattern=a;
    if(c<4) { for(int i=0;i<c;++i) a/=5; return a%5; }
    if(c==4) return hidden;
    if(c==5) return pair;
    if(c==6) return assignment;
    if(c==7) return rho;
    if(c==8) return inventory[(pattern*5+hidden)*2+pair];
    return table[pattern*23+c-9];
}
__device__ int leaf(uint32_t family,int root,const SBNode* nodes,const int64_t* table,const int64_t* inventory) {
    int at=root;
    while(nodes[at].feature>=0) {
        const auto n=nodes[at];
        at=feature(family,n.feature,table,inventory)<=n.threshold?n.left:n.right;
    }
    return at;
}
__global__ void predict_kernel(const uint32_t* ids,size_t count,const int* roots,size_t targets,const SBNode* nodes,const int64_t* table,const int64_t* inventory,int* out) {
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;
    if(i<count*targets) out[i]=leaf(ids[i/targets],roots[i%targets],nodes,table,inventory);
}
__global__ void scan_kernel(uint32_t start,uint32_t count,const int* roots,size_t targets,const SBNode* nodes,const int64_t* table,const int64_t* inventory,unsigned long long* counts) {
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;
    if(i<size_t(count)*targets) atomicAdd(counts+leaf(start+uint32_t(i/targets),roots[i%targets],nodes,table,inventory),1ULL);
}
__device__ uint32_t translated(uint32_t a,const int* delta,int direction=1) {
    uint32_t b=0;
    for(int c=0;c<9;++c) {
        int q=int((a>>c)&1)+2*int((a>>(c+9))&1);
        q=(q+direction*delta[c]+8)%4;
        b|=(uint32_t(q&1)<<c)|(uint32_t(q>>1)<<(c+9));
    }
    return b;
}
__global__ void cycle_kernel(const SBCycle* jobs,size_t count,SBCycleResult* out) {
    size_t i=size_t(blockIdx.x)*blockDim.x+threadIdx.x;
    if(i>=count) return;
    const auto& j=jobs[i]; auto& r=out[i];
    r.addresses[0]=translated(j.initial,j.h);
    for(int k=1;k<=j.steps;++k) r.addresses[k]=translated(r.addresses[k-1],j.v);
    r.recovered=translated(r.addresses[j.steps],j.h,-1);
    for(int k=0;k<4;++k) { int64_t x=j.amplitudes[2*k],y=j.amplitudes[2*k+1]; r.actions[k]=x*x+y*y; }
}
}
struct SBGpu::Impl {
    Device<SBNode> nodes;
    Device<int64_t> features,inventory;
    size_t node_count,bytes;
    explicit Impl(const SBPolicyIR& p):nodes(p.nodes.size()),features(p.features.size()),inventory(p.inventory.size()),node_count(p.nodes.size()),bytes(p.nodes.size()*sizeof(SBNode)+(p.features.size()+p.inventory.size())*8) {
        nodes.load(p.nodes); features.load(p.features); inventory.load(p.inventory);
    }
};
SBGpu::SBGpu(const SBPolicyIR& p):p_(new Impl(p)) {}
SBGpu::~SBGpu() { delete p_; }
size_t SBGpu::resident_bytes() const { return p_->bytes; }
std::vector<int> SBGpu::predict(const std::vector<uint32_t>& ids,const std::vector<int>& roots,SBExecution& execution) {
    auto begin=std::chrono::steady_clock::now(); size_t n=ids.size()*roots.size();
    Device<uint32_t> input(ids.size()); Device<int> selected(roots.size()),output(n);
    input.load(ids); selected.load(roots); Timer timer; timer.start();
    predict_kernel<<<unsigned((n+255)/256),256>>>(input.p,ids.size(),selected.p,roots.size(),p_->nodes.p,p_->features.p,p_->inventory.p,output.p);
    execution.kernel_seconds=timer.end(); std::vector<int> result(n);
    ck(cudaMemcpy(result.data(),output.p,n*sizeof(int),cudaMemcpyDeviceToHost));
    execution.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count(); return result;
}
std::vector<uint64_t> SBGpu::scan(uint32_t start,uint32_t count,const std::vector<int>& roots,SBExecution& execution) {
    auto begin=std::chrono::steady_clock::now(); size_t n=size_t(count)*roots.size();
    Device<int> selected(roots.size()); Device<unsigned long long> output(p_->node_count);
    selected.load(roots); ck(cudaMemset(output.p,0,p_->node_count*sizeof(uint64_t))); Timer timer; timer.start();
    scan_kernel<<<unsigned((n+255)/256),256>>>(start,count,selected.p,roots.size(),p_->nodes.p,p_->features.p,p_->inventory.p,output.p);
    execution.kernel_seconds=timer.end(); std::vector<uint64_t> result(p_->node_count);
    ck(cudaMemcpy(result.data(),output.p,result.size()*8,cudaMemcpyDeviceToHost));
    execution.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count(); return result;
}
std::vector<SBCycleResult> SBGpu::cycles(const std::vector<SBCycle>& jobs,SBExecution& execution) {
    auto begin=std::chrono::steady_clock::now(); Device<SBCycle> input(jobs.size()); Device<SBCycleResult> output(jobs.size());
    input.load(jobs); ck(cudaMemset(output.p,0,jobs.size()*sizeof(SBCycleResult))); Timer timer; timer.start();
    cycle_kernel<<<unsigned((jobs.size()+127)/128),128>>>(input.p,jobs.size(),output.p);
    execution.kernel_seconds=timer.end(); std::vector<SBCycleResult> result(jobs.size());
    ck(cudaMemcpy(result.data(),output.p,result.size()*sizeof(SBCycleResult),cudaMemcpyDeviceToHost));
    execution.wall_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count(); return result;
}
}
