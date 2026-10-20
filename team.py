import requests
import os

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
# The AI answers with text + code between ``` marks.
# This function keeps only the code part.
def extract_code(text):
    if "```" not in text:
        return text  # no ``` marks: return everything

    code = text.split("```")[1]  # the part between the first two ```

    if code.startswith("python"):
        code = code[len("python"):]  # remove the word "python"

    return code.strip()  # remove spaces at start and end


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
approved = False  # becomes True when the Reviewer says APPROVED

for attempt in range(1, 4):
    print(f"\n--- Attempt {attempt} ---")

    result = run_agent(DEV, dev_input)
    print("\n[Dev]:", result)

    review_input = f"Task:\n{task}\n\nCode from Dev:\n{result}"
    review = run_agent(REVIEWER, review_input)
    print("\n[Reviewer]:", review)

    if review.strip().startswith("APPROVED"):
        print("\nApproved!")
        approved = True
        break

    dev_input = (
        f"Task:\n{task}\n\nYour last code:\n{result}\n\n"
        f"Reviewer feedback:\n{review}\n\nFix the code."
    )


# Human approval: only save if the user says yes
if approved:
    answer = input("\nSave the code to workspace/solution.py? (y/n): ")
    if answer == "y":
        code = extract_code(result)
        os.makedirs("workspace", exist_ok=True)  # create folder if missing
        with open("workspace/solution.py", "w", encoding="utf-8") as f:  # "w" = write
            f.write(code)
        print("Saved!")
else:
    print("\nNot approved after 3 attempts. Nothing saved.")
