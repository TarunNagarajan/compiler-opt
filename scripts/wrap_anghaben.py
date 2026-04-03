"""
Wrap AnghaBench/TheAlgorithms-style C files with standalone main() wrappers.

These files are LeetCode-style solutions with no main() function.
We add a minimal main() that calls the primary function with dummy args,
plus any missing #include directives, making them compilable as
standalone LLVM IR for the RL training pipeline.
"""

import re
import os
from pathlib import Path

SOURCE_DIR = Path("benchmarks/large_scale/anghaben")
OUTPUT_DIR = Path("benchmarks/large_scale/anghaben_wrapped")


def find_function_signatures(code):
    """Extract top-level function signatures from C code."""
    # Match function definitions (not declarations/prototypes)
    pattern = r'^(\w[\w\s\*]*?)\s+(\w+)\s*\(([^)]*)\)\s*\{'
    matches = re.finditer(pattern, code, re.MULTILINE)
    funcs = []
    for m in matches:
        ret_type = m.group(1).strip()
        name = m.group(2).strip()
        params = m.group(3).strip()
        # Skip if it's already main
        if name == 'main':
            continue
        funcs.append((ret_type, name, params))
    return funcs


def generate_dummy_arg(param_str):
    """Generate a dummy argument for a given C parameter type."""
    param_str = param_str.strip()
    if not param_str or param_str == 'void':
        return None

    # Remove parameter name (last word)
    parts = param_str.rsplit(None, 1)
    if len(parts) == 1:
        type_str = parts[0]
    else:
        type_str = parts[0]
        # Check if last part is actually part of the type
        if parts[1] in ('*', '**', 'int', 'char', 'float', 'double', 'long', 'unsigned', 'void'):
            type_str = param_str

    type_str = type_str.strip()

    if '**' in type_str or '* *' in type_str:
        return 'NULL'
    elif '*' in type_str:
        if 'char' in type_str:
            return '"test"'
        else:
            return 'NULL'
    elif 'float' in type_str:
        return '1.0f'
    elif 'double' in type_str:
        return '1.0'
    elif 'bool' in type_str:
        return 'true'
    elif 'long long' in type_str:
        return '42LL'
    elif 'long' in type_str:
        return '42L'
    elif 'unsigned' in type_str:
        return '42u'
    elif 'int' in type_str or 'size' in type_str:
        return '42'
    elif 'char' in type_str:
        return "'x'"
    else:
        return '0'


def generate_call_args(params_str):
    """Generate dummy arguments for a function call."""
    if not params_str or params_str.strip() == 'void':
        return ''

    params = []
    depth = 0
    current = ''
    for ch in params_str:
        if ch == ',' and depth == 0:
            params.append(current)
            current = ''
        else:
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1
            current += ch
    if current.strip():
        params.append(current)

    args = []
    for p in params:
        arg = generate_dummy_arg(p)
        if arg is not None:
            args.append(arg)
    return ', '.join(args)


def wrap_file(source_path):
    """Read a C file, add includes + main() wrapper, return wrapped code."""
    with open(source_path, 'r', errors='replace') as f:
        code = f.read()

    # Skip files that already have main()
    if re.search(r'\bint\s+main\s*\(', code):
        return code

    funcs = find_function_signatures(code)
    if not funcs:
        return None  # Can't wrap — no functions found

    # Pick the "primary" function (first non-helper, or just the first one)
    primary = funcs[0]
    ret_type, name, params = primary

    # Build includes block (add common ones if missing)
    includes = set()
    if '#include <stdio.h>' not in code:
        includes.add('#include <stdio.h>')
    if '#include <stdlib.h>' not in code:
        includes.add('#include <stdlib.h>')
    if '#include <string.h>' not in code:
        includes.add('#include <string.h>')
    if '#include <stdbool.h>' not in code and 'bool' in code:
        includes.add('#include <stdbool.h>')
    if '#include <math.h>' not in code and ('ceil' in code or 'floor' in code or 'sqrt' in code
                                             or 'log' in code or 'pow' in code or 'fabs' in code):
        includes.add('#include <math.h>')
    if '#include <limits.h>' not in code and ('INT_MAX' in code or 'INT_MIN' in code):
        includes.add('#include <limits.h>')

    includes_str = '\n'.join(sorted(includes))

    # Generate the call
    call_args = generate_call_args(params)

    # Build main that calls primary function and sinks the result
    if ret_type == 'void':
        call_line = f'    {name}({call_args});'
        sink_line = '    volatile int _sink = 0; (void)_sink;'
    else:
        call_line = f'    {ret_type} _result = {name}({call_args});'
        sink_line = '    volatile int _sink = (int)(long long)_result; (void)_sink;'
        if '*' in ret_type:
            sink_line = '    volatile long long _sink = (long long)_result; (void)_sink;'

    main_block = f"""

/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {{
{call_line}
{sink_line}
    return 0;
}}
"""

    wrapped = ''
    if includes_str:
        wrapped += includes_str + '\n'
    wrapped += code
    wrapped += main_block

    return wrapped


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    wrapped = 0
    skipped = 0

    for source_file in sorted(SOURCE_DIR.glob("*.c")):
        total += 1
        result = wrap_file(source_file)
        if result is None:
            skipped += 1
            continue

        output_path = OUTPUT_DIR / source_file.name
        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(result)
        wrapped += 1

    print(f"[WRAP] Processed {total} files: {wrapped} wrapped, {skipped} skipped (no functions found)")
    print(f"[WRAP] Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
