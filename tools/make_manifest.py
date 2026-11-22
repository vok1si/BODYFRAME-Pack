#!/usr/bin/env python3
"""Builds manifest.json for the BODYFRAME launcher from the jars in ./mods.

Usage:
  python tools/make_manifest.py --out manifest.json --urls assets.json
  python tools/make_manifest.py --out test-manifest.json --base http://127.0.0.1:8765/mods/

assets.json maps a file name to its download URL (e.g. GitHub release asset URLs).
Without it, --base + the URL-encoded file name is used.
"""
import argparse, hashlib, json, os, urllib.parse

ap = argparse.ArgumentParser()
ap.add_argument('--out', default='manifest.json')
ap.add_argument('--mods', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mods'))
ap.add_argument('--urls', help='JSON file: {"file.jar": "https://..."}')
ap.add_argument('--base', help='URL prefix used when --urls has no entry')
ap.add_argument('--minecraft', default='1.21.1')
ap.add_argument('--neoforge', default='21.1.267')
ap.add_argument('--revision', type=int, default=1)
a = ap.parse_args()

urls = json.load(open(a.urls, encoding='utf-8')) if a.urls else {}
files = []
for name in sorted(os.listdir(a.mods)):
    if not name.lower().endswith('.jar'):
        continue
    path = os.path.join(a.mods, name)
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    url = urls.get(name) or (a.base + urllib.parse.quote(name) if a.base else None)
    if not url:
        raise SystemExit('no URL for ' + name)
    files.append({'path': 'mods/' + name, 'size': os.path.getsize(path), 'sha256': h.hexdigest(), 'url': url})

manifest = {
    'schema': 1,
    'name': 'BODYFRAME',
    'revision': a.revision,
    'minecraft': a.minecraft,
    'neoforge': a.neoforge,
    'cleanDirs': ['mods'],
    'files': files,
}
with open(a.out, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print('wrote', a.out, len(files), 'files')
