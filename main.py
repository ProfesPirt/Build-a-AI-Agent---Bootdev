import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI



def generate_content(client, messages):
    chat_completed = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )
    return chat_completed

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found check to see if you setup your .env file correctly")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "user", "content": args.user_prompt},
    ]
    chat_completed = generate_content(client, messages)
    if not chat_completed.usage:
        raise RuntimeError("It seems the API request has failed try again?")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {chat_completed.usage.prompt_tokens}\nResponse tokens: {chat_completed.usage.completion_tokens}")
    print(chat_completed.choices[0].message.content)


if __name__ == "__main__":
    main()
