#include "training.hpp"
#include "training_binding.hpp"
#include "knowledge.hpp"
#include "starbreaker.hpp"
#include <algorithm>
#include <chrono>
#include <fstream>
#include <functional>
#include <set>
#include <omp.h>

namespace rxt {
namespace {
void need(bool ok,const std::string& s){if(!ok)throw std::invalid_argument("Native training: "+s);}
void fields(const json& p,const std::set<std::string>& names){for(auto i=p.begin();i!=p.end();++i)need(names.count(i.key()),"Unknown field: "+i.key());}
mpq_class ratio(uint64_t a,uint64_t b){need(b>0,"Empty ratio denominator");mpq_class q{mpz_class(a),mpz_class(b)};q.canonicalize();return q;}
mpq_class purity(uint64_t p,uint64_t n){return ratio(p*p+(n-p)*(n-p),n);}
json metric(uint64_t a,uint64_t b){return b?json(ratio(a,b).get_str()):json(nullptr);}
bool better(const json& a,const json& b){
    auto x=rational(a.at("balanced_accuracy")),y=rational(b.at("balanced_accuracy"));
    if(x!=y)return x>y;
    if(a.at("leaves")!=b.at("leaves"))return a.at("leaves")<b.at("leaves");
    return a.at("depth")<b.at("depth");
}
struct Leaf {std::string path;bool positive;mpq_class probability;};
json evaluate(const json& tree,const std::vector<int>& columns,const TrainingData& data,int target,int depth){
    uint64_t tp=0,tn=0,fp=0,fn=0,leaves=0;std::map<std::string,std::pair<uint64_t,uint64_t>> groups;std::map<std::string,mpq_class> probabilities;
    std::function<void(const json&)> count=[&](const json& node){if(node.at("split").is_null()||node.at("depth")>=depth){++leaves;return;}count(node.at("left"));count(node.at("right"));};count(tree);
    for(size_t i=0;i<data.x.size();++i)if(data.split[i]==1){
        const json* node=&tree;
        while(!node->at("split").is_null()&&node->at("depth")<depth){const auto& s=node->at("split");int f=columns.at(s.at("feature").get<size_t>());node=&node->at(data.x[i][f]<=s.at("threshold").get<int>()?"left":"right");}
        auto p=rational(node->at("probability"));bool prediction=p>=mpq_class(1,2),actual=data.y[i][target];
        if(actual){if(prediction)++tp;else ++fn;}else{if(prediction)++fp;else ++tn;}
        auto path=node->at("path").get<std::string>();auto& group=groups[path];++group.first;group.second+=actual;probabilities[path]=p;
    }
    auto n=tp+tn+fp+fn;need(n>0,"Development set is empty");mpq_class balanced=0;
    if(tp+fn&&tn+fp)balanced=(ratio(tp,tp+fn)+ratio(tn,tn+fp))/2;else balanced=tp+fn?ratio(tp,tp+fn):ratio(tn,tn+fp);
    mpq_class max=-1;for(const auto& i:probabilities)if(i.second>max)max=i.second;uint64_t top_n=0,top_p=0;
    for(const auto& i:probabilities)if(i.second==max){top_n+=groups[i.first].first;top_p+=groups[i.first].second;}
    return {{"families",n},{"depth",depth},{"leaves",leaves},{"tp",tp},{"tn",tn},{"fp",fp},{"fn",fn},
        {"accuracy",metric(tp+tn,n)},{"precision",metric(tp,tp+fp)},{"recall",metric(tp,tp+fn)},{"specificity",metric(tn,tn+fp)},
        {"prevalence",metric(tp+fn,n)},{"balanced_accuracy",balanced.get_str()},{"single_class",!(tp+fn&&tn+fp)},
        {"top_group_families",top_n},{"top_group_precision",metric(top_p,top_n)}};
}
}
TrainingData::TrainingData(const std::filesystem::path& dir,const SBPolicyIR& policy,const Resources& resources){
    need(file_sha256(dir/"BUNDLE.json")==TRAINING_BUNDLE_SHA,"Training source bundle differs");bundle=read_json(dir/"BUNDLE.json");
    need(bundle.at("schema")=="GEN3_RXT_ACQUIRED_TRAINING_V1"&&bundle.at("rows")==541568&&bundle.at("record_bytes")==50,"Training encoding differs");
    for(auto i=bundle.at("files").begin();i!=bundle["files"].end();++i){need(i.key().find('/')==std::string::npos&&i.key().find("..") == std::string::npos,"Invalid source filename");need(file_sha256(dir/i.key())==i.value().get<std::string>(),"Training file differs: "+i.key());}
    resources.admit(256ull*1024*1024);plan=read_json(dir/"PLAN.json");auto metadata=read_json(dir/"DATASET.json");
    pattern_split.fill(255);int code=0;for(const auto* name:{"train","development","test"}){for(const auto& raw:metadata.at("split_patterns").at(name)){int p=raw.get<int>();need(p>=0&&p<625&&pattern_split[p]==255,"Repeated pattern split");pattern_split[p]=uint8_t(code);}++code;}
    for(auto v:pattern_split)need(v<3,"Missing source pattern partition");
    size_t n=bundle.at("rows");need(std::filesystem::file_size(dir/"ROWS.bin")==n*50,"Training extent differs");
    x.resize(n);y.resize(n);ids.resize(n);split.resize(n);index.assign(4800000,-1);
    std::ifstream in(dir/"ROWS.bin",std::ios::binary);unsigned char row[50];
    for(size_t i=0;i<n;++i){in.read(reinterpret_cast<char*>(row),50);need(in.gcount()==50,"Incomplete training row");uint32_t id=uint32_t(row[0])|(uint32_t(row[1])<<8)|(uint32_t(row[2])<<16)|(uint32_t(row[3])<<24);
        need(id<4800000&&index[id]<0,"Training family outside source or repeated");ids[i]=id;index[id]=int32_t(i);split[i]=row[49];need(split[i]==pattern_split[id/7680],"Whole-pattern partition differs");
        int64_t f[32];sb_features(policy,id,f);for(int k=0;k<32;++k){need(f[k]>=0&&f[k]<=4096,"Feature exceeds exact histogram encoding");x[i][k]=int16_t(f[k]);maximum[k]=std::max(maximum[k],int(f[k]));}
        for(int k=0;k<45;++k){need(row[4+k]<=1,"Label is not binary");y[i][k]=row[4+k];}
    }
    binding={{"directory",std::filesystem::absolute(dir).string()},{"bundle_sha256",TRAINING_BUNDLE_SHA},{"source_dataset_sha256",bundle.at("source_dataset_sha256")}};seal();
}
void TrainingData::append(const json& row,const SBPolicyIR& policy){
    auto id=row.at("family_id").get<uint32_t>();need(id<4800000,"New family outside source");std::array<uint8_t,45> labels{};
    for(int k=0;k<45;++k)labels[k]=row.at("observed_targets").at(bundle.at("labels")[k].get<std::string>()).get<bool>();
    if(index[id]>=0){need(y[index[id]]==labels,"New exact observation conflicts with acquired label");return;}
    index[id]=int32_t(ids.size());ids.push_back(id);y.push_back(labels);split.push_back(pattern_split[id/7680]);
    std::array<int16_t,32> values{};int64_t f[32];sb_features(policy,id,f);for(int k=0;k<32;++k){need(f[k]>=0&&f[k]<=4096,"New feature outside histogram encoding");values[k]=int16_t(f[k]);maximum[k]=std::max(maximum[k],int(f[k]));}x.push_back(values);
}
void TrainingData::seal(){std::string data=TRAINING_BUNDLE_SHA;std::vector<uint32_t> extra(ids.begin()+541568,ids.end());std::sort(extra.begin(),extra.end());for(auto id:extra){data+=std::to_string(id)+":";for(auto v:y[index[id]])data.push_back(char('0'+v));}signature=hash(data);}
json TrainingData::status() const {std::array<uint64_t,3> counts{};for(auto v:split)++counts[v];return {{"source",binding},{"dataset_signature",signature},{"families",ids.size()},{"new_simulated_families",ids.size()-541568},{"train_rows",counts[0]},{"development_rows",counts[1]},{"test_rows_reserved",counts[2]},{"feature_count",32},{"target_count",45},{"fit_backend","NATIVE_CPP_OPENMP_EXACT_GMP"}};}

json Engine::train(const std::string& op,const json& p){
    need(bool(store_)&&bool(starbreaker_)&&bool(construction_memory_),"Load the shared construction engine first");
    auto ensure=[&](){
        need(state_.contains("training_source"),"Compile the acquired training dataset first");
        if(!training_){auto data=std::make_unique<TrainingData>(state_["training_source"]["directory"].get<std::string>(),starbreaker_->policy_ir(),resources_);
            need(data->binding==state_["training_source"],"Saved training binding differs");
            for(const auto& ref:state_.value("training_ingested_jobs",json::object())){auto chunk=store_->get(ref.get<std::string>());for(const auto& row:chunk.at("rows"))data->append(row,starbreaker_->policy_ir());}
            data->seal();training_=std::move(data);}
    };
    auto commit=[&](json next,json result){next["sequence"]=state_["sequence"].get<uint64_t>()+1;
        next["training_log_head"]=store_->put({{"previous",state_.value("training_log_head",json(nullptr))},{"op",op},{"payload",p},{"result",result}});
        auto root=store_->commit(next);state_=std::move(next);result["checkpoint"]={{"root",root},{"sequence",state_["sequence"]}};return result;};
    if(op=="TRAIN_COMPILE"){
        fields(p,{"directory"});auto data=std::make_unique<TrainingData>(p.at("directory").get<std::string>(),starbreaker_->policy_ir(),resources_);
        need(data->bundle.at("policy_sha256")==starbreaker_->binding().at("policy_sha256"),"Training and policy sources differ");
        if(state_.contains("training_source")){need(state_["training_source"]["bundle_sha256"]==data->binding["bundle_sha256"],"Another acquired dataset is already attached");ensure();return training_->status();}
        auto next=state_;next["training_source"]=data->binding;next["training_ingested_jobs"]=json::object();next["training_lessons"]=json::object();next["trained_models"]=json::object();next["training_state"]="READY_FOR_NATIVE_TRAINING";
        auto result=commit(std::move(next),data->status());training_=std::move(data);return result;
    }
    ensure();
    if(op=="TRAIN_STATUS"){
        fields(p,{});auto result=training_->status();result["completed_native_lessons"]=state_.value("training_lessons",json::object()).size();result["promoted_targets"]=state_.value("trained_models",json::object()).size();result["progress"]=state_.value("training_progress",json(nullptr));return result;
    }
    if(op=="TRAIN_MODEL"){
        fields(p,{"target","object"});if(p.contains("object"))return store_->get(p.at("object").get<std::string>());return starbreaker_->policy().at("models").at(p.at("target").get<std::string>());
    }
    if(op=="TRAIN_RULES"){
        fields(p,{"target","max_leaves"});const auto name=p.at("target").get<std::string>();
        const auto& learned=starbreaker_->policy().at("models").at(name);const auto& model=learned.at("model");
        const auto columns=model.at("columns").get<std::vector<int>>();int depth=model.at("selected_depth");
        int target=-1;for(int k=0;k<45;++k)if(training_->bundle["labels"][k]==name)target=k;need(target>=0,"Rule target outside native labels");
        json rules=json::array(),split_ties=json::object();std::map<std::string,size_t> paths;
        std::function<void(const json&,json)> walk=[&](const json& node,json conditions){
            auto path=node.at("path").get<std::string>();
            if(node.at("split").is_null()||node.at("depth")>=depth){
                auto probability=rational(node.at("probability"));paths[path]=rules.size();
                rules.push_back({{"path",path},{"conditions",conditions},{"probability",node["probability"]},{"prediction",probability>=mpq_class(1,2)},
                    {"prediction_ties",probability==mpq_class(1,2)?json::array({false,true}):json::array({probability>=mpq_class(1,2)})},
                    {"train",{{"families",0},{"positive",0},{"exceptions",0}}},{"development",{{"families",0},{"positive",0},{"exceptions",0}}},
                    {"witness_ids",json::object()}});return;
            }
            const auto& split=node.at("split");int f=columns.at(split["feature"].get<size_t>());
            split_ties[path]=node.value("best_ties",json::array());
            for(const auto* branch:{"left","right"}){auto next=conditions;next.push_back({{"feature",starbreaker_->policy()["names"][f]},{"feature_index",f},{"relation",std::string(branch)=="left"?"<=":">"},{"threshold",split["threshold"]}});walk(node.at(branch),next);}
        };walk(model.at("tree"),json::array());
        unsigned limit=p.value("max_leaves",32u);need(limit>0&&limit<=1024,"Rule rendering limit outside 1..1024");
        if(rules.size()>limit)return {{"status","EXCEEDS_RENDERING_LIMIT"},{"target",name},{"leaves",rules.size()},{"max_leaves",limit},{"model_sha256",learned["sha256"]}};
        for(size_t i=0;i<training_->ids.size();++i)if(training_->split[i]<2){
            const json* node=&model.at("tree");while(!node->at("split").is_null()&&node->at("depth")<depth){auto& split=node->at("split");int f=columns.at(split["feature"].get<size_t>());node=&node->at(training_->x[i][f]<=split["threshold"].get<int>()?"left":"right");}
            auto& rule=rules.at(paths.at(node->at("path").get<std::string>()));bool actual=training_->y[i][target],exception=actual!=rule["prediction"].get<bool>();
            auto& counts=rule[training_->split[i]==0?"train":"development"];counts["families"]=counts["families"].get<uint64_t>()+1;counts["positive"]=counts["positive"].get<uint64_t>()+actual;counts["exceptions"]=counts["exceptions"].get<uint64_t>()+exception;
            auto kind=exception?"exception":"support";if(!rule["witness_ids"].contains(kind))rule["witness_ids"][kind]=training_->ids[i];
        }
        json witnesses=json::object(),sets=json::object();
        for(auto& rule:rules)for(auto it=rule["witness_ids"].begin();it!=rule["witness_ids"].end();++it){
            auto id=it.value().get<uint32_t>();auto key=std::to_string(id);if(witnesses.contains(key))continue;
            auto exact=joint("ATOM3D_CONSTRUCTION_RESULT",{{"family_id",id}});need(exact["status"]=="EXACT_OUTCOME","Rule witness has no native minimum custody");
            need(exact["observed_targets"][name].get<bool>()==bool(training_->y[training_->index[id]][target]),"Rule witness and acquired target disagree");
            json values=json::object();for(int k=0;k<32;++k)values[starbreaker_->policy()["names"][k].get<std::string>()]=training_->x[training_->index[id]][k];exact["features"]=values;
            for(const auto& context:exact["outcome"]["contexts"]){auto digest=context["set"].get<std::string>();if(!sets.contains(digest))sets[digest]=joint("ATOM3D_CONSTRUCTION_MINIMUM_SET",{{"sha256",digest}});}
            witnesses[key]=exact;
        }
        json result={{"schema","GEN3_NATIVE_CONSTRUCTION_RULES_V1"},{"status","EXTRACTED"},{"target",name},{"target_definition",learned["target_definition"]},
            {"model_sha256",learned["sha256"]},{"dataset",training_->status()},{"selected_depth",depth},{"leaves",rules.size()},{"rules",rules},{"split_ties",split_ties},
            {"witnesses",witnesses},{"complete_minimum_sets",sets},{"source",construction_memory_->binding()},{"feature_names",starbreaker_->policy()["names"]},
            {"rule_meaning","Conditions of the acquired selected tree, with exact observed support and exceptions traced to complete native minimum sets"},{"heldout_test_used",false},{"backend","NATIVE_CPP_EXACT_GMP"}};
        auto next=state_;next["construction_rules"][name]=store_->put(result);return commit(std::move(next),result);
    }
    if(op=="TRAIN_INGEST"){
        fields(p,{"job_id"});auto name=p.at("job_id").get<std::string>();
        if(state_["training_ingested_jobs"].contains(name))return {{"status","ALREADY_INGESTED"},{"job_id",name}};
        auto job=store_->get(state_.at("joint_jobs").at(name).get<std::string>());need(job["cursor"]==job["family_count"],"Finish the simulation job before training on it");json rows=json::array();
        for(const auto& ref:job["batches"]){auto batch=store_->get(ref.get<std::string>());need(batch["source_binding"]["bundle_sha256"]==state_["joint_binding"]["bundle_sha256"],"Simulation feedback belongs to another source");for(const auto& row:batch["rows"])rows.push_back(row);}
        resources_.admit(rows.size()*512+256ull*1024*1024);
        for(const auto& row:rows){auto id=row.at("family_id").get<uint32_t>();need(id<4800000,"Feedback family outside source");for(int k=0;k<45;++k){auto label=row.at("observed_targets").at(training_->bundle["labels"][k].get<std::string>()).get<bool>();if(training_->index[id]>=0)need(training_->y[training_->index[id]][k]==label,"New exact observation conflicts with an acquired label");}}
        auto next=state_;next["training_ingested_jobs"][name]=store_->put({{"job_id",name},{"rows",rows},{"source",state_["joint_binding"]}});
        auto result=commit(std::move(next),{{"status","ACQUIRED_SIMULATION_FEEDBACK"},{"job_id",name},{"families",rows.size()}});
        try{for(const auto& row:rows)training_->append(row,starbreaker_->policy_ir());training_->seal();}catch(...){training_.reset();throw;}result["dataset"]=training_->status();return result;
    }
    need(op=="TRAIN_FIT","Unknown training operation");fields(p,{"index"});need(p.at("index").is_number_integer()&&!p.at("index").is_boolean(),"Curriculum index must be an integer");
    int index=p.at("index").get<int>();need(index>=0&&size_t(index)<training_->plan.at("jobs").size(),"Curriculum index outside installed plan");
    json config=training_->plan.at("jobs").at(index);auto signature=hash(json({{"dataset",training_->signature},{"config",config},{"learner","NATIVE_EXACT_CART_V1"}}).dump());
    if(state_["training_lessons"].contains(signature)){auto report=store_->get(state_["training_lessons"][signature].get<std::string>());report["idempotent_replay"]=true;return report;}
    int target=config.at("target"),max_depth=config.at("depth"),minimum=config.at("minimum_leaf_families");auto columns=config.at("columns").get<std::vector<int>>();
    auto target_name=training_->bundle.at("labels").at(target).get<std::string>();auto start=std::chrono::steady_clock::now();uint64_t computed=0,reused=0;
    std::function<json(const std::vector<uint32_t>&,const std::string&,int)> fit;
    fit=[&](const std::vector<uint32_t>& rows,const std::string& path,int depth)->json{
        auto memory_key="TRAIN_NODE:"+signature+":"+path;json node=store_->recall(memory_key);
        if(node.is_null()){
            uint64_t n=rows.size(),positive=0;need(n>0,"Empty training branch");for(auto i:rows)positive+=training_->y[i][target];
            json ties=json::array();mpq_class best=0;auto base=purity(positive,n);
            if(depth<max_depth&&positive>0&&positive<n&&n>=uint64_t(2*minimum)){
                struct Candidate{int feature,threshold;mpq_class gain;};std::vector<std::vector<Candidate>> candidates(columns.size());
                #pragma omp parallel for num_threads(resources_.cpu_threads) schedule(static) if(rows.size()>4096)
                for(size_t local=0;local<columns.size();++local){
                    int f=columns[local];std::vector<uint64_t> counts(training_->maximum[f]+1),positives(counts.size());
                    for(auto i:rows){auto v=training_->x[i][f];++counts[v];positives[v]+=training_->y[i][target];}
                    std::vector<int> thresholds;for(size_t v=0;v<counts.size();++v)if(counts[v])thresholds.push_back(int(v));if(!thresholds.empty())thresholds.pop_back();
                    if(thresholds.size()>24){std::vector<int> chosen;for(size_t k=0;k<24;++k)chosen.push_back(thresholds[k*(thresholds.size()-1)/23]);thresholds=std::move(chosen);}
                    for(size_t v=1;v<counts.size();++v){counts[v]+=counts[v-1];positives[v]+=positives[v-1];}
                    for(int t:thresholds){auto left=counts[t],lp=positives[t];if(left<uint64_t(minimum)||n-left<uint64_t(minimum))continue;candidates[local].push_back({int(local),t,purity(lp,left)+purity(positive-lp,n-left)-base});}
                }
                for(const auto& feature:candidates)for(const auto& c:feature)if(c.gain>0){if(c.gain>best){best=c.gain;ties=json::array();}if(c.gain==best)ties.push_back({{"feature",c.feature},{"threshold",c.threshold},{"gain",best.get_str()}});}
            }
            node={{"binding",signature},{"path",path},{"depth",depth},{"training_families",n},{"positive_families",positive},{"probability",ratio(positive,n).get_str()},{"gain",best.get_str()},{"best_ties",ties},{"split",ties.empty()?json(nullptr):ties[0]}};
            auto ref=store_->remember(memory_key,node);++computed;auto next=state_;next["training_state"]="TRAINING";next["training_progress"]={{"index",index},{"dataset_signature",training_->signature},{"node",path},{"node_object",ref},{"status","NODE_CHECKPOINTED"}};store_->commit(next);state_=std::move(next);
        }else{need(node.at("binding")==signature&&node.at("training_families")==rows.size(),"Training node binding differs");++reused;}
        if(!node.at("split").is_null()){
            int f=columns.at(node["split"]["feature"].get<size_t>()),threshold=node["split"]["threshold"];std::vector<uint32_t> left,right;left.reserve(rows.size());right.reserve(rows.size());for(auto i:rows)(training_->x[i][f]<=threshold?left:right).push_back(i);
            node["left"]=fit(left,path+"L",depth+1);node["right"]=fit(right,path+"R",depth+1);
        }return node;
    };
    std::vector<uint32_t> rows;for(size_t i=0;i<training_->ids.size();++i)if(training_->split[i]==0)rows.push_back(uint32_t(i));auto tree=fit(rows,"root",0);
    json scores=json::array(),chosen;std::set<int> depths={3,5,7,max_depth};for(int depth:depths)if(depth<=max_depth){auto score=evaluate(tree,columns,*training_,target,depth);scores.push_back(score);if(chosen.is_null()||better(score,chosen))chosen=score;}
    auto incumbent=starbreaker_->policy()["models"][target_name];const auto& old=incumbent.at("model");auto old_score=evaluate(old.at("tree"),old.at("columns").get<std::vector<int>>(),*training_,target,old.at("selected_depth"));
    bool promote=rational(chosen["balanced_accuracy"])>rational(old_score["balanced_accuracy"])||(rational(chosen["balanced_accuracy"])==rational(old_score["balanced_accuracy"])&&(chosen["leaves"]<old_score["leaves"]||(chosen["leaves"]==old_score["leaves"]&&index<=old.at("config").at("index").get<int>())));
    json model={{"schema","GEN3_AUTONOMOUS_CONSTRUCTION_MODEL_V1"},{"binding",signature},{"columns",columns},{"config",config},{"selected_depth",chosen["depth"]},{"tree",tree},{"scores",scores}};
    json learned={{"model",model},{"development",chosen},{"target_definition",incumbent.at("target_definition")},{"sha256",hash(model.dump())},
        {"source","GEN3-RXT-R3:NATIVE_EXACT_CART_V1"},{"qualification","DEVELOPMENT_SELECTED"},{"baseline_policy_sha256",starbreaker_->binding()["policy_sha256"]},{"dataset_signature",training_->signature}};
    auto model_ref=store_->put(learned);json report={{"status","TRAINED"},{"index",index},{"target",target_name},{"dataset",training_->status()},{"model_object",model_ref},{"model_sha256",learned["sha256"]},{"development",chosen},{"incumbent_development",old_score},{"promoted",promote},{"new_nodes",computed},{"reused_nodes",reused},{"wall_seconds",std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()},{"backend","NATIVE_CPP_OPENMP_EXACT_GMP"},{"test_used_for_selection",false}};
    auto next=state_;next["training_lessons"][signature]=store_->put(report);if(promote)next["trained_models"][target_name]=model_ref;
    next["training_state"]="READY_FOR_NATIVE_TRAINING";next["training_progress"]={{"index",index},{"status","COMPLETE"},{"model_object",model_ref},{"promoted",promote}};
    // Validate the complete new policy before installing its durable head.
    if(promote)starbreaker_->adopt(target_name,learned);
    try{return commit(std::move(next),report);}catch(...){if(promote){auto rollback=incumbent;rollback["baseline_policy_sha256"]=starbreaker_->binding()["policy_sha256"];starbreaker_->adopt(target_name,rollback);}throw;}
}
}
