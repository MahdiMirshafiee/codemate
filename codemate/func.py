from pathlib import Path
import os

SUPPORTED_EXTENSIONS = (".c", ".cpp", ".h", ".hpp", ".cs", ".java", ".kt", ".go", ".rs", ".py", ".ipynb", ".r", ".jl",    ".pl", ".php", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".vue", ".dart", ".swift", ".rb", ".scala",
    ".html", ".htm", ".css", ".scss", ".json", ".yaml", ".yml", ".xml", ".md", ".sh", ".bash", ".bat",    ".cmd", ".ps1", ".dockerfile", ".gitignore", ".editorconfig", ".env", ".ini", ".toml", ".cfg",
    ".sql", ".exe", ".dll", ".so")

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
        return None, f"[bold gold3][!] Could not read file"
    return ("".join([f"{i+1}: {line}" for i, line in enumerate(lines)]), None) 


def list_dir_file(directory: Path):
    result = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(SUPPORTED_EXTENSIONS):
                result.append(os.path.join(root, f))
    return sorted(result)