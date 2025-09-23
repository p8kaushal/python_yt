import requests

def summarize_text(text, model="llama3"):
    endpoint = "http://localhost:11434/api/generate"
    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
    data = {"model": model, "prompt": prompt}
    response = requests.post(endpoint, json=data)
    summary = response.json()['response']
    return summary

# Example usage:
text = "The rise of artificial intelligence has led to significant advancements..."
print(summarize_text(text))
