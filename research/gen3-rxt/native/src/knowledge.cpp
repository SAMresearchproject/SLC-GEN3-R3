#include "knowledge.hpp"
#include <openssl/evp.h>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <stdexcept>
namespace rxt {
namespace {
void check(bool b,const std::string& s) { if(!b) throw std::invalid_argument("Construction memory: "+s); }
uint64_t le(const unsigned char* p,int n) { uint64_t x=0;for(int i=0;i<n;++i)x|=uint64_t(p[i])<<(8*i);return x; }
}
std::string file_sha256(const std::filesystem::path& path) {
    std::ifstream f(path,std::ios::binary);check(bool(f),"Cannot read "+path.string());
    auto* raw=EVP_MD_CTX_new();check(raw!=nullptr,"Digest allocation failed");
    std::unique_ptr<EVP_MD_CTX,decltype(&EVP_MD_CTX_free)> ctx(raw,EVP_MD_CTX_free);
    check(EVP_DigestInit_ex(ctx.get(),EVP_sha256(),nullptr)==1,"Digest initialization failed");
    char block[65536];while(f) { f.read(block,sizeof(block));if(f.gcount())check(EVP_DigestUpdate(ctx.get(),block,size_t(f.gcount()))==1,"Digest update failed"); }
    check(f.eof(),"Source read failed");unsigned char out[EVP_MAX_MD_SIZE];unsigned size=0;check(EVP_DigestFinal_ex(ctx.get(),out,&size)==1,"Digest finish failed");
    std::ostringstream text;text<<std::hex<<std::setfill('0');for(unsigned i=0;i<size;++i)text<<std::setw(2)<<unsigned(out[i]);return text.str();
}
ConstructionKnowledge::ConstructionKnowledge(const std::filesystem::path& directory,const std::string& expected,const Resources& resources):directory_(std::filesystem::absolute(directory)),bundle_sha_(expected) {
    check(file_sha256(directory_/"BUNDLE.json")==expected,"Source bundle differs");bundle_=read_json(directory_/"BUNDLE.json");
    check(bundle_.at("schema")=="A3D41_ACQUIRED_CONSTRUCTION_MEMORY_V1","Source schema differs");
    check(bundle_.at("record_bytes")==704&&bundle_.at("contexts")==32&&bundle_.at("family_space")==4800000,"Memory encoding differs");
    resources.admit(16*1024*1024);
    for(auto i=bundle_.at("files").begin();i!=bundle_["files"].end();++i) {
        check(i.key().find('/')==std::string::npos&&i.key().find("..") == std::string::npos,"Invalid source filename");
        check(file_sha256(directory_/i.key())==i.value().get<std::string>(),"Source file differs: "+i.key());
    }
    dictionary_=read_json(directory_/"MINIMUM_SET_DICTIONARY.json");batches_=read_json(directory_/"SOURCE_BATCHES.json");
    check(dictionary_.size()==bundle_.at("minimum_set_count"),"Minimum-set dictionary differs");
    check(std::filesystem::file_size(directory_/"OUTCOMES.bin")==bundle_.at("completed_families").get<uint64_t>()*704,"Outcome extent differs");
    check(std::filesystem::file_size(directory_/"MINIMUM_SETS.bin")==dictionary_.size()*32768,"Minimum-set extent differs");
    outcomes_.open(directory_/"OUTCOMES.bin",std::ios::binary);check(bool(outcomes_),"Cannot open observations");
}
json ConstructionKnowledge::binding() const {return {{"directory",directory_.string()},{"bundle_sha256",bundle_sha_},{"source_domain_sha256",bundle_["source_domain_sha256"]},{"policy_sha256",bundle_["policy_sha256"]}};}
json ConstructionKnowledge::status() const {return {{"status","ACQUIRED"},{"source",binding()},{"completed_families",bundle_["completed_families"]},{"context_results",bundle_["completed_families"].get<uint64_t>()*32},{"complete_minimum_sets",dictionary_.size()},{"acquired_models",45},{"completed_training_lessons",1906},{"training_state","OWNER_PAUSED"},{"access","EXACT_NATIVE_OUTCOMES_BY_FAMILY_ID"}};}
bool ConstructionKnowledge::contains(uint32_t id) const {if(id>=4800000)return false;uint64_t ordinal=((uint64_t(id)+4800000-bundle_["offset"].get<uint64_t>())%4800000*bundle_["inverse_stride"].get<uint64_t>())%4800000;return ordinal<bundle_["completed_families"].get<uint64_t>();}
json ConstructionKnowledge::outcome(uint32_t id) {
    check(contains(id),"Family has no acquired exact outcome");
    uint64_t ordinal=((uint64_t(id)+4800000-bundle_["offset"].get<uint64_t>())%4800000*bundle_["inverse_stride"].get<uint64_t>())%4800000;
    unsigned char record[704];outcomes_.clear();outcomes_.seekg(std::streamoff(ordinal*704));outcomes_.read(reinterpret_cast<char*>(record),sizeof(record));check(outcomes_.gcount()==704,"Outcome record is incomplete");
    json contexts=json::array();
    for(int c=0;c<32;++c) {
        const auto* p=record+c*22;uint64_t low=le(p,8),high=le(p+8,8);mpz_class numerator(std::to_string(high));numerator<<=64;numerator+=mpz_class(std::to_string(low));
        if(high>>63) {mpz_class sign=1;sign<<=128;numerator-=sign;}
        mpq_class minimum(numerator,mpz_class(576));minimum.canonicalize();auto count=le(p+16,4),slot=le(p+20,2);
        check(slot<dictionary_.size()&&dictionary_[slot]["count"]==count,"Stored count and minimum set differ");const auto& set=dictionary_[slot];
        contexts.push_back({{"context",c},{"minimum",minimum.get_str()},{"count",count},{"set",set["sha256"]},{"single_quarter_turn_orbit",set["single_quarter_turn_orbit"]},{"four_states",set["four_states"]}});
    }
    auto batch=std::upper_bound(batches_.begin(),batches_.end(),ordinal,[](uint64_t n,const json& b){return n<b["ordinal"].get<uint64_t>();});
    check(batch!=batches_.begin(),"Missing source batch ancestry");--batch;check(ordinal<batch->at("ordinal").get<uint64_t>()+batch->at("families").get<uint64_t>(),"Source batch interval differs");
    return {{"schema","A3D41_EXACT_CONSTRUCTION_OUTCOME_V1"},{"family_id",id},{"source_contract","A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1"},{"source_domain_sha256",bundle_["source_domain_sha256"]},{"origin","ACQUIRED_SIMULATION"},{"source_batch",*batch},{"source_ordinal",ordinal},{"memory_bundle_sha256",bundle_sha_},{"contexts",contexts}};
}
json ConstructionKnowledge::labels(const json& outcome,const json& policy) const {
    check(outcome.at("source_contract")=="A3D41_TYPED_CONSTRUCTION_CAMPAIGN_V1"&&outcome.at("source_domain_sha256")==bundle_.at("source_domain_sha256"),"Outcome belongs to another source");
    const auto& c=outcome.at("contexts");check(c.size()==32,"Complete context set required");for(int i=0;i<32;++i)check(c[i].at("context")==i,"Context order differs");
    json actual=json::object();
    for(auto i=policy.at("models").begin();i!=policy["models"].end();++i) {
        const auto& m=i.value().at("target_definition").at("meaning");bool value=false;
        if(i.key()=="shared_four_state_orbit") value=c[3]["count"]==4&&c[3]["set"]==c[11]["set"]&&c[3].at("single_quarter_turn_orbit").get<bool>();
        else if(i.key()=="channel_minimum_sets_agree")value=c[3]["set"]==c[11]["set"];
        else if(m.contains("count_threshold"))value=c[m.at("context").get<size_t>()]["count"].get<uint64_t>()<=m.at("count_threshold").get<uint64_t>();
        else if(m.contains("minimum_set_equality"))value=c[m["minimum_set_equality"][0].get<size_t>()]["set"]==c[m["minimum_set_equality"][1].get<size_t>()]["set"];
        else if(m.contains("strict_count_comparison"))value=c[m["strict_count_comparison"][0].get<size_t>()]["count"].get<uint64_t>()<c[m["strict_count_comparison"][1].get<size_t>()]["count"].get<uint64_t>();
        else throw std::invalid_argument("Unknown acquired target meaning: "+i.key());
        actual[i.key()]=value;
    }
    return actual;
}
std::string ConstructionKnowledge::bits(const std::string& key) const {
    for(size_t i=0;i<dictionary_.size();++i)if(dictionary_[i]["sha256"]==key) {
        std::ifstream in(directory_/"MINIMUM_SETS.bin",std::ios::binary);in.seekg(std::streamoff(i*32768));std::string value(32768,'\0');in.read(value.data(),value.size());check(in.gcount()==32768&&hash(value)==key,"Acquired minimum set differs");return value;
    }
    throw std::invalid_argument("Unknown acquired minimum set");
}
}
