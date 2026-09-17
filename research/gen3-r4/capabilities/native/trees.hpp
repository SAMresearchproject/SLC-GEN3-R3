#pragma once
#include "engine.hpp"
namespace rxt {
struct Example { std::vector<int> x; bool y; int split; json witness; };
mpq_class impurity(int64_t n,int64_t p){return n?mpq_class(mpz_class(2)*p*(n-p),mpz_class(n)):mpq_class(0);}
json tree(const std::vector<Example>& data,const std::vector<int>& ids,int depth,int positive_weight,int negative_weight) {
    int pos=0;for(int i:ids)pos+=data[i].y;
    json node={{"n",ids.size()},{"positive",pos},{"probability",number(mpq_class(pos,ids.size()))}};
    node["witness"]=data[ids.front()].witness;
    if(!depth || pos==0 || pos==int(ids.size()))return node;
    auto cost_of=[&](int n,int p){return impurity(int64_t(p)*positive_weight+int64_t(n-p)*negative_weight,int64_t(p)*positive_weight);};
    mpq_class best=cost_of(ids.size(),pos);int feature=-1,threshold=0;
    for(size_t f=0;f<data[ids[0]].x.size();++f){
        std::map<int,std::pair<int,int>> counts;for(int i:ids){auto& c=counts[data[i].x[f]];c.first++;c.second+=data[i].y;}
        int n=0,p=0;for(const auto& [t,c]:counts){n+=c.first;p+=c.second;if(n==int(ids.size()))break;
            mpq_class cost=cost_of(n,p)+cost_of(ids.size()-n,pos-p);
            if(cost<best){best=cost;feature=int(f);threshold=t;}
        }
    }
    if(feature<0)return node;
    std::vector<int> a,b;for(int i:ids)(data[i].x[feature]<=threshold?a:b).push_back(i);
    node["feature"]=feature;node["threshold"]=threshold;node["left"]=tree(data,a,depth-1,positive_weight,negative_weight);node["right"]=tree(data,b,depth-1,positive_weight,negative_weight);return node;
}
mpq_class predict(const json& t,const std::vector<int>& x){const json* p=&t;while(p->contains("feature"))p=&p->at(x[p->at("feature").get<int>()]<=p->at("threshold").get<int>()?"left":"right");return rational(p->at("probability"));}
json metric(const json& t,const std::vector<Example>& d,int split){int n=0,yes=0,tp=0,tn=0;json examples=json::array();
    for(const auto& r:d)if(r.split==split){bool p=predict(t,r.x)>=rational(t.value("classification_threshold",json("1/2")));++n;yes+=r.y;tp+=p&&r.y;tn+=!p&&!r.y;if(p!=r.y && examples.size()<8)examples.push_back(r.witness);}
    mpq_class score=yes&&n>yes?(mpq_class(tp,yes)+mpq_class(tn,n-yes))/2:n?mpq_class(tp+tn,n):mpq_class(0);
    return {{"rows",n},{"positives",yes},{"correct",tp+tn},{"balanced_accuracy",number(score)},{"exception_witnesses",examples}};
}
json fit(const std::vector<Example>& d){std::vector<int> ids;for(size_t i=0;i<d.size();++i)if(d[i].split==0)ids.push_back(i);need(!ids.empty(),"No training source rows");
    int positives=0;for(int i:ids)positives+=d[i].y;int negatives=int(ids.size())-positives;
    bool both=positives>0&&negatives>0;
    json selected;mpq_class best=-1;int depth=0;
    for(int k=0;k<=3;++k){auto t=tree(d,ids,k,both?negatives:1,both?positives:1);t["classification_threshold"]=both?number(mpq_class(positives,ids.size())):json("1/2");auto dev=metric(t,d,1);mpq_class score=rational(dev["balanced_accuracy"]);if(score>best){best=score;selected=t;depth=k;}}
    return {{"tree",selected},{"depth",depth},{"training",metric(selected,d,0)},{"development",metric(selected,d,1)},
        {"test_rows_reserved",std::count_if(d.begin(),d.end(),[](const auto& r){return r.split==2;})},
        {"fit","NATIVE_CPP_EXACT_GMP_CLASS_BALANCED_CART"},{"class_weights",{{"positive",both?negatives:1},{"negative",both?positives:1}}},{"selection","development balanced accuracy; shallower on tie"}};
}
void rules(const json& t,json path,json& out){if(!t.contains("feature")){auto row=t;row["conditions"]=path;row["all_probability_ties_retained"]=true;out.push_back(row);return;}
    for(auto side:{"left","right"}){auto p=path;p.push_back({{"feature",t["feature"]},{"comparison",std::string(side)=="left"?"<=":">"},{"threshold",t["threshold"]}});rules(t[side],p,out);}}

}
