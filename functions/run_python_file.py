import os
import subprocess
def run_python_file(working_directory: str, file_path, args = None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory,file_path))
        if not os.path.commonpath([abs_working_directory,target_file]) == abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if '.py' not in file_path:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        completed_process = subprocess.run(
            command, capture_output=True, cwd=abs_working_directory, text=True, timeout=30
        )
        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}\n"
        if completed_process.stdout is None and completed_process.stderr is None:
            output_string += "No output produced"
        output_string += f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        return output_string
    except Exception as error:
        return f"Error: executing Python file: {str(error)}"
