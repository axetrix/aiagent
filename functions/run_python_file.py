import os
import subprocess
from pathlib import Path

from typing_extensions import List, Dict, Callable

from google.genai import types


def run_python_file(
    working_directory: str, file_path: str, args: List[str] | None = None
) -> str:
    try:
        working_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_abspath, file_path))

        if not file_abspath.startswith(working_abspath):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not Path(file_abspath).exists():
            return f'Error: File "{file_path}" not found.'

        if Path(file_abspath).suffix != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        commands = ["python", file_abspath]
        if args:
            commands.extend(args)

        print(f"Ran {file_path} file")

        result = subprocess.run(
            commands,
            timeout=30,
            capture_output=True,
            check=True,
            text=True,
            cwd=working_directory,
        )

        messages = []

        if result.returncode == 0:
            if result.stderr.strip():
                messages.append(f"STDERR: {result.stderr.strip()}")

            if result.stdout.strip():
                messages.append(f"STDOUT: {result.stdout.strip()}")

            if len(messages) == 0:
                messages.append("No output produced.")
        else:
            messages.append(f"Process exited with code {result.returncode}")

            if result.stderr.strip():
                messages.append(f"STDERR: {result.stderr.strip()}")

            if result.stdout.strip():
                messages.append(f"STDOUT: {result.stdout.strip()}")

            if not result.stdout.strip() and not result.stderr.strip():
                messages.append("No output produced.")

        return "\n".join(messages)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute or run a Python file when the user asks to run, execute, launch, or start a Python script. Use this function when users say things like 'run script.py', 'execute main.py', 'launch my_file.py', or similar commands.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute (e.g., 'main.py', 'script.py', 'src/app.py'). Extract this from user requests like 'run main.py' where 'main.py' is the file_path.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Command-line arguments for the Python script. Extract from requests like 'run script.py --verbose' where '--verbose' would be an argument. Can be null if no arguments provided.",
                nullable=True,
            ),
        },
        required=["file_path"],
    ),
)
