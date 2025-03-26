from openai import OpenAI  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

qrok_api_key = os.getenv("QROK_API")  

try:
    # Initialize OpenAI client
    client = OpenAI(
        api_key=qrok_api_key,
        base_url="https://api.openai.com/v1"  
    )

    response = client.chat.completions.create(
        model="qrok-1",  #
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        stream=False
    )

    # Print the response from the API
    print(response.choices[0].message.content)

except Exception as e:
    print(f"Error: {e}")
