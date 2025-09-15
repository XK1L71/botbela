from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "botbela_verify_token"
PAGE_ACCESS_TOKEN = "EAAPVY60zAeIBPWVha8QDduxZCdJ5mDkCn7v6GF7ttj82u3tOA6FGvxcR5Rf6HQYKXRqWVmhAUKXCHbOc0gdHYaAHSRKZAA93aCoWGz8hq4YnnD1vLEjwpwtVFZCFM0IdvedgVDAH6kmTl1KR9AWOKhVJPDRxIRKsSFgNvuZCwZBTnvQpSiT6gSsjGZCjuNkpULXlMb5wZDZD"

user_limits = {}

@app.route('/', methods=['GET'])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return str(challenge)
    return 'Invalid verification token'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if 'message' in messaging_event:
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message'].get('text')

                    if not sender_id in user_limits:
                        user_limits[sender_id] = {"count": 0}

                    if user_limits[sender_id]["count"] < 40:
                        reply = funny_reply(message_text)
                        send_message(sender_id, reply)
                        user_limits[sender_id]["count"] += 1
                    else:
                        send_message(sender_id, "⚠️ আজকের limit (40) শেষ! কালকে আবার চেষ্টা করুন 🙂")

    return "Message Processed"

def funny_reply(msg):
    if not msg:
        return "😅 বলো কী খবর?"
    text = msg.lower()
    if "hi" in text or "hello" in text:
        return "👋 হ্যালো! কেমন আছো?"
    if "kemon" in text or "কেমন" in text:
        return "😊 আমি ভালো, তুমি কেমন আছো?"
    if "valo" in text:
        return "👍 দারুন! শোনাও নতুন কী চলছে?"
    return "😂 আহা! মজার কথা বলো, একটু হাসাই!"

def send_message(recipient_id, message_text):
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v13.0/me/messages",
                  params=params, headers=headers, json=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
