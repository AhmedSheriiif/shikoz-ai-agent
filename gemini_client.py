from google import genai
from google.genai import types
import json

from config import GEMINI_API_KEY
from tools import (
    get_car_price,
    get_available_colors,
    get_all_cars,
    edit_test_drive_request,
    save_test_drive_request,
    check_test_drive_request,
    search_policy
)

from google.genai import types


def convert_messages(messages):
    gemini_messages = []

    for msg in messages:

        role = msg["role"]
        content = msg["content"]

        # Gemini doesn't support system role
        if role == "system":
            gemini_messages.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            text=f"SYSTEM INSTRUCTIONS:\n{content}"
                        )
                    ]
                )
            )

        elif role == "user":
            gemini_messages.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=content)
                    ]
                )
            )

        elif role == "assistant":
            gemini_messages.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part(text=content or "")
                    ]
                )
            )

    return gemini_messages

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"


available_functions = {
    "get_car_price": get_car_price,
    "get_available_colors": get_available_colors,
    "get_all_cars": get_all_cars,
    "edit_test_drive_request": edit_test_drive_request,
    "save_test_drive_request": save_test_drive_request,
    "check_test_drive_request": check_test_drive_request,
    "search_policy": search_policy,
}



def response_to_text(messages):
    gemini_messages = convert_messages(messages)

    response = client.models.generate_content(
        model=MODEL,
        contents=gemini_messages,
        config=types.GenerateContentConfig(
            tools=gemini_tools
        )
    )
    while True:

        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[
                    get_car_price,
                    get_available_colors,
                    get_all_cars,
                    edit_test_drive_request,
                    save_test_drive_request,
                    check_test_drive_request,
                    search_policy,
                ]
            )
        )

        candidate = response.candidates[0]

        parts = candidate.content.parts

        tool_calls = []

        for part in parts:
            if hasattr(part, "function_call") and part.function_call:
                tool_calls.append(part.function_call)

        # No tool call → final answer
        if not tool_calls:
            return response.text

        # Execute tools
        for tool_call in tool_calls:

            function_name = tool_call.name
            function_args = dict(tool_call.args)

            function_to_call = available_functions[
                function_name
            ]

            function_response = function_to_call(
                **function_args
            )

            # Send tool result back
            messages.append(
                types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={
                                "result": function_response
                            }
                        )
                    ]
                )
            )