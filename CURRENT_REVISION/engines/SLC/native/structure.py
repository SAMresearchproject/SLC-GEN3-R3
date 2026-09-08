"""Exact component-conditional graph spectra, recovered from the N100 route.

Counts retain every requested port state; disconnected source components are
enumerated in bounded chunks and combined by exact integer convolution.
"""
from collections import Counter
import multiprocessing as mp
import os
import time

from .exact import ExactError, integer, seal

H14F_CPUS=(0,2,4,6,8,10,12,13,14,15,16,17,18,19)


def prepare(instance, ports):
    n=integer(instance["N"],minimum=1)
    ports=tuple(integer(x,minimum=0) for x in ports)
    if len(set(ports))!=len(ports) or any(p>=n for p in ports): raise ExactError("invalid retained ports")
    fields=tuple(integer(x) for x in instance["fields"])
    if len(fields)!=n: raise ExactError("source field count differs")
    if any(any(integer(x) for x in factor["energy_table"]) for factor in instance.get("native_factors",[])):
        raise ExactError("nonzero higher-order factors require their native factor route")
    edges=[];seen=set();adj=[set() for _ in range(n)]
    for edge in instance["edges"]:
        u,v,j=integer(edge["u"]),integer(edge["v"]),integer(edge["J"])
        if not 0<=u<n or not 0<=v<n or u==v:raise ExactError("invalid source relation")
        pair=tuple(sorted((u,v)))
        if pair in seen:raise ExactError("duplicate source relation")
        seen.add(pair);edges.append((u,v,j));adj[u].add(v);adj[v].add(u)
    remaining=set(range(n));components=[]
    while remaining:
        seed=min(remaining);remaining.remove(seed);stack=[seed];group=[]
        while stack:
            u=stack.pop();group.append(u)
            for v in sorted(adj[u]&remaining):remaining.remove(v);stack.append(v)
        components.append(sorted(group))
    port_groups=[i for i,group in enumerate(components) if set(group)&set(ports)]
    if len(port_groups)>1 or max(map(len,components))>24:
        raise ExactError("component route requires localized retained ports and components of at most 24 source variables")
    jobs=[]
    for group_index,group in enumerate(components):
        lookup={u:i for i,u in enumerate(group)}
        local_edges=[(lookup[u],lookup[v],j) for u,v,j in edges if u in lookup and v in lookup]
        local_ports=[(lookup[u],i) for i,u in enumerate(ports) if u in lookup]
        body={"group":group_index,"edges":local_edges,"fields":[fields[u] for u in group],"ports":local_ports}
        for start in range(0,1<<len(group),4096):
            jobs.append({**body,"start":start,"end":min(start+4096,1<<len(group))})
    return components,jobs


def enumerate_job(job):
    import numpy as np
    masks=np.arange(job["start"],job["end"],dtype=np.uint32)
    bound=sum(abs(j) for u,v,j in job["edges"])+sum(abs(h) for h in job["fields"])
    dtype=np.int64 if bound <= (1<<62)-1 else object
    energy=np.zeros(len(masks),dtype=dtype)
    for u,v,j in job["edges"]:
        opposite=(((masks>>u)^(masks>>v))&1).astype(np.int64)
        energy+=(2*opposite-1)*j
    for u,h in enumerate(job["fields"]):
        if h:energy-=(2*((masks>>u)&1).astype(np.int64)-1)*h
    port_state=np.zeros(len(masks),dtype=np.uint32)
    for position,bit in job["ports"]:port_state|=((masks>>position)&1)<<bit
    counts=Counter((int(s),int(e)) for s,e in zip(port_state,energy))
    return job["group"],counts


def worker(cpu,jobs,connection):
    try:
        os.sched_setaffinity(0,{cpu})
        connection.send({"rows":[enumerate_job(job) for job in jobs],"cpu":cpu,"pid":os.getpid(),
                         "assignments":sum(job["end"]-job["start"] for job in jobs)})
    except BaseException as error:connection.send({"error":str(error)})
    finally:connection.close()


def convolve(a,b):
    result=Counter()
    for x,n in a.items():
        for y,m in b.items():result[x+y]+=n*m
    return result


def retained_spectrum(instance, ports=(), *, parallel=True):
    start=time.perf_counter();components,jobs=prepare(instance,ports)
    if parallel and len(jobs)>=14:
        if not set(H14F_CPUS)<=os.sched_getaffinity(0):raise ExactError("H14F affinity unavailable")
        context=mp.get_context("fork");processes=[];readers=[];shards=[]
        try:
            for i,cpu in enumerate(H14F_CPUS):
                reader,writer=context.Pipe(duplex=False)
                process=context.Process(target=worker,args=(cpu,jobs[i::14],writer));process.start();writer.close()
                processes.append(process);readers.append(reader)
            for reader in readers:
                if not reader.poll(120):raise RuntimeError("component worker did not finish")
                row=reader.recv()
                if "error" in row:raise RuntimeError(row["error"])
                shards.append(row)
        finally:
            for reader in readers:reader.close()
            for process in processes:
                process.join(5)
                if process.is_alive():process.terminate();process.join()
        results=[row for shard in shards for row in shard["rows"]]
    else:
        results=[enumerate_job(job) for job in jobs];shards=[]
    grouped=[Counter() for _ in components]
    for group,counter in results:grouped[group].update(counter)
    scalar=Counter({0:1});conditional=None
    for group,counts in zip(components,grouped):
        if set(group)&set(ports):
            conditional=[Counter({e:n for (s,e),n in counts.items() if s==state}) for state in range(1<<len(ports))]
        else:scalar=convolve(scalar,Counter({e:n for (s,e),n in counts.items()}))
    conditional=conditional or [Counter({0:1})]
    output=[convolve(row,scalar) for row in conditional]
    constant=integer(instance.get("constant",0))
    output=[Counter({e+constant:n for e,n in row.items()}) for row in output]
    total=Counter()
    for row in output:total.update(row)
    if sum(total.values())!=1<<instance["N"]:raise ExactError("source configuration count differs")
    def serialize(row):return [{"energy":e,"count":str(n)} for e,n in sorted(row.items())]
    mathematical=seal("SLC_EXACT_COMPONENT_CONDITIONAL_SPECTRUM_V1",source=instance,
        route="EXACT_COMPONENT_CONDITIONAL_CONVOLUTION",component_sizes=[len(c) for c in components],
        enumerated_assignments=sum(1<<len(c) for c in components),retained_ports=list(ports),
        port_rows=[serialize(row) for row in output],scalar_dos=serialize(total),
        configuration_count=str(sum(total.values())))
    return {"mathematical":mathematical,"execution":{"seconds":time.perf_counter()-start,
        "workers":[{k:v for k,v in row.items() if k!="rows"} for row in shards]}}
