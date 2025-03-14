#!/usr/bin/env python3
import os
import time
import argparse
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.transcription import ConversationTranscriber
from dotenv import load_dotenv

def transcribe_audio(audio_filename):
    # Load credentials from .env (AZURE_SPEECH_KEY and AZURE_REGION)
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_REGION")
    if not speech_key or not service_region:
        print("Error: AZURE_SPEECH_KEY and AZURE_REGION must be set in your environment.")
        exit(1)

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.output_format = speechsdk.OutputFormat.Detailed

    # Create an audio configuration from the file.
    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    # Create a ConversationTranscriber instance.
    transcriber = ConversationTranscriber(speech_config=speech_config, audio_config=audio_config)

    done = False
    transcription_results = []

    # Callback for when a final result is received.
    def transcribed_cb(evt):
        result = evt.result
        if result.reason == speechsdk.ResultReason.Transcribed:
            # Attempt to get speaker information; if not available, use "unknown".
            speaker = getattr(result, "speaker_id", "unknown")
            print(f"Speaker {speaker}: {result.text}")
            transcription_results.append((speaker, result.text))
        else:
            print(f"Interim result: {result.text}")

    # Callback to signal the session has ended.
    def stop_cb(evt):
        nonlocal done
        print("Transcription session ended.")
        done = True

    # Connect the event handlers.
    transcriber.transcribed.connect(transcribed_cb)
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    print("Starting transcription...")
    transcriber.start_transcribing()

    # Wait until the transcription session ends.
    while not done:
        time.sleep(0.5)

    transcriber.stop_transcribing()
    return transcription_results

def main():
    parser = argparse.ArgumentParser(description="Diarized transcription using Azure Speech Service")
    parser.add_argument("audio_file", help="Path to the audio file")
    args = parser.parse_args()

    results = transcribe_audio(args.audio_file)
    print("\nFinal Transcription Results:")
    for speaker, text in results:
        print(f"Speaker {speaker}: {text}")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env
    main()
