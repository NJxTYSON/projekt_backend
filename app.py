from flask import Flask, request, jsonify, redirect
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

# ✅ API: Authenticate
@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    if data.get("key") == ACCESS_KEY:
        return jsonify({"success": True, "message": "Access granted"})
    return jsonify({"success": False, "message": "Access denied"}), 403

# ✅ API: Log device info
@app.route("/api/log", methods=["POST"])
def log_device():
    data = request.json
    log_line = f"{datetime.now()} - {data.get('deviceId')} - v{data.get('version')}\n"
    os.makedirs("data", exist_ok=True)
    with open("data/logs.txt", "a") as f:
        f.write(log_line)
    return "", 204

# ✅ API: Get feature flags
@app.route("/api/flags", methods=["GET"])
def get_flags():
    return jsonify(FEATURE_FLAGS)

# ✅ UI: Control panel form
@app.route("/", methods=["GET"])
def dashboard():
    return f"""
    <html><head><title>PROJEKT LUDO Control Panel</title>
    <style>
    body {{ background:#111; color:#fff; font-family:sans-serif; padding:20px; }}
    input[type=checkbox]{{margin-right:8px}}
    button{{padding:10px 20px; background:#00ffcc; border:none; margin-top:20px;}}
    </style></head><body>
    <h1>PROJEKT LUDO Control Panel</h1>
    <form action="/update_flags" method="post">
      <label><input type="checkbox" name="killSwitch" {'checked' if FEATURE_FLAGS['killSwitch'] else ''}> Kill Switch</label><br>
      <label>Enable Buttons:</label><br>
      {"".join([
        f'<label><input type="checkbox" name="buttonsEnabled" value="{i}" {"checked" if FEATURE_FLAGS["buttonsEnabled"][i] else ""}> Button {i+1}</label><br>'
        for i in range(6)
      ])}
      <label>Message:</label><br>
      <input type="text" name="message" value="{FEATURE_FLAGS['message']}" style="width:100%;padding:8px;"><br>
      <button type="submit">Update</button>
    </form>
    </body></html>
    """

# ✅ Handle dashboard form submission
@app.route("/update_flags", methods=["POST"])
def update_flags():
    global FEATURE_FLAGS
    form = request.form
    FEATURE_FLAGS["killSwitch"] = "killSwitch" in form
    FEATURE_FLAGS["buttonsEnabled"] = [str(i) in form.getlist("buttonsEnabled") for i in range(6)]
    FEATURE_FLAGS["message"] = form.get("message", "")
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
