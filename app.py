import os
import sqlite3
import base64
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from dotenv import load_dotenv

# Konfiguration
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "quantum_secret_99")

# OpenAI Client (holt Key aus Render Environment oder .env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- LOGIK: DREIFACHE VERSCHLÜSSELUNG (Aus deinem Ultra-Code) ---
def ultra_transform(text):
    data = text.encode()
    for _ in range(3):
        data = base64.b64encode(data[::-1])
    return data.decode()

# --- DATENBANK SETUP ---
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

with get_db() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, assistant TEXT, role TEXT, message TEXT, encrypted TEXT)")

# --- ROUTEN ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    assistant_name = data.get("assistant")

    # 1. Text verschlüsseln
    encrypted_preview = ultra_transform(user_msg)

    # 2. KI Anfrage
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Du bist {assistant_name}, eine hochentwickelte KI in einem Dark-Sci-Fi Universum."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Systemfehler im Kern: {str(e)}"

    # 3. Speichern
    with get_db() as conn:
        conn.execute("INSERT INTO chats (assistant, role, message, encrypted) VALUES (?, ?, ?, ?)", 
                     (assistant_name, "user", user_msg, encrypted_preview))

    return jsonify({"reply": reply, "encryption": encrypted_preview})

if __name__ == '__main__':
    # Lokal auf Port 5000, Render nutzt gunicorn
    app.run(debug=True, port=5000)
