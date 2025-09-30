import requests

def summarize_text(text, model="gemma2:2b"):
    endpoint = "http://localhost:11434/api/generate"
    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
    data = {"model": model, "prompt": prompt}
    response = requests.post(endpoint, json=data)
    print(response)
    summary = response.json()['response']
    return summary

# Example usage:
with open("37aUuoRyMhM.txt", "r") as file:
    text = file.read()
print(summarize_text(text))
