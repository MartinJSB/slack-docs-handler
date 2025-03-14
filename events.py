from slack_bolt import App
from slack_bolt.context.respond import Respond

from tools.drive_video_to_audio import download_audio_from_drive

def register_events(slack_app: App):
    @slack_app.event("message")
    def message_handler(event, say):
        try:
            user_text = event.get("text", "")  # Get user message
            user_id = event.get("user", "")      # Get user ID
            say(f"Hello <@{user_id}>! You said: {user_text}")
        except Exception as e:
            # Notify the user with an error message
            say(f"An error occurred while processing your message: {str(e)}")

    @slack_app.command("/upload_meeting")
    def handle_upload(ack, respond: Respond, command):
        try:
            ack()  # Acknowledge the command immediately
            respond("Uploading...")
            drive_link = command.get("text", "").strip()
            if not drive_link:
                respond("No Google Drive link was provided.")
                return

            # Verify the link is a Google Drive link.
            if "drive.google.com" not in drive_link:
                respond("The provided link is not a valid Google Drive link.")
                return

            # Attempt to download the video and extract the audio.
            result = download_audio_from_drive(drive_link)
            if result["status"] == "success":
                respond(result["message"])
                # Optionally: upload the audio file to persistent storage and send its URL.
            else:
                respond(f"Error: {result['message']}")
        except Exception as e:
            respond(f"An unexpected error occurred: {str(e)}")