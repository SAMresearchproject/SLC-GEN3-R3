#pragma once
#include "backend.hpp"
#include <gmpxx.h>
#include <nlohmann/json.hpp>
#include <filesystem>
#include <memory>
#include <future>
#include <map>
#include <set>

namespace rxt {
using json = nlohmann::json;
std::string hash(const std::string&);
json read_json(const std::filesystem::path&);
mpq_class rational(const json&);
json number(const mpq_class&);
json log_value(const mpq_class&);
json log_account(const json&);

struct Resources {
    unsigned cpu_threads = 1;
    uint64_t host_limit = 0, host_current = 0, host_reclaimable = 0, host_budget = 0, gpu_budget = 0;
    double cpu_quota = 1;
    json describe() const;
    static Resources detect();
    void admit(uint64_t host_bytes, uint64_t device_bytes = 0) const;
};

class Contract {
public:
    json source;
    std::string id;
    Tables tables;
    std::vector<int> coordinates;
    std::vector<std::string> labels;
    std::vector<mpz_class> denominators;
    bool has_contact = false;
    explicit Contract(const json&, const Resources&);
    uint32_t encode(const json&) const;
    json decode(uint32_t) const;
    json frame(uint32_t, const std::string& view = "JOINT") const;
    Batch batch(const json&) const;
    json describe() const;
    json describe_trace(const Batch&, const Trace&, size_t lane) const;
};

class Store {
    std::filesystem::path root_;
    int lock_fd_ = -1;
    mutable std::set<std::string> validated_runs_;
public:
    explicit Store(const std::filesystem::path&);
    ~Store();
    Store(const Store&) = delete;
    Store& operator=(const Store&) = delete;
    std::string put(const json&);
    json get(const std::string&) const;
    std::string commit(const json&);
    json restore() const;
    std::string remember(const std::string& key, const json&);
    json recall(const std::string& key) const;
};

class Atom3d;
class Starbreaker;
class ConstructionKnowledge;
class TrainingData;
class Riemann;
class Engine {
    Resources resources_;
    std::unique_ptr<Contract> contract_;
    std::unique_ptr<CudaBackend> gpu_;
    std::unique_ptr<Store> store_;
    std::unique_ptr<Atom3d> atom3d_;
    std::unique_ptr<Starbreaker> starbreaker_;
    std::unique_ptr<ConstructionKnowledge> construction_memory_;
    std::unique_ptr<TrainingData> training_;
    std::unique_ptr<Riemann> rh_;
    std::future<json> joint_prefetch_;
    json joint_prefetch_ids_;
    size_t joint_drain_remaining_=0;
    std::string joint_prediction_object_;
    std::map<uint32_t,json> joint_predictions_;
    std::set<std::string> joint_saved_sets_;
    json state_ = {{"schema", "GEN_RXT_MACHINE_V1"}, {"version", VERSION},
                   {"sequence", 0}, {"runs", json::array()},
                   {"knowledge", json::object()}, {"accounts", json::object()}};
public:
    Engine();
    ~Engine();
    json execute(const json&);
    Trace run(const Batch&, const std::string& backend);
    const Contract& contract() const;
    const Resources& resources() const { return resources_; }
private:
    json checkpoint();
    json inverse(const json&);
    json joint(const std::string&,const json&);
    json core(const std::string&,const json&);
    json train(const std::string&,const json&);
    json horizon(const std::string&,const json&);
    json campaign(const std::string&,const json&);
    json rh(const std::string&,const json&);
    json transfer(const std::string&,const json&);
    Trace learned_run(const Batch&,json&,uint64_t&,uint64_t&);
};
}
