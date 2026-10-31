import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import *
from call_function import call_function, available_functions

def main() -> None:
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY environment variable not set")

    client = OpenAI(
        base_url="http://127.0.0.1:8080/v1",
        api_key=api_key,
    )

    parser =argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
        ,]

    for rounds in range(20):
        response = client.chat.completions.create(
            model="google/gemma-4-31B-it-qat-q4_0-gguf",
            messages=messages,
            tools=available_functions, )

        # Check usage BEFORE anything reads it (the verbose block below does).
        if response.usage is None:
            raise RuntimeError("API response has no usage metadata — request may have failed")

        message = response.choices[0].message
        messages.append(message)

        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens:{response.usage.prompt_tokens} ')
            print(f'Response tokens:{response.usage.completion_tokens} ')

        if not message.tool_calls:
            print('Response:')
            print(message.content)
            break

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose=args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("content empty")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        raise SystemExit("hit MAX_ROUNDS without a final answer")


if __name__ == "__main__":
    main()
