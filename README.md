# Agent Workspace

A small multi-agent system that runs 100% locally with [Ollama](https://ollama.com).
A Manager, a Developer and a Reviewer work together to write Python code,
using tools to read and write files in a safe sandbox.

## Features
- **Team of agents:** Manager plans the task, Dev writes code, Reviewer checks it
- **Feedback loop:** if the Reviewer finds problems, Dev fixes them (max 3 attempts)
- **Tool calling:** agents can read, list and write files
- **Sandbox:** tools can only access the `workspace/` folder
- **Human approval:** the user must confirm before any file is written
- **Runs locally:** no API key, no cloud, model `qwen3:4b`

## How it works
User request → Manager → Dev (writes `solution.py`) → Reviewer (reads it)
→ APPROVED, or feedback back to Dev

## Project structure
| File | What it does |
|---|---|
| `tools.py` | The tools (read/list/write files), sandbox check and tool menu |
| `agent.py` | `run_agent()`: the agent loop, with or without tools |
| `team.py` | Manager → Dev → Reviewer pipeline with feedback loop |
| `tools_agent.py` | A single agent with tools, for testing |
| `chat.py` | Simple chatbot with memory |

## Setup
1. Install [Ollama](https://ollama.com) and run `ollama pull qwen3:4b`
2. Install Python 3 and `pip install requests`
3. Start Ollama, then:
   ```
   python team.py
   ```

## What I learned
- How agents can talk to each other: the output of one agent becomes the input of the next
- How an agent receives a request, reads it and turns it into a clear task
- How work is split between agents with different roles (Manager, Dev, Reviewer)
- How tool calling works: the AI asks for a tool, my code runs it and sends back the result
- Why you should never trust the AI blindly: sandbox and human approval before writing files


## Next steps
- [ ] RAG: let agents answer questions from my own documents
- [ ] Tests with pytest
- [ ] Web UI and Docker
