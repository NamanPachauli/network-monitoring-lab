
from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)
is_up = True

@app.get("/")
def home():
    return jsonify(service="network-monitoring-demo", status="running")

@app.get("/health")
def health():
    if not is_up:
        return jsonify(status="DOWN"), 503
    return jsonify(status="UP"), 200

@app.post("/simulate/down")
def simulate_down():
    global is_up
    is_up = False
    return jsonify(status="DOWN", time=datetime.now(timezone.utc).isoformat())

@app.post("/simulate/up")
def simulate_up():
    global is_up
    is_up = True
    return jsonify(status="UP", time=datetime.now(timezone.utc).isoformat())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
