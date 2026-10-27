import requests
from tools import TOOLS, run_tool
URL = "http://localhost:11434/api/chat"




# Same as before, but now we also send the tools,
# and we return the whole message (not only the text).
def ask_ai(messages):
    data = {"model": "qwen3:4b", "messages": messages, "tools": TOOLS, "stream": False}
    response = requests.post(URL, json=data)
    return response.json()["message"]

# The conversation starts with the user's question
messages = [
    {"role": "system", "content": "You are a helpful assistant. Always use your tools to read, list and write files. Never just show code, save it with write_file."},
    {"role": "user", "content": input("You: ")},
]

# The agent loop: repeat until the AI gives a final answer
while True:
    message = ask_ai(messages)
    messages.append(message)  # save the AI's message in the history

    # No tool request -> this is the final answer
    if not message.get("tool_calls"):
        print("AI:", message["content"])
        break

    # The AI asked for one or more tools -> run each one
    for call in message["tool_calls"]:
        name = call["function"]["name"]       # which tool, e.g. "read_file"
        args = call["function"]["arguments"]  # its inputs, e.g. {"path": "solution.py"}
        print(f"[Tool] {name}({args})")

    result = run_tool(name, args)  # replaces the whole if/elif block
    messages.append({"role": "tool", "content": result, "tool_name": name})
