import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

funcs = {"get_files_info":get_files_info, "get_file_content":get_file_content, "write_file":write_file, "run_python_file":run_python_file}

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = sys.argv[1]
    model_name = "gemini-2.0-flash-001"
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    available_functions = types.Tool(function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file])
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    
    
    
    verbose = False
    for arg in sys.argv:
        if arg == "--verbose":
            verbose = True

    iterations = 1
    while iterations <= 20:
        iterations += 1
        
        try:
            response = client.models.generate_content(model=model_name, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        except Exception as e:
            print("Invalid argument passed.\nPlease use the format: 'uv run main.py response' where response is a string")
            sys.exit(1)

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls != None:
            for function_call in response.function_calls:
                func_result = call_function(function_call, verbose)
                if func_result.parts[0].function_response.response != None:
                    if verbose:
                        print(f"-> {func_result.parts[0].function_response.response}")
                else:
                    raise Exception("FATAL ERROR")
                messages.append(func_result)
        elif response.text != None:
            if verbose:
                print(f"User prompt: {user_prompt}\n\n{response.text}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
            else:
                print(response.text)
            break

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    if function_call_part.name in funcs:
        function_call_part.args["working_directory"] = "calculator"
        func_result = funcs[function_call_part.name](**function_call_part.args)
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call_part.name, response={"result": func_result})],)
    else:
        return types.Content(role="tool", parts=[types.Part.from_function_response(name=function_call_part.name, response={"error": f"Unknown function: {function_call_part.name}"})],)
    

if __name__ == "__main__":
    main()
