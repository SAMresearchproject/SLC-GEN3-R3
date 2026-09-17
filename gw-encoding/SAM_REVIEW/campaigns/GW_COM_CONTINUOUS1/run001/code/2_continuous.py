"""Continuous Newtonian reference, explicit control and two signed quadrupole channels.

G=4, m1=m2=1, individual reference radius=1, reference angular speed=1.
Native arithmetic evaluates reference mechanics and wave projections. Trig
samples are declared rounded input constants; independent RK4 checks dynamics.
"""
from fractions import Fraction as F
import math
from .native import Graph


def event_times(message):
    events=[];start=F(32)
    for _ in range(2):
        packet=[start+4*i for i in range(4)]
        for n in message:packet.append(packet[-1]+4*n)
        events+=packet;start=packet[-1]+92
    return events


def profile(native):
    g=Graph();out={}
    def v(n):return g.value(n,'continuous reference coefficient')
    def op(o,a,b):return g.op(o,a,b)
    one,two,four,eight,seven,sixteen=map(v,[1,2,4,8,7,16])
    for offset in range(-8,9):
        u=v(F(offset,8));u2=op('MULTIPLY',u,u)
        b=op('SUBTRACT',one,u2);b2=op('MULTIPLY',b,b);b3=op('MULTIPLY',b2,b);b4=op('MULTIPLY',b2,b2)
        r=op('ADD',one,op('DIVIDE',b4,sixteen))
        velocity=op('DIVIDE',op('MULTIPLY',v(-8),op('MULTIPLY',u,b3)),sixteen)
        acceleration=op('DIVIDE',op('MULTIPLY',eight,op('MULTIPLY',b2,op('SUBTRACT',op('MULTIPLY',seven,u2),one))),sixteen)
        r2=op('MULTIPLY',r,r);v2=op('MULTIPLY',velocity,velocity)
        invr2=op('DIVIDE',one,r2)
        fr=op('ADD',op('SUBTRACT',acceleration,r),invr2)
        ft=op('MULTIPLY',two,velocity)
        energy=op('SUBTRACT',op('ADD',v2,r2),op('DIVIDE',two,r))
        power=op('MULTIPLY',two,op('ADD',op('MULTIPLY',fr,velocity),op('MULTIPLY',ft,r)))
        energy_derivative=op('MULTIPLY',op('MULTIPLY',two,velocity),op('ADD',op('ADD',acceleration,r),invr2))
        force2=op('ADD',op('MULTIPLY',fr,fr),op('MULTIPLY',ft,ft))
        a=op('SUBTRACT',op('ADD',v2,op('MULTIPLY',r,acceleration)),op('MULTIPLY',two,r2))
        b_wave=op('MULTIPLY',four,op('MULTIPLY',r,velocity))
        out[offset]=[r,velocity,acceleration,fr,ft,energy,power,energy_derivative,force2,a,b_wave]
    values,receipt=native.evaluate(g,'GW-COM continuous reference: C3 radial bump, Newtonian feedforward radial/tangential force, pair mechanical energy, signed power and quadrupole derivative coefficients')
    keys=('radius','radial_velocity','radial_acceleration','force_radial','force_tangential','energy','power','energy_derivative','force_squared','wave_a','wave_b')
    rows={k:{name:values[node] for name,node in zip(keys,nodes)} for k,nodes in out.items()}
    for row in rows.values():
        r,rv,ra=(row[k] for k in ('radius','radial_velocity','radial_acceleration'))
        assert row['force_radial']==ra-r+1/r**2
        assert row['force_tangential']==2*rv
        assert row['energy']==rv**2+r**2-2/r
        assert row['power']==row['energy_derivative']
    return rows,receipt


