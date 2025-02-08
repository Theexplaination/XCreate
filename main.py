from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Use the API key (store in Replit Secrets for security)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBOJI4akLHLRfappP3BqdXOdiqbajPhOIc")  # Use secret if available
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
    app.run(host="0.0.0.0", port=5000, debug=True)  # Updated to use port 5000
