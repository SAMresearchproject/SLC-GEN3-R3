"""Shared byte custody and serialization only; no receiver mathematics."""
from contextlib import contextmanager
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import re

CODE = Path(__file__).resolve().parent
CAMPAIGN = CODE.parents[1]
PROJECT = CAMPAIGN.parents[2]


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')


def text_new(path, value):
    with Path(path).open('x') as stream:
        stream.write(value)


def check_manifest(base, name, seal):
    manifest = base/name
    if sha(manifest) != seal['manifest_sha256']:
        raise ValueError('Manifest digest differs: '+str(manifest))
    seen = set()
    for line in manifest.read_text().splitlines():
        expected, relative = line.split('  ', 1)
        path = (base/relative).resolve()
        if relative in seen or not path.is_relative_to(base.resolve()):
            raise ValueError('Invalid manifest member: '+relative)
        if sha(path) != expected:
            raise ValueError('Artifact digest differs: '+relative)
        seen.add(relative)
    if len(seen) != seal['manifest_file_count']:
        raise ValueError('Manifest count differs')
    return len(seen)


def preflight():
    design = read(CAMPAIGN/'DESIGN_SEAL.json')
    code = read(CODE/'CODE_SEAL.json')
    if code['design_seal_sha256'] != sha(CAMPAIGN/'DESIGN_SEAL.json'):
        raise ValueError('Executor belongs to another design seal')
    return {
        'design_files': check_manifest(CAMPAIGN, 'SHA256SUMS', design),
        'code_files': check_manifest(CODE, 'SHA256SUMS', code),
        'design_seal_sha256': sha(CAMPAIGN/'DESIGN_SEAL.json'),
        'code_seal_sha256': sha(CODE/'CODE_SEAL.json'),
        'checked_utc': utc(), 'status': 'MATCH',
    }


def run_directory(run_id, independent=False):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', run_id):
        raise ValueError('Invalid run ID')
    parent = CAMPAIGN/'runs'
    parent.mkdir(exist_ok=True)
    path = parent/run_id
    if independent:
        if not path.is_dir():
            raise ValueError('Primary run does not exist')
        path = path/'independent'
    path.mkdir()
    return path


def manifest(directory, name):
    rows = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(directory.iterdir()) if p.is_file() and p.name != name]
    save(directory/name, {'created_utc': utc(), 'files': rows})


def verify_outputs(directory, name):
    rows = read(directory/name)['files']
    seen = set()
    for r in rows:
        p = (directory/r['path']).resolve()
        if not p.is_relative_to(directory.resolve()) or r['path'] in seen:
            raise ValueError('Invalid output manifest member')
        if p.stat().st_size != r['bytes'] or sha(p) != r['sha256']:
            raise ValueError('Output custody differs: '+r['path'])
        seen.add(r['path'])
    return len(rows)


@contextmanager
def ledger(path):
    with Path(path).open('xb') as raw:
        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0, compresslevel=3) as zipped:
            with io.TextIOWrapper(zipped, encoding='utf-8', newline='\n') as stream:
                yield lambda value: stream.write(json.dumps(value, sort_keys=True,
                                                           separators=(',', ':'), allow_nan=False)+'\n')


def ledger_rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            yield json.loads(line)


def fail(directory, error, manifest_name):
    save(directory/'FAILURE.json', {'recorded_utc': utc(), 'status': 'IMPLEMENTATION_OR_INTEGRITY_FAULT',
                                  'classification': None, 'error_type': type(error).__name__,
                                  'error': str(error)})
    manifest(directory, manifest_name)
