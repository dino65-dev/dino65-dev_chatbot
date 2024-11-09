import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

app = Flask(__name__)

def claude_chat(prompt):
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude3.5Sonnet20241022",
        "prompt": prompt,
        "max_tokens_to_sample": 150
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json().get("completion", "Error fetching response").strip()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get("query")
    prompt = f"You are a GitHub assistant chatbot. Answer the following user question:\n\nUser: {user_query}\n\nAssistant:"
    response = claude_chat(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
