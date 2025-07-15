import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    print(f"{working_directory} -- {path} -- {os.path.abspath(path)}")
    if working_directory not in os.path.abspath(path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if file_path[len(file_path)-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["uv", "run", path], capture_output=True, timeout=30)
        if result.returncode != 0:
            return f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}\nProcess exited with code {result.returncode}'
        elif result == None:
            return "No output produced."
        else:
            return f'STDOUT:{result.stdout}\nSTDERR:{result.stderr}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python from a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath to run the .py file from, relative to the working directory. If the provided filepath does not end with .py, it will not run.",
            ),
        },
    ),
)
