import os
import subprocess
from pathlib import Path

from typing_extensions import List, Dict, Callable

from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_abspath, file_path))

        if not file_abspath.startswith(working_abspath):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(file_abspath), exist_ok=True)

        with open(file_abspath, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f'Error while write file "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to the file, constrained in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path represent the file where write content,located relative to the working directory, should be inside working directory. If not provided, return error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content contain a content that should be written to file",
            ),
        },
    ),
)
