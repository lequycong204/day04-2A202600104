import os
from dotenv import load_dotenv
load_dotenv()
public_url = os.getenv("PUBLIC_URL")

from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=f"{public_url}/v1",
)

response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"},
    ]
)

print(response.choices[0].message.content)