from slack_bolt import App

def register_events(slack_app: App):
    @slack_app.event("message")
    def message_handler(event, say):
        user_text = event.get("text", "")  # Get user message
        user_id = event.get("user", "")  # Get user ID
        say(f"Hello <@{user_id}>! You said: {user_text}")

    @slack_app.command("/upload")
    def handle_upload(ack, respond: Respond, command):
        ack()  # Acknowledge the command
        user_text = command.get("text", "")  # Get the text user entered
        user_id = command.get("user_id")  # Get user ID
        respond(f"📤 You uploaded: *{user_text}* (from <@{user_id}>)")
