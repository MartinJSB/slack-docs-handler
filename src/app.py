import os
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../.env")

# Initialize Slack app
slack_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)

# Flask app
app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@app.route("/", methods=["POST"])
def slack_events():
    data = request.get_json()
    
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    return handler.handle(request)

@slack_app.event("message")
def message_handler(event, say):
    user_text = event.get("text", "")  # Get user message
    user_id = event.get("user", "")  # Get user ID
    say(f"Hello <@{user_id}>! You said: {user_text}")

if __name__ == "__main__":
    app.run(port=3000, debug=True)
