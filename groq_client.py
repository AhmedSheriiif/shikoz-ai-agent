from groq import Groq
import json
from tool_schemas import tools
from tools import (get_car_price, get_available_colors, get_all_cars,
                   edit_test_drive_request, save_test_drive_request, check_test_drive_request,
                   search_policy)
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
# MODEL = "llama-3.3-70b-versatile"
MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"



def response_to_text(text):
    print("----------------------------", text)
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=text,
            tools=tools,
            tool_choice="auto"
        )
        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        # append assistant message properly
        text.append({
            "role": "assistant",
            "content": response_msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in tool_calls
            ] if tool_calls else []
        })

        if not tool_calls:
            # no more tools needed — return final answer
            return response_msg.content

        # execute all tool calls
        available_functions = {
            "get_car_price": get_car_price,
            "get_available_colors": get_available_colors,
            "get_all_cars": get_all_cars,
            "edit_test_drive_request": edit_test_drive_request,
            "save_test_drive_request": save_test_drive_request,
            "check_test_drive_request": check_test_drive_request,
            "search_policy": search_policy,
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_args is None:
                function_args = {}
            function_response = function_to_call(**function_args)
            text.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
        # loop continues — sends tool results back to model
