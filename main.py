import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function



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

if args.verbose:
    print(f"User prompt: {args.message}")

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    if not response.usage_metadata:
        raise RuntimeError("No usage metadata to process...")

    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls is not None:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise Exception("No parts in result")
            if function_call_result.parts[0].function_response == None:
                raise Exception("Should have a function response object")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Should have a function result")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print(response.text)
        break
else:
    print("Max iterations reached. Unable to retrieve data.")
    sys.exit(1)