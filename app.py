import os
import sqlite3
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)

# SECURITY HARDENING
_SEC_RATE_LIMIT={}
from time import monotonic
@app.before_request
def _sec_before():
    if request.content_length and request.content_length>1048576:return jsonify(error="Request too large."),413
    if request.path.startswith("/.git/") or request.path.startswith("/.env"):return jsonify(error="Not Found."),404
    ip=request.remote_addr or "unknown";now=monotonic();b=_SEC_RATE_LIMIT.setdefault(ip,[]);b[:]=[t for t in b if now-t<60];limit=30 if request.method in {"POST","PUT","PATCH","DELETE"} else 120
    if len(b)>=limit:return jsonify(error="Too many requests. Please try again later."),429
    b.append(now)
@app.after_request
def _sec_headers(response):
    response.headers.setdefault("X-Content-Type-Options","nosniff");response.headers.setdefault("X-Frame-Options","DENY");response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin");response.headers.setdefault("Permissions-Policy","camera=(), microphone=(), geolocation=()");response.headers.setdefault("Cross-Origin-Opener-Policy","same-origin");response.headers.setdefault("Strict-Transport-Security","max-age=31536000; includeSubDomains");response.headers.pop("Server",None);return response
app.secret_key = os.getenv("SECRET_KEY", "dev-only-change-me")
api_key = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY","").strip()
router_client=OpenAI(api_key=OPENROUTER_API_KEY,base_url="https://openrouter.ai/api/v1") if OPENROUTER_API_KEY else None
client = OpenAI(api_key=api_key) if api_key else None
MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.6-luna")


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
    user_msg = (data.get("message") or "").strip()\n    selected_model = (data.get("model") or MODEL).strip()
    assistant_name = (data.get("assistant") or "Quantum Cat").strip()
    if not user_msg:
        return jsonify({"error": "message is required"}), 400
    if client is None:
        reply = "OpenAI ist nicht konfiguriert. Setze OPENAI_API_KEY in der Umgebung."
    else:
        try:
            response = (router_client if (router_client and selected_model) else client).chat.completions.create(
                model=selected_model,
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
