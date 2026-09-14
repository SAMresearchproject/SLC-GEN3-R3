#!/usr/bin/env python3
"""Compile a factored, exact Li-6 motif and circulation trial."""
import csv
from fractions import Fraction as F
from itertools import combinations, permutations
from math import lcm
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
CURRENT=ROOT/'CURRENT_REVISION/domains/ATOM3D'
PRIOR=ROOT/'SAM_REVIEW/campaigns/A3D41_LI6_SOURCE_CHANNEL_MAP1'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(p,x):Path(p).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')

def inverse(matrix):
    n=len(matrix);a=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if a[i][col])
        a[col],a[pivot]=a[pivot],a[col];factor=a[col][col]
        a[col]=[v/factor for v in a[col]]
        for i in range(n):
            if i!=col:
                factor=a[i][col];a[i]=[u-factor*v for u,v in zip(a[i],a[col])]
    return [row[n:] for row in a]

def rank(matrix):
    a=[[F(x) for x in row] for row in matrix];r=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];v=a[r][col];a[r]=[x/v for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def main():
    sheet=read(CURRENT/'li6_construction/BUILD_SHEET.json')
    old=read(CURRENT/'li6_assembly_source/CONTRACT.json')
    qp_path=PRIOR/'inputs/QP093A_321_ROW_BUCKET_MAP.csv'
    qp=list(csv.DictReader(qp_path.open()))
    by_route={r['route_combination']:r for r in qp}
    obs={r['candidate_id']:r for r in csv.DictReader((PRIOR/'inputs/CR238_matter_row_audit.csv').open())}
    objects=sheet['objects'];order=[o['object_id'] for o in objects]
    relations=sheet['relations'];ids=[r['relation_id'] for r in relations]
    ends=[[order.index(r['source_object']),order.index(r['target_object'])] for r in relations]
    edge_lookup={frozenset(pair):i for i,pair in enumerate(ends)}
    B=np.zeros((6,9),np.int16)
    for e,(a,b) in enumerate(ends):B[a,e]=-1;B[b,e]=1
    masks=np.ones((4,9),np.int16);masks[0,[1,4]]=0;masks[1,4]=0;masks[2,1]=0
    one_body=[]
    for o in objects:
        mode=o['n100_role_type'];anti=mode.startswith('anti_');mode=mode.removeprefix('anti_')
        route=f"{mode}_single_write[p={o['p']},g={o['g']}]"
        if anti:route=f'anti({route})'
        row=by_route[route]
        assert F(row['M_native'])==F(o['M_native'])
        one_body.append({'object':o,'source_row':row['candidate_id'],'route':route})
    pair_rows=[]
    for r,(a,b) in zip(relations,ends):
        row=by_route[f"pair_write[{objects[a]['p']}|anti{objects[b]['p']}]"]
        assert row['matter_row_allowed']=='yes'
        pair_rows.append({'relation_id':r['relation_id'],'source_row':row['candidate_id'],
          'native':str(F(row['M_native'])),'observed':str(F(obs[row['candidate_id']]['M_obs'])),
          'projection':'CANDIDATE_PARTITION_TUPLE_TO_TWO_OWNER_MOTIF',
          'endpoint_context':[objects[a],objects[b]]})

    cycles=[];triads=[]
    def cycle(nodes):
        c=np.zeros(9,np.int16)
        for a,b in zip(nodes,nodes[1:]+nodes[:1]):
            e=edge_lookup[frozenset((a,b))];c[e]=1 if ends[e]==[a,b] else -1
        return c
    for nodes in combinations(range(6),3):
        if not all(frozenset(pair) in edge_lookup for pair in combinations(nodes,2)):continue
        p=sorted(objects[i]['p'] for i in nodes)
        row=by_route['color_triad['+'+'.join(map(str,p))+']']
        if row['matter_row_allowed']!='yes':continue
        c=cycle(list(nodes));cycles.append(c)
        triads.append({'index':len(triads),'objects':[order[i] for i in nodes],
          'edge_indices':np.flatnonzero(c).tolist(),'cycle_incidence':c.tolist(),
          'source_row':row['candidate_id'],'native':str(F(row['M_native'])),
          'observed':str(F(obs[row['candidate_id']]['M_obs'])),
          'projection':'CANDIDATE_PARTITION_TUPLE_TO_THREE_OWNER_CIRCULATION'})
    squares={}
    for nodes in permutations(range(6),4):
        pairs=[frozenset((a,b)) for a,b in zip(nodes,nodes[1:]+nodes[:1])]
        if all(pair in edge_lookup for pair in pairs):
            edges=frozenset(edge_lookup[p] for p in pairs)
            if {1,4,7}<=edges and edges not in squares:squares[edges]=list(nodes)
    assert len(triads)==4 and len(squares)==1
    square=cycle(next(iter(squares.values())));cycles.append(square);C=np.array(cycles,np.int16)
    covers=[]
    for bits in range(1<<len(triads)):
        chosen=[i for i in range(len(triads)) if bits>>i&1]
        covered=[e for i in chosen for e in triads[i]['edge_indices']]
        if len(covered)!=len(set(covered)):continue
        covers.append({'id':f'COVER_{len(covers):02d}','triads':chosen,
                       'pair_edges':[e for e in range(9) if e not in covered]})
    assert len(covers)==5
    independent=[]
    for i in range(len(C)):
        if rank(C[independent+[i]].tolist())>len(independent):independent.append(i)
    A=np.vstack((B[:5],C[independent]));assert A.shape==(9,9)
    inv=inverse(A.tolist());den=lcm(*(x.denominator for row in inv for x in row))
    invnum=np.array([[int(x*den) for x in row] for row in inv],np.int64)
    assert np.array_equal(invnum@A,den*np.eye(9,dtype=np.int64))
    geometry={'object_order':order,'endpoints':ends,'relation_ids':ids,
      'site_incidence':B.tolist(),'masks':masks.tolist(),
      'mask_names':['SEPARATED','PLUS_JOIN','MINUS_JOIN','CONNECTED'],
      'one_body':one_body,'pair_motifs':pair_rows,'triad_motifs':triads,'covers':covers,
      'cycle_incidence':C.tolist(),'depth_cycle_objects':[order[i] for i in next(iter(squares.values()))],
      'independent_cycle_rows':independent,'site_rank':rank(B.tolist()),'cycle_rank':rank(C.tolist()),
      'combined_rank':rank(np.vstack((B,C)).tolist()),'inverse_input_rows':'B first five rows, then independent C rows',
      'edge_inverse_numerator':invnum.tolist(),'edge_inverse_denominator':den,
      'catalog_bucket_counts':{b:sum(r['structural_bucket']==b for r in qp) for b in sorted({r['structural_bucket'] for r in qp})},
      'whole_column_relation_indices':[[ids.index(r) for r in column['ordered_relation_ids']] for column in sheet['qp_presentation_columns']],
      'source_assignments':old['assignments'],'center_relation_indices':[ids.index(r) for r in old['relation_order']]}
    save(HERE/'GEOMETRY.json',geometry)

    inputs=HERE/'inputs';inputs.mkdir(exist_ok=True)
    snapshots=[qp_path,PRIOR/'SOURCE_CHANNEL_MAP.json',PRIOR/'inputs/CR238_matter_row_audit.csv',
               CURRENT/'li6_construction/BUILD_SHEET.json',CURRENT/'li6_assembly_source/CONTRACT.json']
    manifest=[]
    for p in snapshots:
        dest=inputs/p.name;shutil.copyfile(p,dest)
        manifest.append({'path':str(p.relative_to(ROOT)),'snapshot':str(dest.relative_to(HERE)),'sha256':sha(p),'bytes':p.stat().st_size})
    save(HERE/'SOURCE_MANIFEST.json',manifest)
    for oldname,newname in [('FEATURES.i16le','CENTER_FEATURES.i16le'),('FEATURE_REPRESENTATIVE.u32le','CENTER_REPRESENTATIVE.u32le'),
                            ('SOURCE_TO_FEATURE.u32le','CENTER_INVERSE.u32le'),('TMR1_RECIPROCAL_REDUCED.i64le','TMR1.i64le')]:
        shutil.copyfile(CURRENT/'li6_assembly_source'/oldname,HERE/newname)
    tensor=np.fromfile(HERE/'TMR1.i64le',dtype='<i8').reshape(3,128,3)
    cc=np.zeros((384,9),np.int64)
    for e in range(3):cc[e*128:(e+1)*128,e*3:(e+1)*3]=tensor[e]
    cc.astype('<i8').tofile(HERE/'CENTER_COEFFICIENTS.i64le')
    rawref=old['raw_current'];raw=np.memmap(ROOT/rawref['path'],mode='r',dtype=np.int8,shape=tuple(rawref['shape']))
    assert sha(ROOT/rawref['path'])==rawref['sha256']
    address=np.arange(raw.shape[0],dtype=np.uint32)
    q=np.stack([((address>>e)&1)+2*((address>>(e+9))&1) for e in range(9)],axis=1)
    f=np.empty((len(address),2,4,14),np.int16)
    recovery_checks=[]
    for kind in range(2):
        phase=q if kind==0 else q%2
        re=np.array([1,0,-1,0],np.int16)[phase];im=np.array([0,1,0,-1],np.int16)[phase]
        for m,mask in enumerate(masks):
            zr=re*mask;zi=im*mask;cr=zr@C.T;ci=zi@C.T
            j=np.asarray(raw[:,kind,m],dtype=np.int16)
            for e,(a,b) in enumerate(ends):f[:,kind,m,e]=(j[:,0,a]-j[:,0,b])**2+(j[:,1,a]-j[:,1,b])**2
            f[:,kind,m,9:]=cr*cr+ci*ci
            for side,(z,circulation) in enumerate(((zr,cr),(zi,ci))):
                coords=np.concatenate((j[:,side,:5],circulation[:,independent]),axis=1).astype(np.int64)
                assert np.array_equal(coords@invnum.T,den*z)
            recovery_checks.append({'kind':kind,'mask':m,'states':len(address),'exact_edge_reconstruction':True})
    # A common quarter turn rotates both site current and cycle circulation.
    assert np.array_equal(((-im)@C.T)**2+(re@C.T)**2,(re@C.T)**2+(im@C.T)**2)
    unique,reps,inverse_map=np.unique(f.reshape(-1,14),axis=0,return_index=True,return_inverse=True)
    unique.astype('<i2').tofile(HERE/'GRAMMAR_FEATURES.i16le')
    reps.astype('<u4').tofile(HERE/'GRAMMAR_REPRESENTATIVE.u32le')
    inverse_map.astype('<u4').tofile(HERE/'GRAMMAR_INVERSE.u32le')
    del f
    meta=[];gc=[]
    for channel in ('native','observed'):
        for receiver in ('CIRCULATION','ENDPOINT'):
            for m,mask in enumerate(masks):
                for cover in covers:
                    coeff=[F(0)]*14
                    for e in cover['pair_edges']:
                        if mask[e]:coeff[e]+=576*F(pair_rows[e][channel])
                    for t in cover['triads']:
                        w=576*F(triads[t][channel])/3
                        if receiver=='CIRCULATION':coeff[9+t]+=w
                        else:
                            for e in triads[t]['edge_indices']:coeff[e]+=w
                    assert all(x.denominator==1 for x in coeff)
                    gc.append([int(x) for x in coeff]);meta.append({'index':len(meta),'type':'MOTIF_ACTION',
                        'channel':channel,'receiver':receiver,'mask':m,'cover':cover['id'],'denominator':576})
    for m in range(4):
        coeff=[0]*14;coeff[13]=81 if m==3 else 0
        gc.append(coeff);meta.append({'index':len(meta),'type':'HIDDEN_LIFT_LOOP','mask':m,'denominator':576})
    for name,col in [('PHI_MINUS',0),('PHI_PLUS',2)]:
        coeff=[0]*14
        for e in geometry['whole_column_relation_indices'][col]:coeff[e]=192
        gc.append(coeff);meta.append({'index':len(meta),'type':name,'denominator':576})
    coeff=[0]*14
    for e in geometry['whole_column_relation_indices'][0]:coeff[e]-=1
    for e in geometry['whole_column_relation_indices'][2]:coeff[e]+=1
    gc.append(coeff);meta.append({'index':len(meta),'type':'SIGNED_PAIR_SURFACE','denominator':576})
    gc=np.array(gc,dtype='<i8');gc.tofile(HERE/'GRAMMAR_COEFFICIENTS.i64le')
    save(HERE/'GRAMMAR_OUTPUTS.json',meta)
    batches=[]
    for name,features,coefficients,width in [('CENTER','CENTER_FEATURES.i16le','CENTER_COEFFICIENTS.i64le',9),
                                             ('GRAMMAR','GRAMMAR_FEATURES.i16le','GRAMMAR_COEFFICIENTS.i64le',14)]:
        n=(HERE/features).stat().st_size//(2*width);cols=(HERE/coefficients).stat().st_size//(8*width)
        fv=np.fromfile(HERE/features,dtype='<i2').reshape(n,width)
        cv=np.fromfile(HERE/coefficients,dtype='<i8').reshape(cols,width)
        bound=max(sum(int(x)*int(y) for x,y in zip(np.max(np.abs(fv),axis=0),np.abs(row))) for row in cv)
        assert bound<2**63
        batches.append({'name':name,'features':features,'representatives':name+'_REPRESENTATIVE.u32le',
          'coefficients':coefficients,'feature_count':n,'feature_width':width,'output_width':cols,'integer_abs_bound':bound})
    assets={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in HERE.iterdir() if p.is_file() and p.suffix in ('.i16le','.i64le','.u32le')}
    contract={'schema':'A3D41_LI6_GRAMMAR_CONTRACT_V1','operation':'LI6_GRAMMAR','domain_revision':'A3D41-T18-CONTACT-R2',
      'raw_current':rawref,'geometry':geometry,'batches':batches,'assets':assets,'output_metadata':meta,
      'source_history':['H000969','H000974','H000975'],'geometry_sha256':sha(HERE/'GEOMETRY.json'),
      'technical_map_sha256':sha(HERE/'TECHNICAL_MAP.md'),'center_output_multiplier':8,
      'grammar_output_denominator':576,'represented_source_rows':2097152,
      'physical_prediction_law_installed':False,'candidate_operator_provenance':'CODEX_PROPOSAL_AUTHORIZED_FOR_TRIAL'}
    save(HERE/'CONTRACT.json',contract)
    save(HERE/'PREPARATION.json',{'status':'PASS','edge_reconstruction':recovery_checks,
      'reconstructed_edge_coordinates':262144*2*4*2*9,'quarter_rotation_invariance':True,
      'site_rank':geometry['site_rank'],'cycle_rank':geometry['cycle_rank'],'combined_rank':geometry['combined_rank'],
      'batches':batches,'triangle_count':len(triads),'cover_count':len(covers)})
    print(json.dumps({'covers':len(covers),'triangles':len(triads),'site_rank':geometry['site_rank'],
      'cycle_rank':geometry['cycle_rank'],'batches':batches},indent=2))

if __name__=='__main__':main()
