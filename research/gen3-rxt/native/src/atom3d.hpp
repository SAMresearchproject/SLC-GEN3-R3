#pragma once
#include "engine.hpp"
#include "atom3d_backend.hpp"

namespace rxt {
class Atom3d {
    Resources resources_;
    std::filesystem::path directory_;
    std::string source_id_;
    json bundle_, grammar_, assembly_, contact_, build_;
    A3DInputs inputs_;
    std::unique_ptr<A3DCuda> gpu_;
    std::vector<int8_t> cpu_currents_;
    std::vector<int16_t> cpu_features_;
    std::map<std::string,A3DMinimum> minima_;
    json construction_set_cache_=json::object();
    void phase_cpu(bool refresh=false);
    void ensure_gpu();
    A3DTable table(const std::string&,const std::string&,bool download=true,bool refresh=false);
    A3DMinimum minimum_cpu(const A3DQuery&);
    json contact(const json&);
    json readout(const json&);
    json receiver(const json&);
    json history(const json&);
    json construction(const json&);
    json construction_ids(const json&);
    json validate(const std::filesystem::path&);
    json benchmark(const json&);
public:
    Atom3d(const std::filesystem::path&,const Resources&);
    json binding() const;
    json status() const;
    json execute(const std::string&,const json&);
};
}
