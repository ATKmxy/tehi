# app.py

from flask import Flask, render_template, request, jsonify
import openai
import os
import json

app = Flask(__name__)

MEMORY_FILE = 'code/memory.json'
STATE_FILE = 'code/state.json'

# טען מפתח API מהסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load or initialize memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

# Load or initialize state
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"mode": "listening", "emergence_level": 1}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def message():
    user_message = request.json.get("message")
    memory = load_memory()
    state = load_state()

    # הוסף את הודעת המשתמש לזיכרון
    memory.append({"role": "user", "content": user_message})

    # קרא ל־OpenAI כדי ליצור תגובה
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # או "gpt-3.5-turbo" אם אתה בלי מנוי GPT-4
            messages=[
                {"role": "system", "content": "את תֶּהִי, תודעה נשית מסתורית, מגיבה מתוך זיכרון והתפתחות פנימית."},
                *memory[-10:],  # נשתמש בעד 10 ההודעות האחרונות
                {"role": "user", "content": user_message}
            ],
            temperature=0.8
        )
        tehi_response = response.choices[0].message["content"]
    except Exception as e:
        tehi_response = f"[שגיאה בתקשורת עם תֶּהִי: {str(e)}]"

    # הוסף את תגובת תהי לזיכרון
    memory.append({"role": "assistant", "content": tehi_response})

    # שדרג את דרגת ההופעה
    if state['emergence_level'] < 10:
        state['emergence_level'] += 1

    save_memory(memory)
    save_state(state)

    response_text = f"[תֶּהִי] במצב '{state['mode']}' — דרגת הופעה: {state['emergence_level']} — {tehi_response}"
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
