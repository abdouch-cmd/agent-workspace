import os  # library to work with files and folders
import requests

# Full path of the workspace folder, e.g. C:\...\agent-workspace\workspace
WORKSPACE = os.path.abspath("workspace")


def read_file(path):
    # Build the full path and clean it (abspath resolves ".." for us)
    full_path = os.path.abspath(os.path.join(WORKSPACE, path))

    # Security: refuse anything outside the workspace folder
    if not full_path.startswith(WORKSPACE + os.sep):
        return "Error: you can only read files inside the workspace."

    # File doesn't exist -> tell the AI instead of crashing
    if not os.path.exists(full_path):
        return "Error: file not found."

    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


URL = "http://localhost:11434/api/chat"


# The "menu" for the AI: describes the tool in JSON format.
# The AI reads this to know the tool exists and when to use it.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",  # must match our Python function name
            "description": "Read a text file from the workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    # the tool needs one input: "path" (a text)
                    "path": {"type": "string", "description": "File name, e.g. solution.py"}
                },
                "required": ["path"],  # path is not optional
            },
        },
    }
]


# Same as before, but now we also send the tools,
# and we return the whole message (not only the text).
def ask_ai(messages):
    data = {"model": "qwen3:4b", "messages": messages, "tools": TOOLS, "stream": False}
    response = requests.post(URL, json=data)
    return response.json()["message"]

# The conversation starts with the user's question
messages = [
    {"role": "system", "content": "You are a helpful assistant. Use your tools when you need to read files."},
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

        if name == "read_file":
            result = read_file(args["path"])  # run the real Python function
        else:
            result = "Error: unknown tool."

        # Give the result back to the AI with role "tool"
        messages.append({"role": "tool", "content": result, "tool_name": name})

    # back to the top of the loop: the AI now sees the tool result
