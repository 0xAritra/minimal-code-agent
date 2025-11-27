import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional: The list of arguments to pass to the python program. If not provided, takes empty args list.",
                items=types.Schema(
                  type=types.Type.STRING
                )
            ),
        },
    ),
)

def run_python_file(working_dir, file_path, args=[]):
  abs_working_dir = os.path.abspath(working_dir)
  full_path = os.path.join(abs_working_dir, file_path)
  abs_path = os.path.abspath(full_path)

  if (not abs_path.startswith(abs_working_dir)):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
  if (not os.path.isfile(abs_path)):
    return (f'Error: File "{file_path}" not found.')
  
  if (not abs_path.endswith(".py")):
    return f'Error: "{file_path}" is not a Python file.'
  
  try:
    op_str = ""
    completed_process = subprocess.run(["python3", abs_path, *args], capture_output=True, text=True, timeout=30)
    if (completed_process.stdout):
      op_str += f"STDOUT: {completed_process.stdout}\n"
    if (completed_process.stderr):
      op_str += f"STDERR: {completed_process.stderr}\n"
    if completed_process.returncode != 0:
      op_str += f"Process exited with code {completed_process.returncode}\n"
    if not completed_process:
      return "No output produced.\n"

    op_str += "---\n"
    return op_str
    
  except Exception as e:
    return f"Error: executing Python file: {e}"