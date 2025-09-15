from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Messenger verification
VERIFY_TOKEN = "botbela_verify_token"  # এটা Messenger App এ callback verification token হিসেবে দিতে হবে

@app.route("/", methods=["GET"])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return str(challenge)
    return "Invalid verification token"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Message received:", data)  # শুধু টেস্টের জন্য log
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
