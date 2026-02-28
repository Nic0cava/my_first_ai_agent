import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", file_path_abs]
        if args:
            command.extend(args)
        output = ""
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stderr and not result.stdout:
            output += "No output produced\n"
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        return output.strip()


    except Exception as e:
        return f"Error: executing Python file: {e}"