from openai import OpenAI
from api_manager import get_api_key, set_api_key
import sys


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