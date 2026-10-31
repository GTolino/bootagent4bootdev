import os

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs=os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    try:
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            MAX_CHARS = 10_000
            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                # After reading the first MAX_CHARS...
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string

    except Exception as e:
        return f"Error: Tool call failed {e}"
