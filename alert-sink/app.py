
from flask import Flask, request, jsonify
from datetime import datetime, timezone
from pathlib import Path
import json

app = Flask(__name__)
log_file = Path("/tmp/alerts.jsonl")

@app.get("/")
def home():
    return jsonify(status="running", service="local-alert-sink")

@app.get("/alerts")
def alerts():
    if not log_file.exists():
        return jsonify(alerts=[])
    data = []
    for line in log_file.read_text(encoding="utf-8").splitlines():
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return jsonify(alerts=data[-100:])

@app.post("/alerts")
def receive_alerts():
    payload = request.get_json(silent=True) or {}
    record = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "status": payload.get("status"),
        "alerts": payload.get("alerts", [])
    }
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print(json.dumps(record), flush=True)
    return jsonify(received=True), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
