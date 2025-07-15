import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    print(f"{working_directory} -- {path} -- {os.path.abspath(path)}")
    if working_directory not in os.path.abspath(path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        return "Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'\
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to or overwrites files at the specified filepath, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content in a string to be written to the file",
            ),
        },
    ),
)