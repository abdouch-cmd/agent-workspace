import requests
from tools import TOOLS, run_tool

URL = "http://localhost:11434/api/chat"


# Send messages to the AI. Only send the tools menu if use_tools is True.
def ask_ai(messages, use_tools):
    data = {"model": "qwen3:4b", "messages": messages, "stream": False}
    if use_tools:
        data["tools"] = TOOLS
    response = requests.post(URL, json=data)
    return response.json()["message"]


# One agent = a system prompt + a task.
# With use_tools=True it can read, list and write files.
def run_agent(system_prompt, task, use_tools=False):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]

    # The agent loop (same as in tools_agent.py)
    while True:
        message = ask_ai(messages, use_tools)
        messages.append(message)

        # No tool request -> final answer, give it back
        if not message.get("tool_calls"):
            return message["content"]

        # Run each tool the AI asked for
        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            print(f"[Tool] {name}({args})")

            result = run_tool(name, args)
            messages.append({"role": "tool", "content": result, "tool_name": name})
