import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "hello"}],
        model="openai/gpt-oss-120b"
    )
    print("SUCCESS")
    print(response.choices[0].message.content)
except Exception as e:
    print("ERROR")
    print(e)
