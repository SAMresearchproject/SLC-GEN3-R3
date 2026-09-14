#include "backend.hpp"
#include <cuda_runtime.h>
#include <chrono>
#include <stdexcept>
#include <algorithm>
#include <limits>

namespace rxt {
using Clock = std::chrono::steady_clock;
static void check(cudaError_t e) {
    if (e != cudaSuccess) throw std::runtime_error(std::string("CUDA: ") + cudaGetErrorString(e));
}
template<class T> struct Buffer {
    T* p = nullptr;
    size_t capacity = 0;
    ~Buffer() { if (p) cudaFree(p); }
    void reserve(size_t n) {
        if (n <= capacity) return;
        T* next = nullptr;
        check(cudaMalloc(reinterpret_cast<void**>(&next), n * sizeof(T)));
        if (p) cudaFree(p);
        p = next; capacity = n;
    }
    void upload(const std::vector<T>& x, cudaStream_t stream) {
        reserve(x.size());
        if (!x.empty()) check(cudaMemcpyAsync(p, x.data(), x.size()*sizeof(T), cudaMemcpyHostToDevice, stream));
    }
};
struct EventTimer {
    cudaEvent_t start = nullptr, end = nullptr;
    EventTimer() { check(cudaEventCreate(&start)); check(cudaEventCreate(&end)); }
    ~EventTimer() { if(start) cudaEventDestroy(start); if(end) cudaEventDestroy(end); }
    double seconds() { float ms=0; check(cudaEventElapsedTime(&ms,start,end)); return ms/1000.0; }
};

__device__ uint32_t write_bits(uint32_t address, Event event) {
    unsigned low=(address >> event.coordinate)&1u;
    return address ^ (1u<<event.coordinate) ^ ((low ^ unsigned(event.direction<0)) << (event.coordinate+9));
}
__device__ int phase(uint32_t a, int c) {
    return int(((a>>c)&1u) | (((a>>(c+9))&1u)<<1));
}
__device__ int component(int phase_value, int side) {
    // (1,0), (0,1), (-1,0), (0,-1).
    return side == 0 ? (phase_value==0)-(phase_value==2) : (phase_value==1)-(phase_value==3);
}
__global__ void compile_contacts(const uint32_t* addresses, int32_t* out, size_t n, int c0, int c1, int c2) {
    size_t i=blockIdx.x*size_t(blockDim.x)+threadIdx.x;
    if (i>=n) return;
    if (c0<0) { out[i]=0; return; }
    uint32_t a=addresses[i];
    int p0=phase(a,c0), p1=phase(a,c1), p2=phase(a,c2);
    int x=component(p0,0)*component(p2,0)+component(p0,1)*component(p2,1);
    int y=component(p1,0)*component(p2,0)+component(p1,1)*component(p2,1);
    out[i]=6-2*x+2*y;
}
__global__ void compile_frames(const uint32_t* addresses, const int64_t* weights,
                               int64_t* out, size_t n, size_t channels) {
    size_t i=blockIdx.x*size_t(blockDim.x)+threadIdx.x;
    if (i>=n*channels) return;
    size_t ch=i/n, state=i%n, half=channels/2;
    uint32_t a=addresses[state];
    int64_t total=0;
    for(int c=0;c<9;++c) {
        int p=phase(a,c), x=component(p,0), y=component(p,1);
        if (ch>=half) { x=abs(x); y=abs(y); }
        total+=weights[(ch%half)*18+c]*x + weights[(ch%half)*18+9+c]*y;
    }
    out[i]=total;
}
__global__ void execute_histories(const uint32_t* initial, const uint16_t* program,
                                  const Event* events, const int32_t* index,
                                  const uint8_t* admitted, const int32_t* contacts,
                                  uint32_t* states, int32_t* actions,
                                  unsigned long long* error, size_t count,
                                  size_t steps, size_t domain_size) {
    size_t lane=blockIdx.x*size_t(blockDim.x)+threadIdx.x;
    if(lane>=count) return;
    uint32_t q=initial[lane];
    int32_t qi=index[q];
    states[lane]=q; actions[lane]=contacts[qi];
    for(size_t step=0;step<steps;++step) {
        uint16_t ev=program[step*count+lane];
        if (!admitted[size_t(ev)*domain_size+qi]) {
            atomicMin(error, static_cast<unsigned long long>(step*count+lane));
            return;
        }
        q=write_bits(q,events[ev]);
        qi=index[q]; // closure is checked when compiling the source contract
        size_t at=(step+1)*count+lane;
        states[at]=q; actions[at]=contacts[qi];
    }
}
__global__ void complete_map(uint32_t* out) {
    size_t i=blockIdx.x*size_t(blockDim.x)+threadIdx.x;
    if(i>=size_t(18)*ADDRESS_COUNT) return;
    int e=int(i/ADDRESS_COUNT);
    out[i]=write_bits(uint32_t(i%ADDRESS_COUNT), {e%9, e<9?1:-1});
}

struct CudaBackend::Impl {
    Buffer<int32_t> index, contacts;
    Buffer<uint32_t> addresses, initial, states;
    Buffer<Event> events;
    Buffer<uint8_t> admitted;
    Buffer<int64_t> weights, frames;
    Buffer<uint16_t> program;
    Buffer<int32_t> actions;
    Buffer<unsigned long long> error;
    cudaStream_t stream=nullptr;
    size_t domain=0, channels=0;
    ~Impl() { if(stream) { cudaStreamSynchronize(stream); cudaStreamDestroy(stream); } }
};
CudaBackend::CudaBackend(const Tables& t):impl_(new Impl) {
    try {
        auto& p=*impl_;
        check(cudaStreamCreateWithFlags(&p.stream,cudaStreamNonBlocking));
        p.domain=t.addresses.size(); p.channels=t.channels;
        p.index.upload(t.index,p.stream); p.addresses.upload(t.addresses,p.stream);
        p.events.upload(t.events,p.stream); p.admitted.upload(t.admitted,p.stream);
        p.weights.upload(t.weights,p.stream);
        p.contacts.reserve(p.domain); p.frames.reserve(p.domain*p.channels); p.error.reserve(1);
        compile_contacts<<<(p.domain+255)/256,256,0,p.stream>>>(p.addresses.p,p.contacts.p,p.domain,
            t.contact_coordinates[0],t.contact_coordinates[1],t.contact_coordinates[2]);
        check(cudaGetLastError());
        compile_frames<<<(p.domain*p.channels+255)/256,256,0,p.stream>>>(p.addresses.p,p.weights.p,p.frames.p,p.domain,p.channels);
        check(cudaGetLastError()); check(cudaStreamSynchronize(p.stream));
    } catch (...) { delete impl_; impl_=nullptr; throw; }
}
CudaBackend::~CudaBackend() { delete impl_; }
Trace CudaBackend::run(const Batch& b) {
    auto begin=Clock::now(); auto& p=*impl_;
    Trace out; out.count=b.count; out.steps=b.steps; out.backend="CUDA_SM120";
    size_t points=b.count*(b.steps+1);
    out.states.resize(points); out.actions.resize(points);
    p.states.reserve(points); p.actions.reserve(points);
    p.initial.upload(b.initial,p.stream); p.program.upload(b.events,p.stream);
    check(cudaMemsetAsync(p.error.p,255,sizeof(unsigned long long),p.stream));
    EventTimer timer;
    check(cudaEventRecord(timer.start,p.stream));
    execute_histories<<<(b.count+255)/256,256,0,p.stream>>>(p.initial.p,p.program.p,p.events.p,
        p.index.p,p.admitted.p,p.contacts.p,p.states.p,p.actions.p,p.error.p,b.count,b.steps,p.domain);
    check(cudaGetLastError()); check(cudaEventRecord(timer.end,p.stream));
    unsigned long long error=std::numeric_limits<unsigned long long>::max();
    check(cudaMemcpyAsync(&error,p.error.p,sizeof(error),cudaMemcpyDeviceToHost,p.stream));
    check(cudaMemcpyAsync(out.states.data(),p.states.p,points*sizeof(uint32_t),cudaMemcpyDeviceToHost,p.stream));
    check(cudaMemcpyAsync(out.actions.data(),p.actions.p,points*sizeof(int32_t),cudaMemcpyDeviceToHost,p.stream));
    check(cudaStreamSynchronize(p.stream));
    if(error!=std::numeric_limits<unsigned long long>::max())
        throw std::invalid_argument("Event not admitted at step "+std::to_string(error/b.count)+", lane "+std::to_string(error%b.count));
    out.kernel_seconds=timer.seconds();
    out.wall_seconds=std::chrono::duration<double>(Clock::now()-begin).count();
    out.transfer_seconds=out.wall_seconds-out.kernel_seconds;
    return out;
}
std::vector<uint32_t> CudaBackend::map() {
    Buffer<uint32_t> d; d.reserve(size_t(18)*ADDRESS_COUNT);
    complete_map<<<(18*ADDRESS_COUNT+255)/256,256,0,impl_->stream>>>(d.p);
    check(cudaGetLastError());
    std::vector<uint32_t> out(size_t(18)*ADDRESS_COUNT);
    check(cudaMemcpyAsync(out.data(),d.p,out.size()*sizeof(uint32_t),cudaMemcpyDeviceToHost,impl_->stream));
    check(cudaStreamSynchronize(impl_->stream));
    return out;
}
std::vector<int64_t> CudaBackend::frames() {
    std::vector<int64_t> out(impl_->domain*impl_->channels);
    check(cudaMemcpyAsync(out.data(),impl_->frames.p,out.size()*sizeof(int64_t),cudaMemcpyDeviceToHost,impl_->stream));
    check(cudaStreamSynchronize(impl_->stream));
    return out;
}
CudaInfo CudaBackend::info() {
    cudaDeviceProp p; check(cudaGetDeviceProperties(&p,0));
    CudaInfo out; out.name=p.name; out.major=p.major; out.minor=p.minor; out.sms=p.multiProcessorCount;
    out.threads_per_sm=p.maxThreadsPerMultiProcessor; out.shared_per_sm=int(p.sharedMemPerMultiprocessor);
    check(cudaMemGetInfo(&out.free_bytes,&out.total_bytes)); return out;
}
}
