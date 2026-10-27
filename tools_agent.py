from agent import run_agent

SYSTEM = "You are a helpful assistant. Always use your tools to read, list and write files. Never just show code, save it with write_file."

print("AI:", run_agent(SYSTEM, input("You: "), use_tools=True))
