from slack_bolt import App
from slack_bolt.context.respond import Respond

from tools.compress_audio import compress_wav
from tools.drive_video_to_audio import download_audio_from_drive
from tools.speech_to_text import transcribe_audio

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
            audio_result = download_audio_from_drive(drive_link)
            if audio_result["status"] != "success":
                respond(f"Error: {audio_result['message']}")

            # Reduce file size if needed
            compressed_audio = compress_wav(audio_result["file_path"])
            
            transcription_result = transcribe_audio(compressed_audio)
            respond(transcription_result)
        except Exception as e:
            respond(f"An unexpected error occurred: {str(e)}")