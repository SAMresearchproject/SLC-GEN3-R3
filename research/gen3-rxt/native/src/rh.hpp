#pragma once
#include "engine.hpp"
#include <atomic>
#include <future>
namespace rxt {
class Riemann {
public:
    std::future<json> pending;
    json request;
    std::future<json> batch_pending;
    std::atomic<uint64_t> progress{0};
    unsigned workers;
    explicit Riemann(unsigned n):workers(n){}
    ~Riemann(){if(pending.valid())pending.wait();if(batch_pending.valid())batch_pending.wait();}
    json compute(const json&);
};
}
