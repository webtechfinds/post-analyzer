from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import base64
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Post Analyzer API is running"

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
You are a social media strategist reviewing an educational post. Rate it on these 5 metrics (0-5 scale):

1. Hook: Is the post's first impression strong and scroll-stopping?
2. Attention: Does it keep the viewer engaged visually?
3. Value: Is the content informative, useful, or inspiring?
4. Interaction: Is there a clear call to action or engagement element?
5. Design: Is the design clean, modern, and well-structured?

Return a JSON response in this format:
{
  "scores": [hook, attention, value, interaction, design],
  "feedback": [
    {"metric": "Hook", "comment": "..."},
    {"metric": "Attention", "comment": "..."},
    {"metric": "Value", "comment": "..."},
    {"metric": "Interaction", "comment": "..."},
    {"metric": "Design", "comment": "..."}
  ]
}
"""

        try:
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful social media strategist assistant."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        # NEW DEBUG LOGGING
        print("RAW GPT RESPONSE:", response.choices[0].message.content)

        text = response.choices[0].message.content.strip()
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        json_text = text[json_start:json_end]

        import json
        result = json.loads(json_text)
        return jsonify(result)


    except Exception as e:
        return jsonify({"error": str(e)}), 500
