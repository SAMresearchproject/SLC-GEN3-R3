#pragma once
#include <nlohmann/json.hpp>
#include <gmpxx.h>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <stdexcept>
#include <string>
using json=nlohmann::json;
namespace rxt {
inline void need(bool b,const std::string& s){if(!b)throw std::invalid_argument(s);}
inline mpq_class rational(const json& j){
 need(j.is_string()||j.is_number_integer(),"Exact integer or rational string required");
 std::string s=j.is_string()?j.get<std::string>():j.dump();
 auto slash=s.find('/');auto digits=[](std::string x){if(!x.empty()&&x[0]=='-')x.erase(0,1);return !x.empty()&&std::all_of(x.begin(),x.end(),[](char c){return c>='0'&&c<='9';});};
 need(digits(s.substr(0,slash))&&(slash==std::string::npos||digits(s.substr(slash+1))),"Invalid exact rational");
 if(slash!=std::string::npos)need(mpz_class(s.substr(slash+1))!=0,"Zero denominator");
 mpq_class q(s);q.canonicalize();return q;
}
inline json number(mpq_class q){q.canonicalize();return q.get_str();}
}
