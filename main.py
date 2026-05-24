import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

client =  genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="CLI Chatbot powered by AI")
parser.add_argument("message", type=str, help="Message you'd like to send to the chatbot.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.message)])]

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
if not response.usage_metadata:
    raise RuntimeError("No usage metadata to process...")

if args.verbose:
    print(f"User prompt: {args.message}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
if response.function_calls is not None:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)