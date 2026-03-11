from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "ultra_secret_key_singulos"

# OpenAI Setup (Ersetze mit deinem Key oder nutze Umgebungsvariablen)
client = OpenAI(api_key="DEIN_OPENAI_API_KEY")

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Datenbank initialisieren
with get_db() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, assistant TEXT, role TEXT, message TEXT)")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    assistant_name = data.get("assistant")

    # KI-Anfrage (basierend auf deinen Kodes)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Du bist {assistant_name}. Antworte im Stil einer hochentwickelten Sci-Fi-KI."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Systemfehler im Quanten-Kern: {str(e)}"

    # Speichern in DB
    with get_db() as conn:
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, ?, ?)", (assistant_name, "user", user_msg))
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, ?, ?)", (assistant_name, "assistant", reply))

    return jsonify({"reply": reply})

from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "ultra_secret_key_singulos"

# OpenAI Setup
# TIPP: Setze deinen Key hier ein oder nutze os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key="DEIN_OPENAI_API_KEY")

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Datenbank beim Start initialisieren
with get_db() as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, assistant TEXT, role TEXT, message TEXT)")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get("message")
    assistant_name = data.get("assistant")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Du bist {assistant_name}. Antworte im Stil einer hochentwickelten Sci-Fi-KI."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Systemfehler im Quanten-Kern: {str(e)}"

    with get_db() as conn:
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, ?, ?)", (assistant_name, "user", user_msg))
        conn.execute("INSERT INTO chats (assistant, role, message) VALUES (?, ?, ?)", (assistant_name, "assistant", reply))

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    id = "canvas" > < / canvas >
                        < div


    class ="app-container" >
< div


class ="sidebar" id="sidebar" >

</div>

< div


class ="main-content" >

< div


class ="ai-display" >

< h1
id = "ai-name" > SINGULOS < / h1 >
< img
id = "ai-img"


class ="ai-avatar" src="" alt="AI" >

< / div >

< div


class ="chat-box" >

< div
id = "messages" > < / div >
< div


class ="input-area" >

< input
type = "text"
id = "userInput"
placeholder = "Quantenbefehl senden..." >
< button
onclick = "sendMessage()" > SEND < / button >
< / div >
< / div >
< / div >
< / div >

< script >
const
agents = [
    {name: "SINGULOS", img: "/static/assets/485162690...n.jpg"},
    {name: "IONOS-7", img: "/static/assets/485757034...n.jpg"},
    {name: "AUTOKRYPT", img: "/static/assets/485767621...n.jpg"},
    {name: "NEBULA", img: "/static/assets/485859062...n.jpg"},
    {name: "VOID", img: "/static/assets/485882728...n.jpg"},
    {name: "ZENITH", img: "/static/assets/486018216...n.jpg"},
    {name: "ORION", img: "/static/assets/486038969...n.jpg"},
    {name: "QUANTUM", img: "/static/assets/491211109...n.jpg"},
    {name: "CHRONOS", img: "/static/assets/491512015...n.jpg"},
    {name: "ULTRA", img: "/static/assets/491856978...n.jpg"}
];

let
activeAI = agents[0];

function
initSidebar()
{
    const
sb = document.getElementById('sidebar');
agents.forEach((a, index) => {
    const
div = document.createElement('div');
div.className = 'nav-item' + (index === 0 ? ' active': '');
div.style.backgroundImage = `url('${a.img}')`;
div.onclick = () = > selectAI(index, div);
sb.appendChild(div);
});
selectAI(0);
}

function
selectAI(index, el)
{
    activeAI = agents[index];
document.getElementById('ai-name').innerText = activeAI.name;
document.getElementById('ai-img').src = activeAI.img;
document.querySelectorAll('.nav-item').forEach(i= > i.classList.remove('active'));
if (el) el.classList.add('active');

// Effekt-Farbe ändern je nach KI
const colors =['#00ffff', '#f39c12', '#ff00ff', '#00ff00', '#ff0000'];
document.documentElement.style.setProperty('--glow', colors[index %colors.length]);
}

async function
sendMessage()
{
    const
input = document.getElementById('userInput');
const
box = document.getElementById('messages');
if (!input.value)
return;

box.innerHTML += ` < div


class ="msg-u" > DU: $


    ${input.value}< / div > `;
const
userText = input.value;
input.value = '';

const
res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: userText, assistant: activeAI.name})
});
const
data = await res.json();
box.innerHTML += ` < div


class ="msg-a" > ${activeAI.name}: $


    {data.reply} < / div > `;
box.scrollTop = box.scrollHeight;
}

// Heilige
Geometrie
Animation(Blume
des
Lebens)
const
canvas = document.getElementById('canvas');
const
ctx = canvas.getContext('2d');
function
draw()
{
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
ctx.strokeStyle = "rgba(100, 100, 100, 0.2)";
const
time = Date.now() * 0.001;
for (let i=0; i < 12; i++) {
    ctx.beginPath();
ctx.arc(window.innerWidth / 2 + Math.cos(time + i) * 50, window.innerHeight / 2 + Math.sin(time + i) * 50, 150, 0, Math.PI * 2);
ctx.stroke();
}
requestAnimationFrame(draw);
}
initSidebar();
draw();
< / script >
    < / body >
        < / html >
