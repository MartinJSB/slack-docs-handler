import os
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
from events import register_events

if os.getenv("FLASK_ENV") == "development":
    load_dotenv(dotenv_path="../.env")

slack_app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)

register_events(slack_app)

# Flask app
app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@app.route("/", methods=["GET"])
def hello():
    return "What do you want!?"

@app.route("/", methods=["POST"])
def slack_events():
    data = request.get_json()
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    return handler.handle(request) 

@app.route("/slack/events", methods=["POST"])
def slack_commands():
    return handler.handle(request)

if __name__ == "__main__":
    app.run(port=3000, debug=True)
