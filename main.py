import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("API key not found check to see if you setup your .env file correctly")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def main():
    print("Hello from ai-agent-project!")
    chat_completed = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ]
    )
    if not chat_completed.usage:
        raise RuntimeError("It seems the API request has failed try again?")
    print(f"Prompt tokens: {chat_completed.usage.prompt_tokens}\nResponse tokens: {chat_completed.usage.completion_tokens}")
    print(chat_completed.choices[0].message.content)


if __name__ == "__main__":
    main()
