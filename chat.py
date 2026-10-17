import requests

URL = "http://localhost:11434/api/chat"
def ask_ai(message):
    data = {
        "model": "qwen3:4b",
        "messages": message,
        "stream": False,
    }
    response = requests.post(URL, json=data)
    answer = response.json()["message"]["content"]
    return answer
SYSTEM_PROMPT = "You are Dev, a helpful Python developer. You answer short and clear, and you always give a small code example."

history = [{"role": "system", "content": SYSTEM_PROMPT}]
while True:
    message = input("Enter your message: ")

    if message.lower() == "exit":
        break
    history.append({"role": "user", "content": message})
    answer = ask_ai(history)
    print("AI:", answer)
    history.append({"role": "assistant", "content": answer})
