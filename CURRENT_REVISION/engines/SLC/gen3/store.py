"""Content-addressed immutable chunks with atomic authenticated checkpoint roots.

Hashes establish byte identity. Only roots authenticated by the local custody
key may bypass semantic replay. The key is never part of exported object closure.
"""
import fcntl
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import shutil
from ..gen2.exact import canonical_bytes


def sync_dir(path):
    fd = os.open(path, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic(path, data, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.' + secrets.token_hex(8))
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        os.replace(tmp, path); sync_dir(path.parent)
    finally:
        tmp.unlink(missing_ok=True)


class Store:
    def __init__(self, root, binding, *, reserve_bytes=0):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = (self.root / 'writer.lock').open('a')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock.close()
            raise ValueError('R3 store already has an active state writer') from None
        self.binding = binding
        self.reserve = reserve_bytes
        self.objects = self.root / 'objects'; self.objects.mkdir(exist_ok=True)
        keyfile = self.root / 'custody.key'
        if not keyfile.exists():
            atomic(keyfile, secrets.token_bytes(32))
        self.key = keyfile.read_bytes()
        self.written_bytes = self.written_objects = self.read_objects = 0
        self.verified = set()

    def put(self, value):
        data = canonical_bytes(value)
        ref = hashlib.sha256(data).hexdigest()
        path = self.path(ref)
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError('Immutable object identity collision or corruption')
        else:
            if shutil.disk_usage(self.root).free - len(data) < self.reserve:
                raise ValueError('Checkpoint admission would cross the disk free-space reserve')
            atomic(path, data)
            self.written_bytes += len(data); self.written_objects += 1
        self.verified.add(ref)
        return ref

    def path(self, ref):
        if not isinstance(ref, str) or re.fullmatch('[0-9a-f]{64}', ref) is None:
            raise ValueError('Invalid immutable object reference')
        return self.objects / ref[:2] / ref[2:]

    def get(self, ref):
        data = self.path(ref).read_bytes()
        if hashlib.sha256(data).hexdigest() != ref:
            raise ValueError('Immutable object content differs from its reference')
        self.read_objects += 1
        self.verified.add(ref)
        return json.loads(data)

    def commit(self, snapshot, closure):
        root = self.put({'schema': 'GEN3_UNIFIED_CHECKPOINT_V1', 'binding': self.binding,
                         'snapshot': snapshot, 'closure': sorted(set(closure))})
        # The complete closure must exist and authenticate before publishing.
        for ref in self.get(root)['closure']:
            if ref not in self.verified:
                self.get(ref)
        receipt = {'root': root, 'binding': self.binding}
        receipt['authentication'] = hmac.new(self.key, canonical_bytes(receipt), 'sha256').hexdigest()
        atomic(self.root / 'roots' / (root + '.json'), canonical_bytes(receipt))
        atomic(self.root / 'HEAD.json', canonical_bytes(receipt))
        return {'schema': 'GEN3_CHECKPOINT_REFERENCE_V1', 'root': root,
                'binding': self.binding, 'local_durable': True, 'replicated': False}

    def restore(self, root=None):
        if root is not None:
            self.path(root)  # Validate the reference before constructing a path.
        path = self.root / 'HEAD.json' if root is None else self.root / 'roots' / (root + '.json')
        receipt = json.loads(path.read_text())
        auth = receipt.pop('authentication')
        if not hmac.compare_digest(auth, hmac.new(self.key, canonical_bytes(receipt), 'sha256').hexdigest()):
            raise ValueError('Untrusted checkpoint root: semantic import is required')
        if receipt['binding'] != self.binding:
            raise ValueError('Checkpoint implementation/source generation differs; semantic import is required')
        row = self.get(receipt['root'])
        if row['binding'] != self.binding:
            raise ValueError('Checkpoint binding differs from its authenticated root')
        for ref in row['closure']:
            self.get(ref)
        return row['snapshot']

    def close(self):
        if not self.lock.closed:
            fcntl.flock(self.lock, fcntl.LOCK_UN); self.lock.close()
