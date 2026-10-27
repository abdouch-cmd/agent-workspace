import os  # library to work with files and folders
WORKSPACE = os.path.abspath("workspace")
os.makedirs(WORKSPACE, exist_ok=True)
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
# Run the real Python function for the tool the AI asked for
def run_tool(name, args):
    if name == "read_file":
        return read_file(args["path"])
    elif name == "list_files":
        return list_files()
    elif name == "write_file":
        return write_file(args["path"], args["content"])
    else:
        return "Error: unknown tool."
