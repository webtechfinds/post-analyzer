from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Social Media Post Analyzer API is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    prompt = """
You are a social media strategist. Analyze this image post and score it (0 to 5) on these metrics:

1. Hook – Is it scroll-stopping?
2. Attention – Does it keep viewers engaged?
3. Value – Is the content useful or insightful?
4. Interaction – Does it encourage engagement (comments, likes, shares)?
5. Design – Is the visual layout clear, bold, and well-structured?

Respond in this exact JSON format:
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
            model="gpt-4-turbo",  # ✅ Updated to latest model with Vision
            messages=[
                {"role": "system", "content": "You are a helpful assistant for evaluating social media content."},
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

        # Parse and return result
        content = response.choices[0].message.content
        print("RAW GPT RESPONSE:", content)

        json_start = content.find('{')
        json_data = content[json_start:]
        result = eval(json_data)  # You can replace eval with json.loads(json_data) if needed
        return jsonify(result)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
