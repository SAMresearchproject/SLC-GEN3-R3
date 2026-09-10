#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check volume files, chapter identity and local Markdown destinations."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)')

def main():
    manifest = json.loads((ROOT/'maintenance/MIGRATION.json').read_text())
    errors = []
    for volume in ['vol_i','vol_ii','vol_iii','vol_iv']:
        if not (ROOT/volume/'README.md').is_file():
            errors.append('Missing volume: '+volume)
    chapter_sources = [r['source_path'] for r in manifest['chapters']]
    chapter_paths = [r['path'] for r in manifest['chapters']]
    if len(set(chapter_sources)) != len(chapter_sources) or len(set(chapter_paths)) != len(chapter_paths):
        errors.append('Duplicate chapter source or destination')
    for row in manifest['chapters']:
        p = ROOT/row['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
            errors.append('Chapter changed since migration: '+row['path'])
    for row in manifest['branch_test_assignments']:
        p = ROOT/row['path']
        if not p.is_file() or row['record_key'] not in p.read_text():
            errors.append('Missing assigned test: '+row['path'])
    checked_links = 0
    for p in ROOT.rglob('*.md'):
        if p.relative_to(ROOT).parts[0] == 'courtroom':
            continue  # Immutable source artifacts: checked by check_courtroom_mirror.py.
        for raw in LINK.findall(p.read_text()):
            target = raw.strip('<>').split('#')[0]
            if not target or '://' in target or target.startswith('mailto:'):
                continue
            checked_links += 1
            if not (p.parent/unquote(target)).exists():
                errors.append(str(p.relative_to(ROOT))+': missing '+target)
    result = {'status':'FAIL' if errors else 'PASS','chapters':len(chapter_paths),
              'branch_test_assignments':len(manifest['branch_test_assignments']),
              'local_links_checked':checked_links,'errors':errors}
    print(json.dumps(result,indent=2))
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
