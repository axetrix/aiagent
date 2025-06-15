import os
import subprocess
from pathlib import Path

from typing_extensions import List, Dict, Callable

from google.genai import types


def make_dir(working_directory: str, dir_path: str) -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        dir_abspath = os.path.abspath(os.path.join(working_abspath, dir_path))

        if not dir_abspath.startswith(working_abspath):
            return f'Error: Cannot create a directory in "{dir_abspath}" as it is outside the permitted working directory'

        os.makedirs(dir_abspath, exist_ok=True)

        return f'Successfully create directory "{dir_abspath}")'
    except Exception as e:
        return f'Error create a directory "{dir_path}": {e}'


schema_make_dir = types.FunctionDeclaration(
    name="make_dir",
    description="Create a directory, constrained in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "dir_path": types.Schema(
                type=types.Type.STRING,
                description="The directory path represent the directory,located relative to the working directory, should be inside working directory. If not provided, return error.",
            ),
        },
    ),
)
