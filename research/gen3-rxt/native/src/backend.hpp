#pragma once
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace rxt {
constexpr uint32_t ADDRESS_COUNT = 1u << 18;
constexpr const char* VERSION = "GEN3-RXT-R7.1";
struct Event { int coordinate; int direction; };
struct Tables {
    std::vector<int32_t> index;
    std::vector<uint32_t> addresses;
    std::vector<Event> events;
    std::vector<uint8_t> admitted; // event-major, state-minor
    std::vector<int32_t> contacts;
    std::vector<int64_t> frames; // channel-major, state-minor
    std::vector<int64_t> weights; // signed channel-major, 18 phase components
    int contact_coordinates[3] = {-1, -1, -1};
    size_t channels = 0;
};
struct Batch {
    size_t count = 0, steps = 0;
    std::vector<uint32_t> initial;
    std::vector<uint16_t> events; // step-major, history-minor
};
struct Trace {
    size_t count = 0, steps = 0;
    std::vector<uint32_t> states; // point-major, history-minor
    std::vector<int32_t> actions;
    double kernel_seconds = 0, transfer_seconds = 0, wall_seconds = 0;
    std::string backend;
    unsigned cpu_workers = 0;
};
struct CudaInfo {
    std::string name;
    int major = 0, minor = 0, sms = 0, threads_per_sm = 0, shared_per_sm = 0;
    size_t free_bytes = 0, total_bytes = 0;
};
class CudaBackend {
    struct Impl;
    Impl* impl_;
public:
    explicit CudaBackend(const Tables&);
    ~CudaBackend();
    CudaBackend(const CudaBackend&) = delete;
    CudaBackend& operator=(const CudaBackend&) = delete;
    Trace run(const Batch&);
    // Complete packed map in the original +/-, coordinate, address order.
    std::vector<uint32_t> map();
    std::vector<int64_t> frames();
    static CudaInfo info();
};
Trace run_cpu(const Tables&, const Batch&, unsigned threads);
}
