from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# ✅ Hardcoded access key
ACCESS_KEY = "1234"

# ✅ Feature flags
FEATURE_FLAGS = {
    "killSwitch": False,
    "buttonsEnabled": [True, False, True, True, True, True],
    "message": "Welcome to PROJEKT LUDO"
}

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    if data.get("key") == ACCESS_KEY:
        return jsonify({"success": True, "message": "Access granted"})
    return jsonify({"success": False, "message": "Access denied"}), 403

@app.route("/api/log", methods=["POST"])
def log_device():
    data = request.json
    log_line = f"{datetime.now()} - {data.get('deviceId')} - v{data.get('version')}\n"
    os.makedirs("data", exist_ok=True)
    with open("data/logs.txt", "a") as f:
        f.write(log_line)
    return "", 204

@app.route("/api/flags", methods=["GET"])
def get_flags():
    return jsonify(FEATURE_FLAGS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
