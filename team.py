import requests

URL = "http://localhost:11434/api/chat"


def ask_ai(messages):
    data = {"model": "qwen3:4b", "messages": messages, "stream": False}
    response = requests.post(URL, json=data)
    return response.json()["message"]["content"]


def run_agent(system_prompt, task):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]
    return ask_ai(messages)


MANAGER = (
    "You are the Manager of a small team. You never do the work yourself. "
    "Turn the user's request into one clear, short task for the developer. "
    "Answer only with the task."
)

DEV = (
    "You are Dev, a Python developer. Do the task you get. "
    "Answer with short, working Python code and one sentence of explanation."
)
REVIEWER = (
    "You are a strict code reviewer. You get a task and the code for it. "
    "Check if the code really does the task and runs without errors. "
    "If it is good, answer only: APPROVED. "
    "If not, answer: CHANGES: followed by a short list of what to fix."
)

request = input("Your request: ")

task = run_agent(MANAGER, request)
print("\n[Manager -> Dev]:", task)
dev_input = task

for attempt in range(1, 4):
    print(f"\n--- Attempt {attempt} ---")

    result = run_agent(DEV, dev_input)
    print("\n[Dev]:", result)

    review_input = f"Task:\n{task}\n\nCode from Dev:\n{result}"
    review = run_agent(REVIEWER, review_input)
    print("\n[Reviewer]:", review)

    if review.strip().startswith("APPROVED"):
        print("\nApproved!")
        break

    dev_input = (
        f"Task:\n{task}\n\nYour last code:\n{result}\n\n"
        f"Reviewer feedback:\n{review}\n\nFix the code."
    )
