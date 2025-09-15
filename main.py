import os
import json
import datetime
from flask import Flask, request

app = Flask(__name__)

# Page Access Token (your given token)
PAGE_ACCESS_TOKEN = "EAAPVY60zAeIBPWVha8QDduxZCdJ5mDkCn7v6GF7ttj82u3tOA6FGvxcR5Rf6HQYKXRqWVmhAUKXCHbOc0gdHYaAHSRKZAA93aCoWGz8hq4YnnD1vLEjwpwtVFZCFM0IdvedgVDAH6kmTl1KR9AWOKhVJPDRxIRKsSFgNvuZCwZBTnvQpSiT6gSsjGZCjuNkpULXlMb5wZDZD"

VERIFY_TOKEN = "botbela_verify_2025"

# Track user limits
user_limits = {}

# Reset limits daily
def reset_limits():
    today = datetime.date.today()
    for user_id in list(user_limits.keys()):
        if user_limits[user_id]["date"] != today:
            user_limits[user_id] = {"count": 0, "date": today}

# Send message to user
import requests
def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, headers=headers, data=json.dumps(payload))

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verification
        token_sent = request.args.get("hub.verify_token")
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token", 403

    elif request.method == "POST":
        output = request.json
        reset_limits()
        for event in output["entry"]:
            messaging = event["messaging"]
            for message in messaging:
                if message.get("message"):
                    recipient_id = message["sender"]["id"]
                    text = message["message"].get("text", "")

                    # Check limit
                    today = datetime.date.today()
                    if recipient_id not in user_limits:
                        user_limits[recipient_id] = {"count": 0, "date": today}

                    if user_limits[recipient_id]["date"] != today:
                        user_limits[recipient_id] = {"count": 0, "date": today}

                    if user_limits[recipient_id]["count"] >= 40:
                        send_message(recipient_id, "⚠️ You've reached today's 40 message limit. Please try again tomorrow!")
                        continue

                    # Increase counter
                    user_limits[recipient_id]["count"] += 1

                    # Funny responses
                    if "hi" in text.lower():
                        reply = "👋 Hello! How are you doing?"
                    elif "kemon" in text.lower():
                        reply = "😃 Valo achi! Tumi kemon?"
                    elif "joke" in text.lower():
                        reply = "😂 Why don’t scientists trust atoms? Because they make up everything!"
                    else:
                        reply = "😄 I'm your Botbela! Let's have some fun chatting!"

                    send_message(recipient_id, reply)
        return "Message Processed", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
