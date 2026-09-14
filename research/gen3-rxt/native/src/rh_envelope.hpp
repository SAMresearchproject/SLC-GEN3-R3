#pragma once
#include <gmpxx.h>
#include <algorithm>
#include <stdexcept>
namespace rh_envelope {
using Q=mpq_class;
inline Q square(const Q& x){return x*x;}
inline Q root_upper(const Q& x){
    if(x<0)throw std::invalid_argument("Nonnegative root input required");
    mpz_class scale=mpz_class(1)<<40,n=x.get_num()*scale*scale,d=x.get_den(),quotient=n/d,r;
    mpz_sqrt(r.get_mpz_t(),quotient.get_mpz_t());if(r*r*d<n)++r;
    Q out(r,scale);out.canonicalize();return out;
}
inline Q harmonic(unsigned s){Q h=0;for(unsigned k=1;k<s;++k)h+=Q(1,k);return h;}
inline Q geometric_factor(unsigned s,const Q& b){
    if(s<2||b<=0)throw std::invalid_argument("Original positive scale/baseline required");
    Q h=harmonic(s),a=h/s+Q(1,static_cast<unsigned long>(s)*s),radius=2*Q(s)-1;
    return 1+Q(4,3)*(a+2*root_upper(radius*a))/b;
}
struct Terms {
    Q negative=0,diagonal=0,cubic=0;
    void add(const Q& b,const Q& old,const Q& next,const Q& delta,const Q& F){
        if(b<=0||old<0||next<0||delta<0||next-old!=delta+F)throw std::invalid_argument("Original signed energy recurrence differs");
        const Q jump=next-old,magnitude=jump<0?-jump:jump;
        if(F<0)negative-=F*old/(b+old);
        diagonal+=delta*old/(b+old);
        cubic+=magnitude*magnitude*magnitude/((jump<0?3:6)*(b+old)*(b+next));
    }
    Q variation() const{return diagonal+cubic;}
};
}
