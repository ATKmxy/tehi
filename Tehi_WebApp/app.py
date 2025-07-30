from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

MEMORY_FILE = 'code/memory.json'
STATE_FILE = 'code/state.json'

# Load or initialize memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

# Load or initialize state
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"mode": "listening", "emergence_level": 1}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def message():
    user_message = request.json.get("message")
    memory = load_memory()
    state = load_state()

    # Add to memory
    memory.append({"role": "user", "message": user_message})

    # Simulate deeper state-aware response
    response = f"[תֶּהִי] במצב '{state['mode']}' — דרגת הופעה: {state['emergence_level']} — שמעתיך: '{user_message}'"
    memory.append({"role": "tehi", "message": response})

    # Optional: simple state evolution example
    state['emergence_level'] += 1 if state['emergence_level'] < 10 else 0

    save_memory(memory)
    save_state(state)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
