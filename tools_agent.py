import os  # library to work with files and folders
import requests

# Full path of the workspace folder, e.g. C:\...\agent-workspace\workspace
WORKSPACE = os.path.abspath("workspace")
os.makedirs(WORKSPACE, exist_ok=True)  # make sure the folder exists


# Security check used by all tools.
# Returns the full path if it's inside the workspace, otherwise None.
def safe_path(path):
    full_path = os.path.abspath(os.path.join(WORKSPACE, path))
    if not full_path.startswith(WORKSPACE + os.sep):
        return None
    return full_path

def read_file(path):
    full_path = safe_path(path)
    if full_path is None:
        return "Error: you can only read files inside the workspace."
    # File doesn't exist -> tell the AI instead of crashing
    if not os.path.exists(full_path):
        return "Error: file not found."

    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

# Tool: list all files in the workspace folder
def list_files():
    files = os.listdir(WORKSPACE)  # names of everything inside the folder
    if not files:
        return "The workspace is empty."
    return "\n".join(files)  # one file name per line

# Tool: write a file in the workspace, only if the user allows it
def write_file(path, content):
    full_path = safe_path(path)
    if full_path is None:
        return "Error: you can only write files inside the workspace."

    # Human approval: show what the AI wants to write, then ask
    print(f"\n[AI wants to write {path}]\n{content}\n")
    answer = input("Allow? (y/n): ")
    if answer != "y":
        return "Error: the user did not allow this."

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved {path}."

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
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",  # must match our Python function name
            "description": "List all files in the workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",  # must match our Python function name
            "description": "Write a text file in the workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File name, e.g. solution.py"},
                    "content": {"type": "string", "description": "The text to write into the file."}
                },
                "required": ["path", "content"],
            },
        }
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

        # Run the real Python function based on the tool name
        if name == "read_file":
            result = read_file(args["path"])
        elif name == "list_files":
            result = list_files()
        elif name == "write_file":
            result = write_file(args["path"], args["content"])
        else:
            result = "Error: unknown tool."

        # Give the result back to the AI with role "tool"
        messages.append({"role": "tool", "content": result, "tool_name": name})

    # back to the top of the loop: the AI now sees the tool result
