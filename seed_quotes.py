import os
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "motivateme")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
quotes = db["quotes"]

SEED_QUOTES = [
    # focus
    {"text": "The secret of getting ahead is getting started.", "author": "Mark Twain", "mood": "focus"},
    {"text": "Focus on being productive instead of busy.", "author": "Tim Ferriss", "mood": "focus"},
    {"text": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle", "mood": "focus"},
    {"text": "Concentrate all your thoughts upon the work at hand.", "author": "Alexander Graham Bell", "mood": "focus"},
    {"text": "Do what you can, with what you have, where you are.", "author": "Theodore Roosevelt", "mood": "focus"},
    # confidence
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "mood": "confidence"},
    {"text": "You are braver than you believe, stronger than you seem, and smarter than you think.", "author": "A.A. Milne", "mood": "confidence"},
    {"text": "With confidence, you have won before you have started.", "author": "Marcus Garvey", "mood": "confidence"},
    {"text": "No one can make you feel inferior without your consent.", "author": "Eleanor Roosevelt", "mood": "confidence"},
    {"text": "You gain strength, courage, and confidence by every experience in which you really stop to look fear in the face.", "author": "Eleanor Roosevelt", "mood": "confidence"},
    # calm
    {"text": "Almost everything will work again if you unplug it for a few minutes, including you.", "author": "Anne Lamott", "mood": "calm"},
    {"text": "Breathe. Let go. And remind yourself that this very moment is the only one you know you have for sure.", "author": "Oprah Winfrey", "mood": "calm"},
    {"text": "Within you, there is a stillness and a sanctuary to which you can retreat at any time.", "author": "Hermann Hesse", "mood": "calm"},
    {"text": "Peace is the result of retraining your mind to process life as it is, rather than as you think it should be.", "author": "Wayne Dyer", "mood": "calm"},
    {"text": "The greatest weapon against stress is our ability to choose one thought over another.", "author": "William James", "mood": "calm"},
    # energy
    {"text": "Act as if what you do makes a difference. It does.", "author": "William James", "mood": "energy"},
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "mood": "energy"},
    {"text": "Energy and persistence conquer all things.", "author": "Benjamin Franklin", "mood": "energy"},
    {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "mood": "energy"},
    {"text": "Go confidently in the direction of your dreams. Live the life you have imagined.", "author": "Henry David Thoreau", "mood": "energy"},
]


def seed():
    now = datetime.now(timezone.utc)
    for q in SEED_QUOTES:
        existing = quotes.find_one({"text": q["text"]})
        if existing:
            continue
        quotes.insert_one({
            "text": q["text"],
            "author": q["author"],
            "mood": q["mood"],
            "active": True,
            "createdAt": now,
        })
    print(f"Seeding complete. Collection now has {quotes.count_documents({})} quotes.")


if __name__ == "__main__":
    seed()
