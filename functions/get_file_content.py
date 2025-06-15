import os

from google.genai import types

MAX_CHARS = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_abspath, file_path))

        if not file_abspath.startswith(working_abspath):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abspath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content_string = ""

        with open(file_abspath, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += (
                    f'...File "{file_path}" truncated at 10000 characters'
                )

        return file_content_string

    except Exception as e:
        return f'Error while read file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Get file contentent restricted by {MAX_CHARS} symbols by file path, constrained in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory, should be inside working directory. If not provided, return error.",
            ),
        },
    ),
)
