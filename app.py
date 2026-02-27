import os
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "motivateme")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
quotes = db["quotes"]

ALLOWED_MOODS = {"focus", "confidence", "calm", "energy"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/random")
def random_quote():
    pipeline = [
        {"$match": {"active": True}},
        {"$sample": {"size": 1}},
    ]
    result = list(quotes.aggregate(pipeline))
    if not result:
        return jsonify({"error": "No quotes found."}), 404
    doc = result[0]
    return jsonify({"text": doc["text"], "author": doc["author"], "mood": doc["mood"]})


@app.route("/api/random/<mood>")
def random_quote_by_mood(mood):
    mood = mood.lower()
    if mood not in ALLOWED_MOODS:
        return jsonify({"error": "Invalid mood. Choose: focus, confidence, calm, energy."}), 400
    pipeline = [
        {"$match": {"active": True, "mood": mood}},
        {"$sample": {"size": 1}},
    ]
    result = list(quotes.aggregate(pipeline))
    if not result:
        return jsonify({"error": "No quotes found for that mood."}), 404
    doc = result[0]
    return jsonify({"text": doc["text"], "author": doc["author"], "mood": doc["mood"]})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
