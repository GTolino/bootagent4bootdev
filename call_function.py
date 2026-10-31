import json
from collections.abc import Callable
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from prompts import *

available_functions = [
    schema_get_files_info, s_write_file, s_run_python_file, s_get_file_content
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info,
}


def _tool_message(tool_call, content: str) -> dict:
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": content,
    }


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name

    # The model writes the arguments as a JSON *string*; it can be malformed.
    # A failure here must go back to the model as a tool result, not crash the loop.
    try:
        function_args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError as e:
        print(f" - Calling function: {function_name}")
        return _tool_message(tool_call, f"Error: arguments were not valid JSON: {e}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return _tool_message(tool_call, f"Error: Unknown function: {function_name}")

    # Injected by the runtime, never chosen by the model (overwrites any value it sent).
    function_args["working_directory"] = "./calculator"

    # Missing/extra/wrongly-named arguments raise TypeError before the function body
    # (and its own try/except) ever runs — so the dispatch layer catches too.
    try:
        result = function_map[function_name](**function_args)
    except Exception as e:
        result = f"Error: calling {function_name} failed: {type(e).__name__}: {e}"

    # An empty result (empty dir, empty file) is a valid answer, but an empty string
    # tells the model nothing — say so explicitly.
    if not result:
        result = "(empty result: the tool ran successfully but returned no output)"

    return _tool_message(tool_call, result)
