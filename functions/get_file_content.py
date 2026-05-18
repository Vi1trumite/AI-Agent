import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_dir, "r") as file:
            file_contents = file.read(MAX_CHARS)
            if file.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents
    except Exception as e:
        return f"Error: {e}"
