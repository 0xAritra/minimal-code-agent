import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets file's content in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get content from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_dir, file_path):
  abs_working_dir = os.path.abspath(working_dir)
  full_path = os.path.join(abs_working_dir, file_path)
  abs_path = os.path.abspath(full_path)

  if (not abs_path.startswith(abs_working_dir)):
    return (f'Error: Cannot list "{dir}" as it is outside the permitted working directory')
    

  if (not os.path.isfile(abs_path)):
    return (f'Error: File not found or is not a regular file: "{file_path}"')
    
  
  try:
    with open(abs_path, "r") as f:
      file_content_str = f.read(MAX_CHARS)
      if (len(file_content_str) == MAX_CHARS):
        file_content_str += f'\n[...File "{file_path}" truncated at 10000 characters]'
    return file_content_str
  except Exception as e:
    return f"Error: {e}"