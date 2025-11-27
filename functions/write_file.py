import os
from config import MAX_CHARS
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the file.",
            ),
        },
    ),
)

def write_file(working_dir, file_path, content):
  abs_working_dir = os.path.abspath(working_dir)
  full_path = os.path.join(abs_working_dir, file_path)
  abs_path = os.path.abspath(full_path)

  if (not abs_path.startswith(abs_working_dir)):
    return (f'Error: Cannot list "{dir}" as it is outside the permitted working directory')
    

  os.makedirs(abs_working_dir, exist_ok=True)  
  
  try:
    with open(abs_path, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: {e}"