import os
from config import MAX_CHARS 
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if not os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
                return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as error:
          return f"Error: {str(error)}"
          
    with open(target_file, "r") as f:
          file_content_str = f.read(MAX_CHARS)
          if f.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
          return file_content_str

schema_get_file_content = {
      "type": "function",
      "function": {
            "name": "get_file_content",
            "description": "Reads a given file specified by a file path relative to the working directory",
            "parameters":{
                  "type": "object",
                  "properties":{
                        "file_path": {
                              "type": "string",
                              "description": "File path used to choose a file to read, it is relative to the working directory"
                        },
                  },
            },
      },
}
