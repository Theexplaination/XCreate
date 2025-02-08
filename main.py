from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Get API key from environment variable (set in Render)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
if not GEMINI_API_KEY:
    raise ValueError("⚠️ ERROR: GEMINI_API_KEY not found in environment variables!")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        ai_reply = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
        return jsonify({"reply": ai_reply})
    else:
        return jsonify({"error": "API request failed", "details": response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
