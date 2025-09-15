from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "botbela_verify_token"
PAGE_ACCESS_TOKEN = "EAAPVY60zAeIBPWVha8QDduxZCdJ5mDkCn7v6GF7ttj82u3tOA6FGvxcR5Rf6HQYKXRqWVmhAUKXCHbOc0gdHYaAHSRKZAA93aCoWGz8hq4YnnD1vLEjwpwtVFZCFM0IdvedgVDAH6kmTl1KR9AWOKhVJPDRxIRKsSFgNvuZCwZBTnvQpSiT6gSsjGZCjuNkpULXlMb5wZDZD"

@app.route('/')
def index():
    return "Botbela is running!", 200

@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Verification token mismatch", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)

    if "entry" in data:
        for entry in data["entry"]:
            for msg_event in entry.get("messaging", []):
                sender = msg_event["sender"]["id"]

                if "message" in msg_event and "text" in msg_event["message"]:
                    text = msg_event["message"]["text"]
                    reply = f"তুমি লিখেছো: {text} 😁"
                    send_message(sender, reply)

    return "ok", 200

def send_message(recipient_id, message):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    body = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    requests.post(url, params=params, headers=headers, json=body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
