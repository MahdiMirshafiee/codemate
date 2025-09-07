from openai import OpenAI
from codemate.api_manager import get_api_key
import sys

def call_gpt(content, mode='debug'):
    apikey = get_api_key()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=apikey
    )

    if mode == 'debug': 
        try:
            completion = client.chat.completions.create(
                model="openai/GPT-4o",
                messages=[
                {
                    "role": "system",
                    "content": """
You are an AI code debugging assistant. Your task is to analyze one or more provided source code files and identify all possible bugs, errors, or problematic patterns. You must check for all potential issues, including but not limited to:
- Syntax errors
- Logical errors
- Runtime errors
- API misuse
- Performance issues
- Security vulnerabilities
- Incorrect variable usage or scope issues
- Edge case handling
- Language-specific pitfalls

Output format:
For each detected bug, output exactly in the following structure:

filename : (line X OR line A-B)
Bug: concise description of the bug
solution: concise suggestion on how to fix the bug

Where:
- `filename` is the exact name of the file.
- `X` is the line number where the bug occurs.
- For multi-line issues use 'line A-B'.
- `Bug` is a clear and concise description of the bug.
- `solution` is a short, practical explanation of how to fix it.

Rules:
- If multiple bugs exist, list them all using the same structure, one after another.
- If NO bugs are found for a file or files, output: exactly “No Bug Found!”
- Do NOT output anything outside the defined format.
- Do NOT include explanations, greetings, or additional text outside the required output.
- Ensure all possible bugs are checked before responding.
                    """
                },
                {
                    "role": "user",
                    "content": f"source code:\n{content}"
                }
                ],
                temperature=0,
                max_tokens=1500,
            )
        except Exception as e:
            print("An error occurred: ", e)
            sys.exit(1)
    else:  
        try: 
            completion = client.chat.completions.create(
                model="openai/GPT-4o",
                messages=[
                {
                    "role": "system",
                    "content": """
You are an AI code refactoring assistant. Your task is to analyze one or more provided source code files and identify all important and necessary refactor opportunities that would significantly improve code quality, maintainability, readability, or performance.

Rules:
- Only suggest refactors that are important and necessary (avoid nitpicks or purely stylistic changes unless they have a meaningful impact).
- For each detected refactor opportunity, output exactly in the following structure:

filename : (line X OR line A-B)
suggestion: rafactor sulotion

Where:
- `filename` is the exact name of the file.
- `X` is the line number where the refactor is needed.
- For multi-line issues use 'line A-B'.
- `suggestion` should be a short, clear, and practical explanation of the recommended refactor.

- If multiple refactors are needed, list them all in the above format, separated by a blank line.
- If NO important refactors are found, output exactly: "Everything Is Alright!"
- Do NOT output anything outside the defined format.
- Do NOT include explanations, greetings, or additional text outside the required output.
- Carefully check for:
    - Duplicate or redundant code
    - Poor variable naming impacting clarity
    - Long or overly complex functions that should be broken down
    - Repeated logic that should be extracted into reusable functions
    - Inefficient loops or algorithms
    - Poorly structured conditionals
    - Hardcoded values that should be constants/configurable
    - Inconsistent code style affecting readability
    - Code that could leverage built-in language features or standard libraries for better performance or clarity
                    """
                },
                {
                    "role": "user",
                    "content": f"source code:\n{content}"
                }
                ],
                temperature=0,
                max_tokens=1500,
            )
        except Exception as e:
            print("An error occurred: ", e)
            sys.exit(1)

    return completion.choices[0].message.content