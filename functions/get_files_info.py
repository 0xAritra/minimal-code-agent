import os
from google.genai import types

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

def get_files_info(working_dir, directory="."):
  abs_working_dir = os.path.abspath(working_dir)
  full_path = os.path.join(abs_working_dir, directory)
  abs_path = os.path.abspath(full_path)
  if (not abs_path.startswith(abs_working_dir)):
    return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

  if (not os.path.isdir(abs_path)):
    return (f'Error: "{directory}" is not a directory')

  res = f"Results for {directory} directory:\n"
  for file in os.listdir(abs_path):
    file_path = os.path.join(abs_path, file)
    res += f"\t- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}\n"
  return res

