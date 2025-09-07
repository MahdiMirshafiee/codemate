# codemate
An AI-powered CLI tool that helps developers debug and refactor their code efficiently. Using OpenRouter's GPT-4o API, it analyzes source code files to identify bugs, suggest fixes, and recommend refactoring improvements across multiple programming languages.

# Features
- Smart Debugging: Automatically detect syntax errors, logical errors, runtime issues, and security vulnerabilities
- Code Refactoring: Get intelligent suggestions to improve code quality, maintainability, and performance
- Multi-file Analysis: Process entire directories or single files
- Inline Code Support: Analyze code snippets directly from command line or stdin
- Wide Language Support: Supports 40+ programming languages and file types
- Fast & Efficient: Powered by GPT-4o through OpenRouter API

# Installation
### From PyPI (Recommended)
```bash
pip install codesmate
```
### From Source
```bash
git clone https://github.com/MahdiMirshafiee/codemate.git
cd codemate
pip install .
```

# Setup
Before using codemate, you need to configure your OpenRouter API key:
1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Configure codemate with your API key:
```bash
codemate --config
```
You'll be prompted to enter your OpenRouter API key. This will be stored in `~/.codemate/config.json` .

# Usage
### Debug Current Directory
Analyze all supported files in the current directory for bugs:
```bash
codemate
```
### Debug Specific File
```bash
codemate filename.py
codemate src/main.js
```
### Refactor Code
Get refactoring suggestions for a specific file:
```bash
codemate -r filename.py
codemate --refactor src/component.jsx
```
### Inline Code Analysis
Analyze code directly from command line:
```bash
codemate -i "def hello(): print('Hello World')"
```
Read code from stdin:
```bash
cat myfile.py | codemate -i -
# or
codemate -i -
# Then paste your code and press Ctrl+D (Linux/macOS) or Ctrl+Z+Enter (Windows)
```

# Configuration Management
### Set API Key
```bash
codemate --config
```
### Delete Configuration
Remove stored API key and configuration:
```bash
codemate --delete
```

# Help
To see all available options:
```bash
codemate --help
```
This will display:
```bash
usage: codemate [-h] [-r] [-i INLINE] [-c] [-d] [filename]

Codemate CLI: AI Assistant for debug and refactor codes

positional arguments:
  filename              (optional) filename to debug/refactor (if omitted, debug current dir)

options:
  -h, --help            show this help message and exit
  -r, --refactor        Refactor the specified file (use with filename)
  -i INLINE, --inline INLINE
                        Inline code OR use "-" to read code from stdin
  -c, --config          Set OpenRouter API Key
  -d, --delete          Delete the codemate config directory (erase API key)
```

# Examples
<details>
<summary>Debug a Python File</summary>

![Debug a Python File](https://raw.githubusercontent.com/MahdiMirshafiee/codemate/main/pics/debug.png)
</details>

<details>
<summary>Refactor a JavaScript File</summary>

![Refactor a JavaScript File](https://raw.githubusercontent.com/MahdiMirshafiee/codemate/main/pics/refactor.png)
</details>

<details>
<summary>Inline Code Analysis</summary>

![Inline Code Analysis](https://raw.githubusercontent.com/MahdiMirshafiee/codemate/main/pics/inline.png)
</details>

# Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

For major changes, please open an issue first to discuss what you would like to change.

# License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

# Authors
- [Mahdi Mirshafiee](https://github.com/MahdiMirshafiee)
- [Saleh Mirshafiee](https://github.com/SalehMirshafiee)

**Made with ❤️ for developers by developers**