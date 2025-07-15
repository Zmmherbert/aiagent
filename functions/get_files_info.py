import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory=None):
    path = os.path.join(working_directory, directory)
    print(f"{working_directory} -- {path} -- {os.path.abspath(path)}")
    if working_directory not in os.path.abspath(path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    result = ""
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        result += f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"
    return result

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)