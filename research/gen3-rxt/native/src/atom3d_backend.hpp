#pragma once
#include "backend.hpp"
#include <array>
#include <map>
#include <memory>
#include <cstring>

namespace rxt {
constexpr size_t A3D_ROWS = size_t(ADDRESS_COUNT)*8;
constexpr int A3D_FEATURES = 23;
struct A3DGeometry {
    int endpoints[18]{};
    int masks[36]{};
    int cycles[45]{};
    int centers[3]{};
};
struct A3DContactTask {
    uint32_t address=0;
    int prefix=0, kind=0, absolute=0;
    int writes[6]{};
};
struct A3DInputs {
    A3DGeometry geometry;
    std::vector<uint32_t> center_rep, grammar_rep, assembly_rep;
    std::vector<int64_t> center_coeff, grammar_coeff, assembly_coeff, tensors, eta_bound;
    std::vector<int32_t> energy;
    std::vector<A3DContactTask> contact;
    std::vector<int64_t> forms;
};
// Center is in native integer units; motif is in units of 1/576.
// Scaling the center by 576 needs signed 128-bit accumulation.
struct A3DQuery {
    int kind=0, mask=3;
    int64_t center[9]{}, motif[14]{};
};
struct A3DWide { uint64_t lo=0; int64_t hi=0; };
struct A3DMinimum {
    A3DWide value;
    uint32_t count=0;
    std::vector<uint8_t> bits;
    double kernel_seconds=0, wall_seconds=0;
};
struct A3DTable {
    std::string bytes;
    std::vector<size_t> shape;
    size_t element_size=0;
    double kernel_seconds=0, wall_seconds=0;
    bool reused=false;
};
struct A3DBitBuffer {
    std::shared_ptr<char> storage;
    size_t length=0;
    char* data() const { return storage.get(); }
    size_t size() const { return length; }
    std::string substr(size_t offset,size_t count) const { return std::string(data()+offset,count); }
    bool operator==(const A3DBitBuffer& other) const { return length==other.length && std::memcmp(data(),other.data(),length)==0; }
};
struct A3DBatchMinimum {
    std::vector<A3DWide> values;
    std::vector<uint32_t> counts;
    A3DBitBuffer bits;
    double kernel_seconds=0,wall_seconds=0;
};
class A3DCuda {
    struct Impl;
    Impl* p_;
public:
    explicit A3DCuda(const A3DInputs&);
    ~A3DCuda();
    A3DCuda(const A3DCuda&)=delete;
    A3DCuda& operator=(const A3DCuda&)=delete;
    A3DTable table(const std::string&, bool download, bool refresh=false);
    A3DMinimum minimum(const A3DQuery&);
    A3DBatchMinimum minimum_batch(const std::vector<A3DQuery>&);
    size_t resident_bytes() const;
};
}
