#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import click
from openai import OpenAI
from api_manager import get_api_key, set_api_key
import sys

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

def find_file_in_tree():
    pass
def process_file():
    pass
def process_directory():
    pass

def cli():
    parser = argparse.ArgumentParser(prog='codemate', description='Codemate CLI: debug and refactor code')
    parser.add_argument('-r', '--refactor', action='store_true', help='Refactor the specified file (use with filename)')
    parser.add_argument('-c', '--config', action='store_true', dest='config', help='Set OpenRouter API Key (interactive)')
    parser.add_argument('filename', nargs='?', help='(optional) filename to debug/refactor (if omitted, debug current dir)')
    args = parser.parse_args()

    if args.config:
        key = input("Enter your OpenRouter API Key: ").strip()
        if not key:
            print("No API Key provided.")
            sys.exit(1)
        set_api_key(key)
        print("API Key saved. You can now run codemate commands.")
        return

    cwd = Path(os.getcwd())

    if args.filename:

        if not get_api_key():
            print("API Key not set. Run 'codemate -config' first.")
            sys.exit(1)

        candidate = None
        p = Path(args.filename)
        if p.exists():
            candidate = p.resolve()
        else:
            candidate = find_file_in_tree(args.filename, cwd)
        if not candidate:
            print(f"File '{args.filename}' not found in current repository (cwd: {cwd}).")
            sys.exit(1)

        if args.refactor:
            out = process_file(candidate, mode='refactor')
        else:
            out = process_file(candidate, mode='debug')
        print(out)
        return

    if not get_api_key():
        print("API Key not set. Run 'codemate -config' first.")
        sys.exit(1)
    out = process_directory(cwd, mode='debug')
    print(out)

if __name__ == '__main__':
    cli()