"""Bounded read-only retrieval of selected native objects from preserved archives.

This supplies custody records for explicit semantic admission. A matching content
hash alone does not make an archived object a spectral source or trained model.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tarfile


def retrieve(archive, hashes, *, max_scan_bytes=268435456, max_object_bytes=8388608):
    wanted = set(hashes)
    if not wanted or len(wanted) > 256 or any(not re.fullmatch('[0-9a-f]{64}', h) for h in wanted):
        raise ValueError('Supply 1..256 exact native object hashes')
    if type(max_scan_bytes) is not int or not 1 <= max_scan_bytes <= 1073741824:
        raise ValueError('Scan budget must be 1 byte..1 GiB')
    if type(max_object_bytes) is not int or not 1 <= max_object_bytes <= 67108864:
        raise ValueError('Object budget must be 1 byte..64 MiB')
    archive = Path(archive)
    proc = None
    records = {}
    scanned = 0
    reason = 'END_OF_ARCHIVE'
    raw = archive.open('rb')
    try:
        if archive.name.endswith('.zst'):
            proc = subprocess.Popen(['zstd','-q','-d','--long=27','-c'],stdin=raw,
                                    stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
            source = proc.stdout
        else:
            source = raw
        with tarfile.open(fileobj=source, mode='r|*') as tar:
            for member in tar:
                if member.offset_data + member.size > max_scan_bytes:
                    reason = 'SCAN_BUDGET_LIMITED'; break
                scanned = member.offset_data + member.size
                match = re.fullmatch(r'native/objects/([0-9a-f]{64})\.json',member.name)
                if match and match[1] in wanted:
                    if not member.isfile() or member.size > max_object_bytes:
                        raise ValueError('Selected object exceeds admission size or is not a regular file')
                    data = tar.extractfile(member).read()
                    if hashlib.sha256(data).hexdigest() != match[1]:
                        raise ValueError('Archived object content hash differs')
                    records[match[1]] = json.loads(data)
                    if wanted <= records.keys():
                        reason = 'SELECTED_OBJECTS_COMPLETE'; break
                tar.members.clear()
    finally:
        if proc:
            proc.stdout.close(); proc.terminate(); proc.wait()
        raw.close()
    return {'schema':'GEN3_ARCHIVE_FIXTURE_CAPTURE_V1','status':reason,
            'archive':str(archive),'scanned_uncompressed_bytes':scanned,
            'records':records,'missing':sorted(wanted-records.keys()),
            'semantic_admission':'REQUIRED_BEFORE_ENGINE_USE',
            'whole_archive_verified':False}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive');p.add_argument('hashes',nargs='+')
    p.add_argument('--max-scan-bytes',type=int,default=268435456)
    p.add_argument('--output',required=True)
    args=p.parse_args()
    result=retrieve(args.archive,args.hashes,max_scan_bytes=args.max_scan_bytes)
    with open(args.output,'x') as f:json.dump(result,f,indent=2);f.write('\n')
