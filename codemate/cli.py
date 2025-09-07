#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from codemate.api_manager import get_api_key, set_api_key, delete_config
import sys
from rich import print
from codemate.process import process_code_inline, process_directory, process_file
from codemate.func import find_file_in_tree

SUPPORTED_EXTENSIONS = (".c", ".cpp", ".h", ".hpp", ".cs", ".java", ".kt", ".go", ".rs", ".py", ".ipynb", ".r", ".jl",    ".pl", ".php", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".vue", ".dart", ".swift", ".rb", ".scala",
    ".html", ".htm", ".css", ".scss", ".json", ".yaml", ".yml", ".xml", ".md", ".sh", ".bash", ".bat",    ".cmd", ".ps1", ".dockerfile", ".gitignore", ".editorconfig", ".env", ".ini", ".toml", ".cfg",
    ".sql", ".exe", ".dll", ".so")

def cli():
    parser = argparse.ArgumentParser(prog='codemate', description='Codemate CLI: Ai Assistant for debug and refactor codes')
    parser.add_argument('-r', '--refactor', action='store_true', help='Refactor the specified file (use with filename)')
    parser.add_argument('-i', '--inline', help='Inline code OR use "-" to read code from stdin (e.g. codemate -i -)')
    parser.add_argument('filename', nargs='?', default=None, help='(optional) filename to debug/refactor (if omitted, debug current dir)')
    parser.add_argument('-c', '--config', action='store_true', dest='config', help='Set OpenRouter API Key')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete the codemate config directory (erase API key)')
    args = parser.parse_args()

    if args.config:
        token = get_api_key()
        if token :
            print("[bold gold3][!] API key is already set.")
            return
        key = input("Enter your OpenRouter API Key: ").strip()
        if not key:
            print("[bold gold3][!] No API Key provided.")
            sys.exit(1)
        set_api_key(key)
        print("[bold dark_green]API Key saved. You can now run codemate commands.")
        return
            
    if args.delete:
        delete_config()
        return
    
    cwd = Path(os.getcwd())

    if not get_api_key():
        print("[!] API Key not set. Run 'codemate --config' first.")
        sys.exit(1)

    if args.inline is not None:
        mode = 'refactor' if args.refactor else 'debug'

        if args.inline == '-':
            print("[bold cyan]Enter your code. Finish with Ctrl+D (Linux/macOS) or Ctrl+Z (Windows) then Enter:")
            code_str = sys.stdin.read()
            if not code_str:
                print("[bold gold3][!] No input received from stdin.")
                sys.exit(1)
        else:
            code_str = args.inline

        out = process_code_inline(code_str, mode=mode)
        print(f"──────────────────────────────────────────────────────────────────────────────────────────\n{out}\n──────────────────────────────────────────────────────────────────────────────────────────")        
        return

    if args.filename:
        candidate = None
        p = Path(args.filename)

        if not p.suffix or p.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print("[bold dark_red][!] File type not supported.")
            return None
    
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
        print(f"──────────────────────────────────────────────────────────────────────────────────────────\n{out}\n──────────────────────────────────────────────────────────────────────────────────────────")        
        return
    if args.refactor:
        print("[bold gold3] to refactor you should give a file name")
    else:
        out = process_directory(cwd, mode='debug')
        print(f"──────────────────────────────────────────────────────────────────────────────────────────\n{out}\n──────────────────────────────────────────────────────────────────────────────────────────")

if __name__ == '__main__':
    cli()