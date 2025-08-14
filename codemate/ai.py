from openai import OpenAI
from codemate.api_manager import get_api_key

def call_gpt(content, mode='debug'):
    apikey = get_api_key()
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