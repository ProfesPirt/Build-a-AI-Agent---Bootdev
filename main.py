import os
from dotenv import load_dotenv
from openai import OpenAI

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
                "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
            }
        ]
    )
    print(chat_completed.choices[0].message.content)


if __name__ == "__main__":
    main()