def synthesize(native,rows,events,active=True):
    length=int((events[-1]+4)*8)+1
    lookup={int(center*8)+offset:offset for center in events for offset in range(-8,9)} if active else {}
    output=[];trigs=[];profile_indices=[];receipts=[]
    for start in range(0,length,512):
        graph=Graph();four=graph.value(4,'quadrupole derivative coefficient');nodes=[]
        for i in range(start,min(start+512,length)):
            offset=lookup.get(i,-8);p=rows[offset]
            t=F(i,8)
            c=F(format(math.cos(2*float(t)),'.14f'));s=F(format(math.sin(2*float(t)),'.14f'))
            trigs.append((c,s));profile_indices.append(offset)
            a=graph.value(p['wave_a'],{'native_profile_offset':offset,'quantity':'wave_a'})
            b=graph.value(p['wave_b'],{'native_profile_offset':offset,'quantity':'wave_b'})
            cn=graph.value(c,{'time':str(t),'input':'cos(2t) rounded to 14 decimal places'})
            sn=graph.value(s,{'time':str(t),'input':'sin(2t) rounded to 14 decimal places'})
            hp=graph.op('MULTIPLY',four,graph.op('SUBTRACT',graph.op('MULTIPLY',a,cn),graph.op('MULTIPLY',b,sn)))
            hx=graph.op('MULTIPLY',four,graph.op('ADD',graph.op('MULTIPLY',a,sn),graph.op('MULTIPLY',b,cn)))
            nodes.append((hp,hx))
        values,receipt=native.evaluate(graph,'GW-COM continuous signed quadrupole pair: analytic second derivatives from native radius/velocity/acceleration with declared trigonometric inputs')
        receipts.append(receipt);output.extend((values[a],values[b]) for a,b in nodes)
    return output,trigs,profile_indices,receipts


def fit_basis(c,s,channel,size):
    return ([c,-s,F(1),F(0)] if channel==0 else [s,c,F(0),F(1)])[:size]


def fit_and_residual(native,wave,trigs,size):
    graph=Graph();xs=[];ys=[]
    for i in range(128):
        for channel in (0,1):
            xs.append(fit_basis(*trigs[i],channel,size))
            ys.append(graph.value(wave[i][channel],{'calibration_sample':i,'channel':channel}))
    matrix=[[graph.value(sum(x[a]*x[b] for x in xs),{'design_gram':[a,b]}) for b in range(size)] for a in range(size)]
    rhs=[graph.sum([graph.op('MULTIPLY',y,graph.value(x[j],{'design_column':j})) for x,y in zip(xs,ys)]) for j in range(size)]
    for col in range(size):
        pivot=matrix[col][col]
        matrix[col]=[graph.op('DIVIDE',x,pivot) for x in matrix[col]];rhs[col]=graph.op('DIVIDE',rhs[col],pivot)
        for row in range(size):
            if row==col:continue
            factor=matrix[row][col]
            matrix[row]=[graph.op('SUBTRACT',a,graph.op('MULTIPLY',factor,b)) for a,b in zip(matrix[row],matrix[col])]
            rhs[row]=graph.op('SUBTRACT',rhs[row],graph.op('MULTIPLY',factor,rhs[col]))
    values,receipt=native.evaluate(graph,'GW-COM continuous carrier: joint two-channel exact least squares for phase/amplitude and optional channel offsets on quiet calibration samples')
    coeff=[values[x] for x in rhs];receipts=[receipt];prediction=[];residual=[];norm2=[]
    for start in range(0,len(wave),512):
        graph=Graph();cn=[graph.value(c,{'fitted_coefficient':j}) for j,c in enumerate(coeff)];outs=[]
        for i in range(start,min(start+512,len(wave))):
            pp=[];rr=[]
            for channel in (0,1):
                basis=fit_basis(*trigs[i],channel,size)
                p=graph.sum([graph.op('MULTIPLY',c,graph.value(v,{'sample':i,'channel':channel,'role':'design'})) for c,v in zip(cn,basis)])
                r=graph.op('SUBTRACT',graph.value(wave[i][channel],{'raw_sample':i,'channel':channel}),p)
                pp.append(p);rr.append(r)
            n=graph.op('ADD',graph.op('MULTIPLY',rr[0],rr[0]),graph.op('MULTIPLY',rr[1],rr[1]))
            outs.append((pp,rr,n))
        values,receipt=native.evaluate(graph,'GW-COM continuous residual: two signed channels, complete carrier prediction and residual squared norm for marker selection')
        receipts.append(receipt)
        for pp,rr,n in outs:
            prediction.append(tuple(values[v] for v in pp));residual.append(tuple(values[v] for v in rr));norm2.append(values[n])
    assert all(tuple(a-b for a,b in zip(y,p))==r for y,p,r in zip(wave,prediction,residual))
    return coeff,prediction,residual,norm2,receipts


