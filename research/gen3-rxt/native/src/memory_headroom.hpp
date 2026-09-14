#pragma once
#include <algorithm>
#include <cstdint>
namespace rxt {
// Conservative clean, unmapped, inactive filesystem cache allowance. Dirty,
// writeback, mapped and shared-memory counts are each excluded even when they
// overlap or lie outside inactive_file. No slab or active-file credit is used.
inline uint64_t clean_inactive_cache(uint64_t current,uint64_t inactive,uint64_t file,
                                    uint64_t dirty,uint64_t writeback,uint64_t mapped,uint64_t shmem){
    uint64_t bytes=std::min({current,inactive,file});
    for(auto excluded:{dirty,writeback,mapped,shmem})bytes-=std::min(bytes,excluded);
    return bytes;
}
inline uint64_t bounded_host_headroom(uint64_t limit,uint64_t current,uint64_t reclaimable,uint64_t host_available){
    const auto working=current-std::min(current,reclaimable);
    return std::min(limit-std::min(limit,working),host_available);
}
}
