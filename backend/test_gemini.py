from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"API Key starts with: {api_key[:10] if api_key else 'None'}")

try:
    client = genai.Client(api_key=api_key)
    models = client.models.list()
    print("Available flash models:")
    for m in models:
        if "flash" in m.name:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
