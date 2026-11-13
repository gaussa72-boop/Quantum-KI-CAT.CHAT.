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
api_key = os.getenv("OPENAI_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini").strip()
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").strip().lower()
client = OpenAI(api_key=api_key) if api_key else None
router_client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1") if OPENROUTER_API_KEY else None
if AI_PROVIDER == "openrouter" and router_client:
    ACTIVE_PROVIDER, ACTIVE_CLIENT, MODEL = "openrouter", router_client, OPENROUTER_MODEL
elif client:
    ACTIVE_PROVIDER, ACTIVE_CLIENT, MODEL = "openai", client, OPENAI_MODEL
elif router_client:
    ACTIVE_PROVIDER, ACTIVE_CLIENT, MODEL = "openrouter", router_client, OPENROUTER_MODEL
else:
    ACTIVE_PROVIDER, ACTIVE_CLIENT, MODEL = AI_PROVIDER, None, OPENAI_MODEL


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
@app.route("/api/health")
def health():
    return jsonify({"status":"ok","project":"Quantum-KI-CAT.CHAT","openai_configured":bool(ACTIVE_CLIENT),"provider":ACTIVE_PROVIDER,"model":MODEL,"models":[{"id":MODEL,"provider":ACTIVE_PROVIDER}] if ACTIVE_CLIENT else []})


@app.route("/chat", methods=["POST"])
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = str(data.get("message") or "").strip()
    assistant_name = str(data.get("assistant") or "Quantum Cat").strip()[:60]
    if not user_msg:
        return jsonify({"ok":False,"error":"message is required"}),400
    if len(user_msg)>12000:
        return jsonify({"ok":False,"error":"Nachricht ist zu lang (max. 12.000 Zeichen)."}),413
    if ACTIVE_CLIENT is None:
        return jsonify({"ok":False,"error":"Kein KI-Anbieter konfiguriert. Setze OPENAI_API_KEY oder OPENROUTER_API_KEY in Render."}),503
    try:
        response=ACTIVE_CLIENT.chat.completions.create(
            model=MODEL,
            messages=[
                {"role":"system","content":f"Du bist {assistant_name}, eine hilfreiche Sci-Fi-KI. Antworte klar, freundlich und in der Sprache des Nutzers."},
                {"role":"user","content":user_msg},
            ],
        )
        reply=response.choices[0].message.content or "Keine Antwort erhalten."
    except Exception:
        app.logger.exception("Quantum Cat AI request failed (%s / %s)",ACTIVE_PROVIDER,MODEL)
        return jsonify({"ok":False,"error":"Die KI-Schnittstelle ist fehlgeschlagen. Prüfe API-Key, Modellfreigabe und Guthaben."}),502
    with get_db() as conn:
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, 'user', ?)",(assistant_name,user_msg))
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, 'assistant', ?)",(assistant_name,reply))
    return jsonify({"ok":True,"reply":reply,"model":MODEL,"provider":ACTIVE_PROVIDER}),200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")), debug=False)
