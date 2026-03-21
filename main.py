import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found!")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], 
                                       system_instruction=system_prompt,
                                        temperature=0
                                        )
)
if response.usage_metadata is None:
    raise RuntimeError("API request failed!")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

function_results = []

if response.function_calls:
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)

        if not function_call_result.parts:
            raise RuntimeError("Function call returned no parts")

        function_response = function_call_result.parts[0].function_response
        if function_response is None:
            raise RuntimeError("Function call returned no function response")

        if function_response.response is None:
            raise RuntimeError("Function call returned no response payload")

        function_results.append(function_call_result.parts[0])

        if args.verbose:
            print(f"-> {function_response.response}")
else:
    print(f"Response: {response.text}")
