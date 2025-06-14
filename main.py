import os
import sys

from typing_extensions import Optional, Tuple, List

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse, GenerateContentConfig
from google.genai import types

from functions.utils import call_function, available_functions

from prompts import system_prompt

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def request_ai(messages: List[types.Content]) -> GenerateContentResponse:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    return response


def get_response_text(response: GenerateContentResponse) -> str:
    if not response.text:
        return "NO RESULTS"

    return response.text


def get_response_meta(
    response: GenerateContentResponse,
) -> Tuple[Optional[int], Optional[int]]:
    if response.usage_metadata:
        meta = response.usage_metadata

        return (meta.prompt_token_count, meta.candidates_token_count)

    else:
        return (None, None)


def do_interaction_with_ai(
    messages: List[types.Content],
    is_verbose: bool = False,
    iter_number: int = 0,
    max_iteration: int = 20,
) -> str:
    response = request_ai(messages)

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return get_response_text(response)

    for function_call_part in response.function_calls:
        result = call_function(function_call_part)

        parts = result.parts

        if (
            not parts
            or not parts[0].function_response
            or not parts[0].function_response.response
        ):
            raise Exception("No response from function call")

        messages.append(result)

        if is_verbose:
            print(f"-> {parts[0].function_response.response}")

        if iter_number < max_iteration:
            return do_interaction_with_ai(
                messages, is_verbose, iter_number + 1, max_iteration
            )

        return get_response_text(response)


def main():
    is_verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("The prompt was not provided!")
        print('Example: python main.py "prompt here" [--verbose]')
        sys.exit(1)

    user_prompt = " ".join(args)

    messages: List[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    result = do_interaction_with_ai(messages, is_verbose)

    print("Final result: ")
    print(result)


if __name__ == "__main__":
    main()
