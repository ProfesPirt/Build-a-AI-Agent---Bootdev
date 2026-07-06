import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

import json

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

def generate_content(client, messages, available_functions):
    chat_completed = client.chat.completions.create(
        model = "openrouter/free",
        messages = messages,
        temperature = 0,
        tools =  available_functions
    )
    return chat_completed

def call_function(tool_call, verbose: bool = False) -> dict:
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"Error: Unknown function: {function_name}",
    }

    function_args["working_directory"] = "./calculator"

    result = function_map[function_name](**function_args)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    }
    


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    available_functions = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise RuntimeError("API key not found check to see if you setup your .env file correctly")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):

        chat_completed = generate_content(client, messages, available_functions)

        message = chat_completed.choices[0].message
        messages.append(message)
        if not chat_completed.usage:
            raise RuntimeError("It seems the API request has failed try again?")
    
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {chat_completed.usage.prompt_tokens}\nResponse tokens: {chat_completed.usage.completion_tokens}")

    
        if message.tool_calls is not None:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if len(result_message["content"]) == 0:
                    raise Exception("Error: Uhhh I have no idea how we got here")
                if args.verbose:
                    print(f"-> {result_message["content"]}")
        else:
            print(message.content)
            return
    print("It would appear the AI could not solve the problem in time")
    exit(1)


if __name__ == "__main__":
    main()
