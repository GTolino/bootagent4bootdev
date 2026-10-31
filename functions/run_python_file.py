import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs=os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    try:
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif target_file[-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_file]
            if args != None:
                command.extend(args)
            returned = subprocess.run(command, check=False, capture_output=True, text=True,timeout=30)
            if returned.returncode !=0:
                return f'Process exited with code {returned.returncode}, STDOUT:{returned.stdout} STDERR:{returned.stderr}'
            elif returned.stdout=="" and returned.stderr=="":
                return "No output produced"
            else:
                return f"STDOUT:{returned.stdout} STDERR:{returned.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
