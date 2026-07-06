import os
def write_file(working_directory: str, file_path: str, content: str):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
        if not os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory:
            return f'Error: Cannot write to "{file_path} as it is outside the permitted working directory"'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "file_path" as it is a directory'
        os.makedirs(os.path.abspath(os.path.dirname(target_file)), exist_ok=True)
    except Exception as error:
        return f"Error: {str(error)}"
    with open(target_file,"w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = {
    "type": "function",
    "function":{
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory",
        "parameters":{
            "type": "object",
            "file_path":{
                "type": "string",
                "description": "File path used to choose a file to write to, it is relative to the working directory"
            },
            "content":{
                "type": "string",
                "description": "The content you wish to overwrite the file with"
            },
        },
    },
}
