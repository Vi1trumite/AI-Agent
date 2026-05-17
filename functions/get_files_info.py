import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        entries = []
        for name in os.listdir(target_dir):
            filepath = os.path.join(target_dir, name)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            entries.append(f"- {name}: file_size={file_size} bytes, {is_dir=}")
        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"