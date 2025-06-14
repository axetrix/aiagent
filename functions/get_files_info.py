import os
import subprocess
from pathlib import Path

from typing_extensions import List, Dict, Callable

from google.genai import types

MAX_CHARS = 10000


def get_files_info(
    working_directory: str, directory: str | None = None
) -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        target_path = working_abspath

        if directory:
            target_path = os.path.abspath(os.path.join(target_path, directory))

            if not target_path.startswith(working_abspath):
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        files = []

        for item in os.listdir(target_path):
            file = os.path.join(target_path, item)

            if os.path.isfile(file):
                files.append(
                    f"- {item}: file_size={os.path.getsize(file)} bytes, is_dir=False"
                )
            else:
                files.append(
                    f"- {item}: file_size={os.path.getsize(file)} bytes, is_dir=True"
                )

        return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"



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
