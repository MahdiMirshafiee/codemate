#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from openai import OpenAI
from api_manager import get_api_key, set_api_key, delete_config
import sys
from rich import print


SUPPORTED_EXTENSIONS = ('.py', '.js', '.go', '.java')

def call_gpt(content, mode='debug'):
    apikey = get_api_key()
    if not apikey:
        print("API Key not set. Please run 'codemate config'")
        sys.exit(1)
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = apikey
    )

    completion = client.chat.completions.create(
    model="openai/GPT-4o",
    messages=[
{
        "role": "system",
        "content": """
        """},        
{
        "role": "user",
        "content": """
        """
}
    ],
    temperature=0,
    max_tokens=1500,
)

    return completion.choices[0].message.content

def process_code_inline(code_str: str, mode='debug'):
    try:
        lines = code_str.splitlines(keepends=True)
    except Exception as e:
        print(f"[!] __ERROR_READING_INLINE_CODE__: {e}")
        sys.exit(1)

    payload = "".join([f"{i+1}: {line}" for i, line in enumerate(lines)])
    # return call_gpt(payload, mode)
    return (payload)

def find_file_in_tree(filename: str, root: Path):
    fileName = Path(filename)
    if fileName.exists():
        return fileName.resolve()
    matches = [p for p in root.rglob('*') if p.is_file() and p.name.lower() == filename.lower()]
    if len(matches) == 1:
        return matches[0].resolve()
    if len(matches) > 1:
        matches.sort(key=lambda p: len(str(p)))
        return matches[0].resolve()
    partials = [p for p in root.rglob('*') if p.is_file() and filename.lower() in p.name.lower()]
    if partials:
        partials.sort(key=lambda p: len(str(p)))
        return partials[0].resolve()
    return None

def read_file_with_lines(path: Path):
    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        return None, f"[!] __ERROR_READING_FILE__: {e}"
    return ("".join([f"{i+1}: {line}" for i, line in enumerate(lines)]), None) 

def process_file(file_path: Path, mode='debug'):
    if not file_path.exists():
        print(f"[!] File not found: {file_path}")
        sys.exit(1)
    codetxt, err = read_file_with_lines(file_path)
    if err:
        print(err)
        sys.exit(1)
    payload = f"{file_path.name}\n{codetxt}"
    # return call_gpt(payload, mode)
    return (payload)


def list_dir_file(directory: Path):
    result = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(SUPPORTED_EXTENSIONS):
                result.append(os.path.join(root, f))
    return sorted(result)


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
    return (combined)
    # return call_gpt(combined, mode)

def cli():
    parser = argparse.ArgumentParser(prog='codemate', description='Codemate CLI: Ai Assistant for debug and refactor codes')
    parser.add_argument('-r', '--refactor', action='store_true', help='Refactor the specified file (use with filename)')
    parser.add_argument('-c', '--config', action='store_true', dest='config', help='Set OpenRouter API Key')
    parser.add_argument('-i', '--inline', help='Inline code OR use "-" to read code from stdin (e.g. codemate -i -)')
    parser.add_argument('filename', nargs='?', default=None, help='(optional) filename to debug/refactor (if omitted, debug current dir)')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete the codemate config directory (erase API key)')
    args = parser.parse_args()

    # if args.config:
    #     key = input("Enter your OpenRouter API Key: ").strip()
    #     if not key:
    #         print("[!] No API Key provided.")
    #         sys.exit(1)
    #     set_api_key(key)
    #     print("[bold green]API Key saved. You can now run codemate commands.")
    #     return
            
    if args.delete:
        delete_config()
        return
    
    cwd = Path(os.getcwd())

    # if not get_api_key():
    #     print("[!] API Key not set. Run 'codemate -config' first.")
    #     sys.exit(1)

    if args.inline is not None:
        mode = 'refactor' if args.refactor else 'debug'

        if args.inline == '-':
            print("[bold green]Paste your code. Finish with Ctrl+D (Linux/macOS) or Ctrl+Z (Windows) then Enter:")
            code_str = sys.stdin.read()
            if not code_str:
                print("[!] No input received from stdin. Exiting.")
                sys.exit(1)
        else:
            code_str = args.inline

        out = process_code_inline(code_str, mode=mode)
        print(out)
        return

    if args.filename:
        candidate = None
        p = Path(args.filename)
        if p.exists():
            candidate = p.resolve()
        else:
            candidate = find_file_in_tree(args.filename, cwd)
        if not candidate:
            print(f"[!] File '{args.filename}' not found in current repository (cwd: {cwd}).")
            sys.exit(1)

        if args.refactor:
            out = process_file(candidate, mode='refactor')
        else:
            out = process_file(candidate, mode='debug')
        print(out)
        return
    if args.refactor:
        print("[bold yellow] for refactor you should give me a file name")
    else:
        out = process_directory(cwd, mode='debug')
        print(out)

if __name__ == '__main__':
    cli()