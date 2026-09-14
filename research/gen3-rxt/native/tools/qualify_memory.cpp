#include "../src/memory_headroom.hpp"
#include <cassert>
#include <iostream>
#include <limits>
int main(){using namespace rxt;
 assert(clean_inactive_cache(100,70,80,5,4,3,2)==56);
 assert(clean_inactive_cache(100,70,80,80,4,3,2)==0);
 assert(clean_inactive_cache(20,70,80,0,0,0,0)==20);
 assert(clean_inactive_cache(100,70,30,0,0,0,0)==30);
 assert(clean_inactive_cache(100,70,80,std::numeric_limits<uint64_t>::max(),1,1,1)==0);
 assert(bounded_host_headroom(100,99,56,1000)==57);
 assert(bounded_host_headroom(100,120,0,1000)==0);
 assert(bounded_host_headroom(100,99,56,8)==8);
 assert(bounded_host_headroom(100,10,900,1000)==100);
 std::cout<<"{\"status\":\"PASS\",\"checks\":9,\"policy\":\"conservative clean inactive cache; cgroup limit and host MemAvailable retained\"}\n";
}
