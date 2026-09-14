#pragma once
#include <array>
#include <cstdint>
#include <vector>

namespace rxt {
struct SBNode { int feature=-1, left=-1, right=-1; int64_t threshold=0; };
struct SBPolicyIR {
    std::vector<SBNode> nodes;
    std::vector<int> roots;
    std::vector<int64_t> features, inventory;
};
struct SBCycle {
    uint32_t initial=0;
    int steps=4;
    int h[9]{}, v[9]{};
    int64_t amplitudes[8]{};
};
struct SBCycleResult {
    uint32_t addresses[65]{}, recovered=0;
    int64_t actions[4]{};
};
struct SBExecution { double kernel_seconds=0, wall_seconds=0; };
void sb_features(const SBPolicyIR&, uint32_t, int64_t*);
int sb_leaf(const SBPolicyIR&, uint32_t, int);
SBCycleResult sb_cycle_cpu(const SBCycle&);
class SBGpu {
    struct Impl;
    Impl* p_;
public:
    explicit SBGpu(const SBPolicyIR&);
    ~SBGpu();
    SBGpu(const SBGpu&)=delete;
    std::vector<int> predict(const std::vector<uint32_t>&, const std::vector<int>&, SBExecution&);
    std::vector<uint64_t> scan(uint32_t, uint32_t, const std::vector<int>&, SBExecution&);
    std::vector<SBCycleResult> cycles(const std::vector<SBCycle>&, SBExecution&);
    size_t resident_bytes() const;
};
}
