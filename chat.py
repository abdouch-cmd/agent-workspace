import requests
URL = "http://localhost:11434/api/chat"
history = []
while True:
    message = input("Enter your message: ")

    if message.lower() == "exit":
        break
    history.append({"role": "user", "content": message})
    data ={
    "model": "qwen3:4b",
    "messages": history,
    "stream": False,
        }
    response = requests.post(URL, json=data)
    answer = response.json()["message"]["content"]
    print("AI:", answer)
    history.append({"role": "assistant", "content": answer})
