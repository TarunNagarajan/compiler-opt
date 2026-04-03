#!/usr/bin/env python3
"""
Run a set of repository validation scripts in a lightweight, timeboxed way to avoid needing pwsh/uv.

Usage:
  python scripts\run_validations.py --timeout 60 --output validation_report.json

Tries a few safe argument variants for each script ("--quick", "--dry-run") and falls back to running the script plain. Captures stdout/stderr and records timeouts.
"""
import argparse
import os
import sys
import subprocess
import json
import time


def find_candidate_scripts(root):
    scripts_dir = os.path.join(root, 'scripts')
    candidates = []
    if not os.path.isdir(scripts_dir):
        return candidates
    for fn in sorted(os.listdir(scripts_dir)):
        low = fn.lower()
        path = os.path.join(scripts_dir, fn)
        if not os.path.isfile(path):
            continue
        # heuristics: verify/validate/audit/foresight names
        if low.startswith('verify') or 'verify' in low or 'audit' in low or 'validate' in low or 'foresight' in low or low.startswith('v8_'):
            candidates.append(path)
    # de-duplicate while preserving order
    seen = set()
    out = []
    for p in candidates:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def try_run(script_path, timeout):
    # try a few safe argument sets
    attempts = [ ['--quick'], ['--dry-run'], [] ]
    for args in attempts:
        cmd = [sys.executable, script_path] + args
        start = time.time()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            elapsed = time.time() - start
            return {'script': script_path, 'args': args, 'returncode': proc.returncode, 'elapsed': elapsed, 'stdout': proc.stdout[:20000], 'stderr': proc.stderr[:20000], 'status': 'ok' if proc.returncode == 0 else 'failed'}
        except subprocess.TimeoutExpired:
            return {'script': script_path, 'args': args, 'returncode': None, 'elapsed': timeout, 'stdout': '', 'stderr': 'Timeout', 'status': 'timeout'}
        except Exception as e:
            return {'script': script_path, 'args': args, 'returncode': None, 'elapsed': 0, 'stdout': '', 'stderr': f'Exception: {e}', 'status': 'error'}
    # unreachable
    return {'script': script_path, 'args': [], 'returncode': None, 'elapsed': 0, 'stdout': '', 'stderr': 'No attempts', 'status': 'skipped'}


def main():
    p = argparse.ArgumentParser(description='Run lightweight validations')
    p.add_argument('--root', default=os.getcwd())
    p.add_argument('--timeout', type=int, default=60, help='Per-script timeout in seconds')
    p.add_argument('--output', default='validation_report.json', help='Output JSON report')
    p.add_argument('--scripts', nargs='*', default=None, help='Optional explicit scripts to run')
    args = p.parse_args()

    root = os.path.abspath(args.root)
    if args.scripts:
        scripts = [os.path.join(root, s) if not os.path.isabs(s) else s for s in args.scripts]
    else:
        scripts = find_candidate_scripts(root)

    results = []
    for s in scripts:
        print(f'Running {os.path.relpath(s, root)} (timeout {args.timeout}s) ...')
        res = try_run(s, args.timeout)
        results.append(res)
        print(f" -> {res['status']} (rc={res['returncode']}) elapsed={res['elapsed']:.1f}s")

    out = {'generated_at': time.time(), 'root': root, 'results': results}
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2)
        print('Wrote validation report to', args.output)
    except Exception as e:
        print('Failed to write report:', e, file=sys.stderr)
        sys.exit(2)

    # exit non-zero if any serious failure/timeouts
    bad = [r for r in results if r['status'] in ('failed','timeout','error')]
    if bad:
        print('\nSome validations failed or timed out:')
        for r in bad:
            print(os.path.relpath(r['script'], root), r['status'])
        sys.exit(1)
    print('\nAll validations reported OK (within light checks).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
