import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from openai import OpenAI
from werkzeug.exceptions import HTTPException

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API and Flask app
base_url = "https://api.aimlapi.com/v1"
api = OpenAI(api_key=api_key, base_url=base_url)
app = Flask(__name__)

# Rate limiting: max 5 requests per minute per IP
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_travel_advice(user_prompt):
    system_prompt = "You know everyting. Be descriptive and helpful."
    try:
        completion = api.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=256,
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return "Error: Unable to fetch travel advice at this time."

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
@limiter.limit("5 per minute")
def ask():
    data = request.get_json()
    user_prompt = data.get("query")
    if not user_prompt:
        return jsonify({"error": "Query parameter is required"}), 400

    response = get_travel_advice(user_prompt)
    return jsonify({"response": response})

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    logging.error(f"Unhandled exception: {e}")
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
