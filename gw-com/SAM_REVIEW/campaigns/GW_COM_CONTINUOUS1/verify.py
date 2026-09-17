"""Verify native reference mechanics, Cartesian waveform and retained fit/residual chain."""
from fractions import Fraction as F
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
from GW_COM.runtime.evidence import Store,encode


def main():
    run=HERE/'run001';refined=HERE/'refinement001'
    old=Store(ROOT,run/'records',run/'METHOD.json');new=Store(ROOT,refined/'records',refined/'METHOD.json')
    mechanics=old.payload(old.ref(run/'records/reference_mechanics.json'))
    rows={int(k):{name:F(v) for name,v in value.items()} for k,value in mechanics['profiles'].items()}
    for k,p in rows.items():
        u=F(k,8);b=1-u*u
        r=1+b**4/16;v=-u*b**3/2;a=b*b*(7*u*u-1)/2
        assert (p['radius'],p['radial_velocity'],p['radial_acceleration'])==(r,v,a)
        assert p['force_radial']==a-r+1/r**2 and p['force_tangential']==2*v
        assert p['energy']==v*v+r*r-2/r
        assert p['power']==2*v*(a+r+1/r**2)==p['energy_derivative']
    assert all(rows[-8][k]==rows[8][k]==0 for k in ['radial_velocity','radial_acceleration','force_radial','force_tangential','power'])
    records=0;wave_samples=0;residual_samples=0;max_cartesian_error=0.
    for store in (old,new):
        for path in store.directory.glob('*.json'):
            record=json.loads(path.read_text())
            if record.get('schema')=='GW_COM_EVIDENCE_V1':store.verify(store.ref(path));records+=1
    for name in ('continuous_prime','continuous_unmodulated'):
        source=json.loads((run/'records'/f'{name}.source.data.json').read_text())
        wave=[[F(v) for v in pair] for pair in source['waveform']]
        for i,(hp,hx) in enumerate(wave):
            p=rows[source['profile_indices'][i]];r,v,a=(float(p[k]) for k in ('radius','radial_velocity','radial_acceleration'))
            t=i/8;c,s=math.cos(t),math.sin(t)
            x,y=r*c,r*s;vx,vy=v*c-r*s,v*s+r*c
            ax,ay=(a-r)*c-2*v*s,(a-r)*s+2*v*c
            expected=(4*(vx*vx-vy*vy+x*ax-y*ay),4*(ax*y+2*vx*vy+x*ay))
            error=max(abs(float(actual)-wanted) for actual,wanted in zip((hp,hx),expected))
            assert error<1e-10
            max_cartesian_error=max(max_cartesian_error,error);wave_samples+=2
        for size in (2,4):
            fit=json.loads((run/'records'/f'{name}.fit{size}.data.json').read_text())
            residual=json.loads((run/'records'/f'{name}.residual{size}.data.json').read_text())
            coeff=list(map(F,fit['coefficients']))
            pred=[[F(v) for v in pair] for pair in fit['predicted_samples']]
            res=[[F(v) for v in pair] for pair in residual['signed_samples']]
            for i,(y,forecast,remainder) in enumerate(zip(wave,pred,res)):
                c,s=map(F,source['trig_inputs'][i])
                bases=([c,-s,F(1),F(0)][:size],[s,c,F(0),F(1)][:size])
                for channel in (0,1):
                    assert forecast[channel]==sum(a*b for a,b in zip(coeff,bases[channel]))
                    assert y[channel]-forecast[channel]==remainder[channel];residual_samples+=1
                assert sum(v*v for v in remainder)==F(residual['norm_squared'][i])
    ledger=old.payload(old.ref(run/'records/work_ledger.json'))
    assert F(ledger['per_marker_positive_work'])==F(1073,4352)
    assert F(ledger['all_markers_positive_work'])==22*F(1073,4352)
    final=json.loads((refined/'records/RESULT.json').read_text())
    assert final['cases']['continuous_prime']['admitted'] and final['cases']['continuous_prime']['exact_match']
    assert not final['cases']['continuous_unmodulated']['admitted']
    assert final['cases']['continuous_unmodulated']['decoded'] is None
    report={'status':'PASS','evidence_records_verified':records,'native_profile_rows':len(rows),
            'cartesian_wave_channel_samples_checked':wave_samples,'exact_residual_channel_samples_checked':residual_samples,
            'maximum_native_vs_cartesian_wave_error':max_cartesian_error,
            'positive_work_identity':'1073/4352 per marker, 22 markers',
            'refined_admissions':'prime admitted with exact seven values; unmodulated blocked'}
    with (HERE/'VALIDATION.json').open('xb') as f:f.write(encode(report))
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
