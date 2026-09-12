import os
import sqlite3
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


with get_db() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, assistant TEXT, role TEXT, message TEXT)")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "project": "Quantum-KI-CAT.CHAT", "openai_configured": client is not None})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = (data.get("message") or "").strip()
    assistant_name = (data.get("assistant") or "Quantum Cat").strip()
    if not user_msg:
        return jsonify({"error": "message is required"}), 400
    if client is None:
        reply = "OpenAI ist nicht konfiguriert. Setze OPENAI_API_KEY in der Umgebung."
    else:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"Du bist {assistant_name}, eine hochentwickelte Sci-Fi-KI."},
                    {"role": "user", "content": user_msg},
                ],
            )
            reply = response.choices[0].message.content or "Keine Antwort erhalten."
        except Exception:
            reply = "Die KI-Schnittstelle ist momentan nicht erreichbar."
    with get_db() as conn:
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, 'user', ?)", (assistant_name, user_msg))
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, 'assistant', ?)", (assistant_name, reply))
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")), debug=False)
