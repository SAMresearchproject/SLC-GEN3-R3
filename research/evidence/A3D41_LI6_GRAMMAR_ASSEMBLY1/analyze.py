#!/usr/bin/env python3
"""Exact minima of the factored Li-6 grammar action, retaining every tie."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import time
import numpy as np

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def read(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    started=time.perf_counter();c=read(HERE/'CONTRACT.json');g=c['geometry'];run=read(HERE/'FULL_CLI.json');rp=Path(run['result_directory'])
    nc=c['batches'][0]['feature_count'];ng=c['batches'][1]['feature_count'];nw=c['batches'][1]['output_width']
    primitive=np.fromfile(rp/'CENTER_RESPONSE.i64le',dtype='<i8').reshape(nc,3,128)
    grammar=np.fromfile(rp/'GRAMMAR_RESPONSE.i64le',dtype='<i8').reshape(ng,nw)
    ci=np.fromfile(HERE/'CENTER_INVERSE.u32le',dtype='<u4').reshape(262144,2,4)
    gi=np.fromfile(HERE/'GRAMMAR_INVERSE.u32le',dtype='<u4').reshape(262144,2,4)
    gf=np.fromfile(HERE/'GRAMMAR_FEATURES.i16le',dtype='<i2').reshape(ng,14)
    cf=np.fromfile(HERE/'CENTER_FEATURES.i16le',dtype='<i2').reshape(nc,3,3)
    tensor=np.fromfile(HERE/'TMR1.i64le',dtype='<i8').reshape(3,128,3)
    raw=np.memmap(ROOT/c['raw_current']['path'],dtype=np.int8,mode='r',shape=tuple(c['raw_current']['shape']))
    old_contact=np.sum(np.asarray(raw[:,0,3],dtype=np.int16)**2,axis=(1,2))==2
    weights=np.array([r['native_account_numerators'] for r in g['source_assignments']],np.int64)
    mask_center=np.array(g['masks'],np.int64)[:,g['center_relation_indices']]
    shape=(2,4,2,2,5,2,6,128)
    offsets=np.empty(shape,dtype='<i8');set_indices=np.empty(shape,dtype='<u4');counts=np.empty(shape,dtype='<u4')
    bases=np.empty((2,4,6,128),dtype='<i8');all_sets=[];set_lookup={};set_info=[]
    metadata=c['output_metadata'];channels=('native','observed');receivers=('CIRCULATION','ENDPOINT')
    motif_index={(r['channel'],r['receiver'],r['mask'],r['cover']):r['index'] for r in metadata if r['type']=='MOTIF_ACTION'}
    lift_index={r['mask']:r['index'] for r in metadata if r['type']=='HIDDEN_LIFT_LOOP'}
    diagnostic={r['type']:r['index'] for r in metadata if r['type'] in ('PHI_MINUS','PHI_PLUS','SIGNED_PAIR_SURFACE')}
    checks=[]
    def check(name,test):
        checks.append({'name':name,'pass':bool(test)})
        if not test:raise AssertionError(name)
    check('hardware exact agreement',run['three_way_exact_agreement'])
    check('old contact address join',int(old_contact.sum())==256)
    check('nonnegative center primitives',bool(np.all(primitive>=0)))
    check('phase-current reconstruction',all(r['exact_edge_reconstruction'] for r in read(HERE/'PREPARATION.json')['edge_reconstruction']))
    check('complete edge information rank',g['site_rank']==5 and g['cycle_rank']==4 and g['combined_rank']==9)
    # This checks new source-feature wiring under the native quarter turn.
    a=np.arange(262144,dtype=np.uint32);q=np.stack([((a>>e)&1)+2*((a>>(e+9))&1) for e in range(9)],axis=1)
    rotated=(q+1)%4;ra=np.zeros(len(a),np.uint32)
    for e in range(9):ra|=((rotated[:,e]&1)<<e)|(((rotated[:,e]>>1)&1)<<(e+9))
    for m in range(4):check(f'new motif quarter rotation mask {m}',np.array_equal(gf[gi[:,0,m]],gf[gi[ra,0,m]]))
    # Coordinate covariance of the inherited directional tensor, not a new
    # fixed-matrix rotational symmetry assumption.
    for e in range(3):
        rot_f=cf[:,e][:,[2,1,0]].copy();rot_f[:,1]*=-1
        rot_t=tensor[e][:,[2,1,0]].copy();rot_t[:,1]*=-1
        check(f'center coordinate covariance relation {e}',np.array_equal(rot_f@rot_t.T,primitive[:,e]))
    check('whole-column signed surface identity',
          np.array_equal(192*grammar[:,diagnostic['SIGNED_PAIR_SURFACE']],
                         grammar[:,diagnostic['PHI_PLUS']]-grammar[:,diagnostic['PHI_MINUS']]))
    max_eligible=0;direct_checks=0;max_filter_width=0
    for kind in range(2):
        for m in range(4):
            cidx=ci[:,kind,m];gidx=gi[:,kind,m];occupied=np.unique(cidx)
            center=np.einsum('fer,ae->far',primitive,weights*mask_center[m],optimize=False,dtype=np.int64)
            base=center[occupied].min(axis=0);bases[kind,m]=base
            delta=center[occupied]-base[None,:,:]
            for ch,channel in enumerate(channels):
                for rec,receiver in enumerate(receivers):
                    for cover_no,cover in enumerate(g['covers']):
                        mi=motif_index[(channel,receiver,m,cover['id'])]
                        for hidden in range(2):
                            if hidden and m!=3:
                                offsets[kind,m,ch,rec,cover_no,hidden]=offsets[kind,m,ch,rec,cover_no,0]
                                set_indices[kind,m,ch,rec,cover_no,hidden]=set_indices[kind,m,ch,rec,cover_no,0]
                                counts[kind,m,ch,rec,cover_no,hidden]=counts[kind,m,ch,rec,cover_no,0]
                                continue
                            values=grammar[gidx,mi].copy()
                            if hidden:values+=grammar[gidx,lift_index[m]]
                            gmin=np.full(nc,np.iinfo(np.int64).max,np.int64);np.minimum.at(gmin,cidx,values)
                            low=int(values.min());minimal_for_center=values==gmin[cidx]
                            cached={}
                            for assignment in range(6):
                                for r in range(128):
                                    dd=delta[:,assignment,r]
                                    upper=int(gmin[occupied[dd==0]].min())
                                    width=(upper-low)//4608;max_filter_width=max(max_filter_width,width)
                                    eligible=dd<=width;ids=occupied[eligible]
                                    score=dd[eligible]*4608+gmin[ids]
                                    best=int(score.min());selected=tuple(int(x) for x in ids[score==best])
                                    max_eligible=max(max_eligible,len(ids))
                                    if selected not in cached:
                                        accepted=np.zeros(nc,bool);accepted[list(selected)]=True
                                        selected_states=accepted[cidx]&minimal_for_center
                                        packed=np.packbits(selected_states,bitorder='little');digest=sha(packed.tobytes())
                                        if digest not in set_lookup:
                                            index=len(all_sets);set_lookup[digest]=index;all_sets.append(packed)
                                            addresses=np.flatnonzero(selected_states)
                                            set_info.append({'index':index,'sha256':digest,'count':int(len(addresses)),
                                               'first_address':int(addresses[0]),'old_contact_overlap':int(np.sum(selected_states&old_contact))})
                                        cached[selected]=set_lookup[digest]
                                    index=cached[selected];loc=(kind,m,ch,rec,cover_no,hidden,assignment,r)
                                    offsets[loc]=best;set_indices[loc]=index;counts[loc]=set_info[index]['count']
                            # Unfiltered Python-integer contraction checks the
                            # filter at one fixed coordinate of every group.
                            direct=min(4608*int(d)+int(x) for d,x in zip(delta[:,0,0],gmin[occupied]))
                            check(f'exact lower-bound filter {kind}/{m}/{ch}/{rec}/{cover_no}/{hidden}',
                                  direct==int(offsets[kind,m,ch,rec,cover_no,hidden,0,0]))
                            direct_checks+=1
            print(json.dumps({'kind':kind,'mask':m,'minimum_sets':len(all_sets),'elapsed_seconds':time.perf_counter()-started}),flush=True)
    np.save(HERE/'MINIMUM_OFFSETS.npy',offsets)
    np.save(HERE/'MINIMUM_SET_INDEX.npy',set_indices)
    np.save(HERE/'MINIMUM_COUNTS.npy',counts)
    np.save(HERE/'CENTER_BASE.npy',bases)
    np.savez_compressed(HERE/'MINIMUM_BITSETS.npz',sets=np.stack(all_sets))
    save(HERE/'MINIMUM_SET_INFO.json',set_info)
    axis={'shape':list(shape),'axes':['map','mask','source_channel','triad_receiver','motif_cover','hidden_loop','center_placement','rho'],
       'values':[['NATIVE','PHASE_ERASED'],g['mask_names'],list(channels),list(receivers),[x['id'] for x in g['covers']],
                 ['OFF','ON'],list(range(6)),list(range(1,129))],
       'exact_minimum_formula':'8*CENTER_BASE[map,mask,placement,rho] + MINIMUM_OFFSETS[all_axes]/576',
       'bit_order':'little','source_address_count':262144,'cases':int(np.prod(shape))}
    save(HERE/'MINIMUM_METADATA.json',axis)
    connected=[]
    for ch,channel in enumerate(channels):
        for rec,receiver in enumerate(receivers):
            for cover_no,cover in enumerate(g['covers']):
                for hidden in range(2):
                    loc=(0,3,ch,rec,cover_no,hidden,0,0);index=int(set_indices[loc])
                    value=F(int(bases[0,3,0,0]))*8+F(int(offsets[loc]),576)
                    families=np.unique(set_indices[0,3,ch,rec,cover_no,hidden])
                    connected.append({'channel':channel,'receiver':receiver,'cover':cover['id'],
                      'triad_objects':[g['triad_motifs'][t]['objects'] for t in cover['triads']],
                      'hidden_loop':bool(hidden),'minimum':str(value),'states':int(counts[loc]),
                      'old_contact_overlap':set_info[index]['old_contact_overlap'],'set_index':index,
                      'same_state_set_all_placements_and_rho':len(families)==1})
    # Source histories indistinguishable by the full signed site current but
    # distinguished by retained circulation and a new motif response.
    anchor=int(np.flatnonzero(old_contact)[0]);j0=raw[anchor,0,3]
    same=np.flatnonzero(np.all(raw[:,0,3]==j0,axis=(1,2)))
    anchor_cycle=gf[gi[anchor,0,3],9:]
    other=int(next(s for s in same if np.any(gf[gi[s,0,3],9:]!=anchor_cycle)))
    diff=grammar[gi[other,0,3]]-grammar[gi[anchor,0,3]]
    differing=next(row for row in metadata if row['type']=='MOTIF_ACTION' and row['receiver']=='CIRCULATION' and row['mask']==3 and diff[row['index']]!=0)
    witness={'states':[anchor,other],'site_current':np.asarray(j0).tolist(),
      'circulation_norms':[anchor_cycle.tolist(),gf[gi[other,0,3],9:].tolist()],
      'distinguishing_response':differing,'source_action_difference':str(F(int(diff[differing['index']]),576))}
    save(HERE/'CIRCULATION_WITNESS.json',witness)
    # Complete ground-reference differences are held exactly in the same
    # factored baseline/offset representation.
    releases=[]
    for ch,channel in enumerate(channels):
        for rec,receiver in enumerate(receivers):
            for cover_no,cover in enumerate(g['covers']):
                for hidden in range(2):
                    loc0=(0,0,ch,rec,cover_no,hidden,0,0);loc1=(0,3,ch,rec,cover_no,hidden,0,0)
                    delta=8*F(int(bases[0,0,0,0])-int(bases[0,3,0,0]))+F(int(offsets[loc0])-int(offsets[loc1]),576)
                    releases.append({'channel':channel,'receiver':receiver,'cover':cover['id'],'hidden_loop':bool(hidden),
                      'placement':0,'rho':1,'separated_minus_connected_minimum':str(delta)})
    save(HERE/'REFERENCE_EXAMPLES.json',releases)
    check('hidden loop inactive before complete joining',np.array_equal(offsets[:,:3,:,:,:,0],offsets[:,:3,:,:,:,1]))
    check('every case has a minimizing source address',bool(np.all(counts>0)))
    check('same-current histories have different circulation response',F(witness['source_action_difference'])!=0)
    result={'schema':'A3D41_LI6_GRAMMAR_RESULT_V1','status':'COMPLETE','hardware_run':run,
      'source_geometry':{'site_rank':g['site_rank'],'cycle_rank':g['cycle_rank'],'combined_rank':g['combined_rank'],
        'triangles':4,'new_depth_cycles':1,'covers':5},
      'new_response_values':run['new_response_values'],'minimum_cases':int(np.prod(shape)),
      'unique_minimum_sets':len(all_sets),'maximum_filter_width_in_center_units':max_filter_width,
      'maximum_eligible_center_features':max_eligible,'unfiltered_exact_checks':direct_checks,
      'connected_examples':connected,'circulation_witness':witness,
      'native_phase_erased_distinct_cases':int(np.sum(set_indices[0]!=set_indices[1])),
      'physical_binding_energy_computed':False,'physical_exterior_tensor_type_selected':False,
      'scientific_result_classification':'The test result suggests strong contact with the concept.',
      'classification_scope':'Finite isotope-specific grammar assembly, retained circulation distinction, and exact candidate source-action selection.',
      'analysis_seconds':time.perf_counter()-started,'checks':checks}
    save(HERE/'RESULT.json',result)
    save(HERE/'VALIDATION.json',{'status':'PASS','check_count':len(checks),'checks':checks,'result_sha256':sha((HERE/'RESULT.json').read_bytes())})
    print(json.dumps({'status':'PASS','cases':result['minimum_cases'],'unique_sets':len(all_sets),'checks':len(checks),
      'connected_circulation_observed':[r for r in connected if r['channel']=='observed' and r['receiver']=='CIRCULATION']},indent=2),flush=True)

if __name__=='__main__':main()