def reference(t,events,active=True):
    # Independent floating-point reference for RK4, not the native producer.
    r,rv,ra=1.,0.,0.
    if active:
        import bisect
        j=bisect.bisect_left(events,t)
        for center in events[max(0,j-1):j+1]:
            u=t-center
            if abs(u)<1:
                b=1-u*u;r+=b**4/16;rv+=-u*b**3/2;ra+=b*b*(7*u*u-1)/2
    c,s=math.cos(t),math.sin(t)
    x,y=r*c,r*s;vx,vy=rv*c-r*s,rv*s+r*c
    fr,ft=ra-r+1/r**2,2*rv
    return (x,y,vx,vy),(fr*c-ft*s,fr*s+ft*c)


def integrate_check(events,end,step,active=True):
    events=[float(t) for t in events]
    state=[1.,0.,0.,1.];t=0.;maximum=0.;wave_error=0.;work=0.;max_feedback=0.;trajectory=[]
    def derivative(t,z):
        target,ff=reference(t,events,active)
        x,y,vx,vy=z;radius=math.hypot(x,y)
        feedback=[4*(target[i]-z[i])+4*(target[i+2]-z[i+2]) for i in (0,1)]
        force=[ff[i]+feedback[i] for i in (0,1)]
        return [vx,vy,-x/radius**3+force[0],-y/radius**3+force[1]],2*(force[0]*vx+force[1]*vy),math.hypot(*feedback)
    count=round(end/step)
    for k in range(count):
        t=k*step
        k1,p1,_=derivative(t,state)
        k2,p2,_=derivative(t+step/2,[a+step*b/2 for a,b in zip(state,k1)])
        k3,p3,_=derivative(t+step/2,[a+step*b/2 for a,b in zip(state,k2)])
        k4,p4,_=derivative(t+step,[a+step*b for a,b in zip(state,k3)])
        state=[a+step*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(state,k1,k2,k3,k4)]
        work+=step*(p1+2*p2+2*p3+p4)/6
        now=(k+1)*step;target,_=reference(now,events,active)
        maximum=max(maximum,max(abs(a-b) for a,b in zip(state,target)))
        derivative_now,_,feedback=derivative(now,state);max_feedback=max(max_feedback,feedback)
        if (k+1)%round(F(1,8)/F(str(step)))==0:
            x,y,vx,vy=state;ax,ay=derivative_now[2:]
            integrated=(4*(vx*vx-vy*vy+x*ax-y*ay),4*(ax*y+2*vx*vy+x*ay))
            tr,tf=reference(now,events,active);tx,ty,tvx,tvy=tr;radius=math.hypot(tx,ty)
            tax,tay=-tx/radius**3+tf[0],-ty/radius**3+tf[1]
            expected=(4*(tvx*tvx-tvy*tvy+tx*tax-ty*tay),4*(tax*ty+2*tvx*tvy+tx*tay))
            wave_error=max(wave_error,max(abs(a-b) for a,b in zip(integrated,expected)))
            radius=math.hypot(x,y)
            trajectory.append([now,x,y,vx,vy,ax,ay,ax+x/radius**3,ay+y/radius**3,
                               vx*vx+vy*vy-2/radius,work,*integrated])
    x,y,vx,vy=state;energy=vx*vx+vy*vy-2/math.hypot(x,y)
    return {'step':step,'steps':count,'maximum_state_error':maximum,'maximum_wave_error':wave_error,
            'maximum_feedback_correction':max_feedback,'final_energy':energy,'integrated_signed_work':work,
            'energy_balance_error':abs(energy+1-work),'trajectory_columns':['time','x','y','vx','vy','ax','ay','force_x','force_y','pair_energy','integrated_pair_work','H_plus','H_cross'],
            'sampled_trajectory':trajectory,'scope':'Independent float RK4 of Newtonian acceleration plus reference feedforward and kp=kd=4 tracking; no radiation reaction'}
