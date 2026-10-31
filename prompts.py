system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

s_get_file_content =  {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Provides file content as string in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path as string in relation to the working directory ",
                },
            },
        },
    },
}

s_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python files",
        "parameters": {
            "type": "object",
            "required":["file_path"],
            "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path as string in relation to the working directory ",
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of command-line arguments to pass to the Python file"
                    }
                },
            },
        },
    }

s_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write or overwrite files",
        "parameters": {
            "type": "object",
            "required":["file_path","content"],
            "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path as string in relation to the working directory "},
                        "content": {
                            "type": "string",
                            "description": "content of the file path as string in relation to the working directory ",
                    },
                },
            },
        },
    }
