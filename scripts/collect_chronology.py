#!/usr/bin/env python3
"""
Collect file modification chronology (by mtime) while excluding markdown files and common large dirs.

Usage:
  python scripts\collect_chronology.py --root . --output chronology.json --top 50

Produces JSON (list of {path, mtime, mtime_iso, size}) sorted by newest first. Also optionally writes CSV if --csv is given.
"""
import argparse
import os
import sys
import json
import datetime
from typing import List


def parse_args():
    p = argparse.ArgumentParser(description="Collect file modification chronology (by mtime)")
    p.add_argument('--root', default=os.getcwd(), help='Repository root to scan')
    p.add_argument('--output', default='chronology.json', help='Output JSON path')
    p.add_argument('--csv', default=None, help='Optional CSV output path')
    p.add_argument('--top', type=int, default=50, help='How many top files to print')
    p.add_argument('--extensions', default='py,c,cpp,h,hh,hpp,ll,rs,go,java,js,ts,json,toml,ini,txt,csv,sh,ps1,yaml,yml,cmake,mak,md',
                   help='Comma-separated whitelist of file extensions to include (md will be excluded by default post-filter)')
    p.add_argument('--exclude-dirs', default='.git,venv,env,__pycache__,models,runs,results,data,dataset,logs,tmp',
                   help='Comma-separated list of directories to skip')
    return p.parse_args()


def main():
    args = parse_args()
    root = os.path.abspath(args.root)
    exts = [e.strip().lower() for e in args.extensions.split(',') if e.strip()]
    # explicitly exclude markdown from results regardless
    if 'md' in exts:
        exts.remove('md')
    exclude_dirs = set(d.strip() for d in args.exclude_dirs.split(',') if d.strip())

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs and not d.startswith('.')]
        for fn in filenames:
            # skip hidden files
            if fn.startswith('.'):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            # use extension whitelist if provided
            if '.' in fn:
                ext = fn.rsplit('.', 1)[1].lower()
            else:
                ext = ''
            if exts and ext not in exts:
                continue
            try:
                st = os.stat(full)
            except OSError:
                continue
            mtime = st.st_mtime
            size = st.st_size
            files.append({
                'path': rel.replace(os.sep, '\\'),
                'mtime': mtime,
                'mtime_iso': datetime.datetime.utcfromtimestamp(mtime).replace(microsecond=0).isoformat() + 'Z',
                'size': size,
            })

    files.sort(key=lambda x: x['mtime'], reverse=True)

    out_json = os.path.abspath(args.output)
    try:
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump({'generated_at': datetime.datetime.utcnow().isoformat() + 'Z', 'root': root, 'files': files}, f, indent=2)
    except Exception as e:
        print('Failed to write JSON:', e, file=sys.stderr)
        sys.exit(2)

    if args.csv:
        try:
            import csv
            with open(args.csv, 'w', newline='', encoding='utf-8') as cf:
                writer = csv.writer(cf)
                writer.writerow(['path', 'mtime_iso', 'size'])
                for item in files:
                    writer.writerow([item['path'], item['mtime_iso'], item['size']])
        except Exception as e:
            print('Failed to write CSV:', e, file=sys.stderr)

    top = args.top
    print(f"Found {len(files)} files (filtered). Top {top} by mtime:")
    for item in files[:top]:
        print(f"{item['mtime_iso']}  {item['path']}  {item['size']} bytes")

    print('\nWrote chronology to', out_json)
    return 0


if __name__ == '__main__':
    sys.exit(main())
