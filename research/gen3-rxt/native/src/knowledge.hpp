#pragma once
#include "engine.hpp"
#include <fstream>
namespace rxt {
class ConstructionKnowledge {
    std::filesystem::path directory_;
    json bundle_,dictionary_,batches_;
    std::ifstream outcomes_;
    std::string bundle_sha_;
public:
    ConstructionKnowledge(const std::filesystem::path&,const std::string&,const Resources&);
    json binding() const;
    json status() const;
    bool contains(uint32_t) const;
    json outcome(uint32_t);
    json labels(const json&,const json&) const;
    std::string bits(const std::string&) const;
};
std::string file_sha256(const std::filesystem::path&);
}
