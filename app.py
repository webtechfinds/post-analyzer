from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "API is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    fake_response = {
        "scores": [4, 4, 5, 3, 4],
        "feedback": [
            {"metric": "Hook", "comment": "Strong opening, could be punchier."},
            {"metric": "Attention", "comment": "Great layout and contrast."},
            {"metric": "Value", "comment": "Delivers clear, actionable info."},
            {"metric": "Interaction", "comment": "No strong CTA."},
            {"metric": "Design", "comment": "Clean but a bit text-heavy."}
        ]
    }
    return jsonify(fake_response)
