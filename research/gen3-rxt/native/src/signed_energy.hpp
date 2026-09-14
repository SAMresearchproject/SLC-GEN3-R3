#pragma once
#include "engine.hpp"
namespace rxt {
// Same exact identity for RH scalar signed counts and SB receiver vectors.
// Supports are explicit: an SB phase is never relabelled as RH squarefree mass.
inline json signed_energy(const json& x,const json& y,const mpq_class& a,const mpq_class& b) {
    if(!x.is_array() || x.size()!=y.size() || x.empty() || a<0 || b<0)
        throw std::invalid_argument("Signed energy needs matched vectors and nonnegative supports");
    mpq_class xx=0,yy=0,xy=0,dd=0,rr=0;
    for(size_t k=0;k<x.size();++k) {
        mpq_class u=rational(x[k]),v=rational(y[k]),d=u-v,z=b*u+a*v;
        xx+=u*u; yy+=v*v; xy+=u*v; dd+=d*d; rr+=z*z;
    }
    if((a==0 && xx!=0)||(b==0 && yy!=0))throw std::invalid_argument("Zero support carries nonzero source");
    mpq_class le=a>0?mpq_class(xx/a):mpq_class(0),re=b>0?mpq_class(yy/b):mpq_class(0);
    mpq_class parent=a+b>0?mpq_class(dd/(a+b)):mpq_class(0);
    mpq_class repay=a>0&&b>0?mpq_class(rr/(a*b*(a+b))):mpq_class(0),gain=parent-le;
    if(le+re-parent!=repay || repay<0 || gain!=re-repay)throw std::runtime_error("Signed repayment identity differs");
    return {{"left",x},{"right",y},{"left_support",number(a)},{"right_support",number(b)},
        {"left_energy",number(le)},{"right_energy",number(re)},{"parent_energy",number(parent)},
        {"repayment",number(repay)},{"gain",number(gain)},{"positive_gain",gain>0},
        {"features",{int(xy>0)-int(xy<0),int(a<=b),int(xx<=yy)}},
        {"feature_names",{"signed_inner_product_sign","left_support_le_right","left_norm_le_right"}},
        {"identity_exact",true}};
}
}
