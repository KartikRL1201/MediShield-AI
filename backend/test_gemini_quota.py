from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

try:
    client = genai.Client(api_key=api_key)
    print("Testing gemini-flash-latest...")
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents="Say hello"
    )
    print("Success! Response:", response.text)
except Exception as e:
    print(f"Error: {e}")
