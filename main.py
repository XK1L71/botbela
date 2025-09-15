from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "botbela_verify_2025"
PAGE_ACCESS_TOKEN = "EAAPVY60zAeIBPWVha8QDduxZCdJ5mDkCn7v6GF7ttj82u3tOA6FGvxcR5Rf6HQYKXRqWVmhAUKXCHbOc0gdHYaAHSRKZAA93aCoWGz8hq4YnnD1vLEjwpwtVFZCFM0IdvedgVDAH6kmTl1KR9AWOKhVJPDRxIRKsSFgNvuZCwZBTnvQpSiT6gSsjGZCjuNkpULXlMb5wZDZD"

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
    if "entry" in data:
        for entry in data["entry"]:
            if "messaging" in entry:
                for messaging_event in entry["messaging"]:
                    if "message" in messaging_event and "text" in messaging_event["message"]:
                        sender_id = messaging_event["sender"]["id"]
                        message_text = messaging_event["message"]["text"]
                        reply = generate_reply(message_text)
                        send_message(sender_id, reply)
    return "ok", 200

def generate_reply(user_msg):
    user_msg = user_msg.lower()
    if "hi" in user_msg or "hello" in user_msg:
        return "Hello! 😃 কেমন আছেন?"
    elif "kemon" in user_msg or "কেমন" in user_msg:
        return "আমি ভালো আছি! আপনি কেমন আছেন?"
    elif "joke" in user_msg or "মজা" in user_msg:
        return "😂 একটা জোক শুনুন: কেন কম্পিউটার ঠান্ডায় কাঁপে? কারণ তার অনেক ফ্যান থাকে!"
    else:
        return "😅 আমি একটা মজার বট! কিছু লিখুন, আমি উত্তর দিব।"

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
