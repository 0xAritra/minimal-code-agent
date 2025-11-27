import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content

func_mppng = {
    "get_files_info": get_files_info,
    "write_file": write_file,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
}

def call_function(function_call_part, verbose=False):

    if (verbose):
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args["working_dir"] = "./calculator"
    if function_name not in func_mppng:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )],
            )

    function_result = func_mppng[function_name](**function_args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )],
    )   

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    try:
        params = sys.argv[1:]
        flags = [flag[2:] for flag in params if flag.startswith("--")]
        args = [arg for arg in params if not arg.startswith("--")]
        if (len(args) < 1):
            raise Exception("Please add the prompt as argument")
        
        user_prompt = args[0]
    except Exception as e:
        print(e)
        sys.exit(1)
    
    system_prompt = """You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(function_declarations=[ schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file,  ])
    if (user_prompt):
        # Messages
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[ available_functions ], system_instruction=system_prompt))
        # print(response.text)
        # func_calls_str = ""
        function_call_responses = []
        is_verbose = False
        if ("verbose" in flags):
            is_verbose = True
        if (response.function_calls != None):
            for function_call_part in response.function_calls:
                # func_calls_str += f"Calling function: {function_call_part.name}({function_call_part.args})\n"
                function_call_result = call_function(function_call_part, verbose=is_verbose)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function Response missing")
                function_call_responses.append(function_call_result.parts[0])
                if is_verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}") 

        # if func_calls_str:
        #     print(func_calls_str)
        
        if ("verbose" in flags):
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
