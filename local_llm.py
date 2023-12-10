import requests
import configparser

URL = "http://127.0.0.1:5000/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json"
}

HISTORY = []

def local_llm_call(prompt):
    HISTORY.append({"role": "user", "content": prompt})
    data = {
        "mode": "chat",
        "character": "Example",
        "messages": HISTORY
    }
    # Call local API for fallacy detection or other tasks
    response = requests.post(URL, headers=HEADERS, json=data, verify=False)
    assistant_message = response.json()['choices'][0]['message']['content']
    HISTORY.append({"role": "assistant", "content": assistant_message})
    print(assistant_message)
    return assistant_message

if __name__ == '__main__':
    prompt = "In order to make homemade bread, follow these steps:\n1)"
    local_llm_call(prompt)