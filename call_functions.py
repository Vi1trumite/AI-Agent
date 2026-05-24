from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, 
                           schema_get_files_content,
                           schema_run_python_file,
                           schema_write_file],
)


def call_function(
        function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")