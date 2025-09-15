from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Fixed Verify Token
VERIFY_TOKEN = "botbela_verify_token"

# Your Page Access Token (from Facebook)
PAGE_ACCESS_TOKEN = "EAAPVY60zAeIBPWVha8QDduxZCdJ5mDkCn7v6GF7ttj82u3tOA6FGvxcR5Rf6HQYKXRqWVmhAUKXCHbOc0gdHYaAHSRKZAA93aCoWGz8hq4YnnD1vLEjwpwtVFZCFM0IdvedgVDAH6kmTl1KR9AWOKhVJPDRxIRKsSFgNvuZCwZBTnvQpSiT6gSsjGZCjuNkpULXlMb5wZDZD"

GRAPH_API = "https://graph.facebook.com/v17.0/me/messages"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        if data and data.get("object") == "page":
            for entry in data.get("entry", []):
                for ev in entry.get("messaging", []):
                    if ev.get("message") and ev["message"].get("text"):
                        sender = ev["sender"]["id"]
                        text = ev["message"]["text"]
                        reply = f"🤖 Botbela says: You said → {text}"
                        send_message(sender, reply)
        return "OK", 200


def send_message(recipient_id, text):
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    r = requests.post(GRAPH_API, params=params, json=payload)
    if r.status_code != 200:
        print("Send error:", r.status_code, r.text)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
