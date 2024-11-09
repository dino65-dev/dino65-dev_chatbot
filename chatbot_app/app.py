from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your actual API key
ANTHROPIC_API_KEY = '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'

def claude_chat(prompt):
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": "claude3.5Sonnet20241022",
        "prompt": prompt,
        "max_tokens_to_sample": 200
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
