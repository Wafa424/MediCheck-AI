import os
import re
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
os.environ["OPENAI_BASE_URL"] = "http://127.0.0.1:8088/v1"
DEBUG_MODE = os.getenv("FLASK_DEBUG", "0") == "1"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        user_data = request.get_json(silent=True) or {}
        symptoms = (user_data.get("symptoms") or "").strip()

        if not symptoms:
            return jsonify({"error": "Please enter your symptoms"}), 400
        h_mem_data = {"engine": "H-MEM", "status": "active", "input": symptoms}
        # --- CODE TEMPORAIRE POUR DÉMONSTRATION VIDÉO SANS ERREUR API ---
        # Simule une réponse immédiate et structurée
        symptoms_lower = symptoms.lower()
        
        if "chest" in symptoms_lower or "breath" in symptoms_lower or "severe" in symptoms_lower:
            parsed = {
                "level": "RED",
                "specialty": "Emergency Medicine / Cardiology",
                "summary": "Severe symptoms suggesting a potential cardiovascular or respiratory emergency.",
                "advice": [
                    "Call emergency services immediately or go to the nearest ER.",
                    "Do not attempt to drive yourself to the hospital.",
                    "Rest in a comfortable position while waiting for help."
                ]
            }
        else:
            parsed = {
                "level": "YELLOW",
                "specialty": "General Practice",
                "summary": "Moderate symptoms that warrant medical evaluation.",
                "advice": [
                    "Schedule an appointment with a general practitioner.",
                    "Monitor your symptoms closely over the next 24 hours.",
                    "Stay hydrated and rest."
                ]
            }

        return jsonify(parsed)

    except Exception as e:
        print("Backend exception:", str(e))
        return jsonify({"error": "Something went wrong while analyzing symptoms. Please try again."}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=DEBUG_MODE)