#pragma once
#include "engine.hpp"
#include "starbreaker_backend.hpp"
#include <array>
#include <map>
namespace rxt {
class TrainingData {
public:
    json bundle, plan, binding;
    std::vector<std::array<int16_t,32>> x;
    std::vector<std::array<uint8_t,45>> y;
    std::vector<uint32_t> ids;
    std::vector<uint8_t> split;
    std::vector<int32_t> index;
    std::array<uint8_t,625> pattern_split{};
    std::array<int,32> maximum{};
    std::string signature;
    TrainingData(const std::filesystem::path&,const SBPolicyIR&,const Resources&);
    void append(const json&,const SBPolicyIR&);
    void seal();
    json status() const;
};
}
