import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found!")

user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt
)
if response.usage_metadata == None:
    raise RuntimeError("API request failed!")
print(f"User prompt: {user_prompt}")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Response: {response.text}")

