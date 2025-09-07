import sys
import os
from pathlib import Path
from codemate.ai import call_gpt
from codemate.func import list_dir_file , read_file_with_lines

def process_directory(directory: Path, mode='debug'):
    files = list_dir_file(directory)
    if not files:
        print("No code files found in directory.")
        sys.exit(1)
    combined = ""
    for f in files:
        numbered, err = read_file_with_lines(Path(f))
        if err:
            print(f"[!] Could not read file '{os.path.basename(f)}'")
            continue
        else:
            combined += f"{os.path.basename(f)}\n{numbered}\n{'-'*20}\n"
    return call_gpt(combined, mode)


def process_file(file_path: Path, mode='debug'):
    if not file_path.exists():
        print(f"[!] File not found: {file_path}")
        sys.exit(1)
    codetxt, err = read_file_with_lines(file_path)
    if err:
        print(err)
        sys.exit(1)
    payload = f"{file_path.name}\n{codetxt}"
    return call_gpt(payload, mode)

def process_code_inline(code_str: str, mode='debug'):
    try:
        lines = code_str.splitlines(keepends=True)
    except Exception as e:
        print("[bold gold3][!] Could not read inline code.")
        sys.exit(1)

    payload = "".join([f"{i+1}: {line}" for i, line in enumerate(lines)])
    return call_gpt(payload, mode)