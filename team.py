from agent import run_agent  # one function for all agents

# Manager: plans only, no tools
MANAGER = (
    "You are the Manager of a small team. You never do the work yourself. "
    "Turn the user's request into one clear, short task for the developer. "
    "Answer only with the task."
)

# Dev: writes the code into a real file
DEV = (
    "You are Dev, a Python developer. Do the task you get. "
    "Always save your code with the write_file tool as solution.py. "
    "After saving, answer with one sentence about what the code does."
)

# Reviewer: reads the real file and checks it
REVIEWER = (
    "You are a strict code reviewer. You get a task. "
    "Read solution.py with the read_file tool and check if the code really does the task "
    "and runs without errors. "
    "If it is good, answer only: APPROVED. "
    "If not, answer: CHANGES: followed by a short list of what to fix."
)

request = input("Your request: ")

task = run_agent(MANAGER, request)  # no tools needed
print("\n[Manager -> Dev]:", task)

dev_input = task
approved = False

for attempt in range(1, 4):
    print(f"\n--- Attempt {attempt} ---")

    result = run_agent(DEV, dev_input, use_tools=True)
    print("\n[Dev]:", result)

    review = run_agent(REVIEWER, f"Task:\n{task}", use_tools=True)
    print("\n[Reviewer]:", review)

    if review.strip().startswith("APPROVED"):
        approved = True
        break

    # Not approved: send the feedback back to Dev
    dev_input = (
        f"Task:\n{task}\n\nReviewer feedback:\n{review}\n\n"
        "Read solution.py, fix it, and save it again with write_file."
    )

if approved:
    print("\nApproved! The code is in workspace/solution.py")
else:
    print("\nNot approved after 3 attempts.")
