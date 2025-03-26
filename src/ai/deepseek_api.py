from openai import OpenAI # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

deep_seek_api_key = os.getenv('DEEP-SEEK-API')

try:
    client = OpenAI(
    api_key=deep_seek_api_key,
    base_url="https://api.deepseek.com"
)

    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=False
)
    
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error: {e}")

