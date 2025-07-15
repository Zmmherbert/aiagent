import os
from config import *
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    print(f"{working_directory} -- {path} -- {os.path.abspath(path)}")
    if working_directory not in os.path.abspath(path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(path, "r") as f:
            text = f.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS+1] + f'...File "{file_path}" truncated at {MAX_CHARS} characters'

    return text

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of files at the specified filepath as text up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to the file to read from, relative to the working directory.",
            ),
        },
    ),
)