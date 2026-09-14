#pragma once
#include "engine.hpp"
#include "starbreaker_backend.hpp"
#include <map>
#include <tuple>

namespace rxt {
constexpr const char* SB_VERSION="SB-GEN3-RXT-R1";
class Starbreaker {
    Resources resources_;
    json binding_, policy_, source_binding_;
    std::string source_id_;
    SBPolicyIR ir_;
    std::vector<std::string> names_;
    std::vector<json> nodes_;
    std::vector<int> node_models_;
    std::map<std::tuple<std::string,std::string,uint32_t>,std::array<json,4>> packets_;
    std::map<std::pair<std::string,int>,json> responses_;
    std::unique_ptr<SBGpu> gpu_;
    int flatten(const json&,const json&,int);
    std::vector<int> targets(const json&) const;
    std::string backend(const json&,size_t) const;
    SBGpu& gpu();
    json policies(const json&,bool);
    json accumulate(const json&,json&,Store*);
public:
    Starbreaker(const std::filesystem::path&,const Resources&);
    const json& binding() const { return binding_; }
    const json& policy() const { return policy_; }
    json status() const;
    json execute(const std::string&,const json&,json&,Store*);
    void adopt(const std::string&,const json&);
    const SBPolicyIR& policy_ir() const { return ir_; }
    const std::vector<std::string>& target_names() const { return names_; }
    json campaign_requests(uint64_t,size_t,const std::string&) const;
};
}
