import os
def get_files_info(working_directory: str, directory: str = ".")-> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
       
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        if not os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files_in_directory = os.listdir(target_dir)
        

        return_string = f"Result for current directory:\n  " if directory == "." else f"Result for '{directory}' directory:\n  "

        for i in range(len(files_in_directory)):
            if i == 0:
                return_string += f"- {files_in_directory[i]}: file_size={os.path.getsize(os.path.join(target_dir ,files_in_directory[i]))} bytes, is_dir={os.path.isdir(os.path.join(target_dir , files_in_directory[i]))}"
                continue
            return_string += f"\n  - {files_in_directory[i]}: file_size={os.path.getsize(os.path.join(target_dir ,files_in_directory[i]))} bytes, is_dir={os.path.isdir(os.path.join(target_dir , files_in_directory[i]))}"

        return return_string



    
    except Exception as error:
        return f"Error: {str(error)}"
