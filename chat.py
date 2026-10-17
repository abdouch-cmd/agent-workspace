import requests
URL = "http://localhost:11434/api/chat"
message = input("Enter your message: ")
data ={
    "model": "qwen3:4b",
    "messages": [{"role": "user","content": message}],
    "stream": False,
}
response = requests.post(URL, json=data)
answer = response.json()["message"]["content"]
print("AI:", answer)
