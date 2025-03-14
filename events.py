from slack_bolt import App
from slack_bolt.context.respond import Respond

def register_events(slack_app: App):
    @slack_app.event("message")
    def message_handler(event, say):
        user_text = event.get("text", "")  # Get user message
        user_id = event.get("user", "")  # Get user ID
        say(f"Hello <@{user_id}>! You said: {user_text}")

    @slack_app.command("/upload")
    def handle_upload(ack, respond: Respond, command):
        ack()  
