import requests

# Python code we want the AI to explain
code = """
def multiply(a, b):
    return a * b
"""

# Create a prompt
prompt = f"""
Explain this Python code in simple words.
Be accurate and give one example.

{code}
"""

# Send a request to our local Ollama API
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:0.5b",
        "prompt": prompt,
        "stream": False
    },
    timeout=180
)

# Check whether the request succeeded
response.raise_for_status()

# Convert JSON response into a Python dictionary
result = response.json()

# Display the AI explanation
print("AI EXPLANATION:")
print(result["response"])