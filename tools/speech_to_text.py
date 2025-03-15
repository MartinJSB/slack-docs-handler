import requests
import json
import os

def transcribe_audio(file_path):
    """
    Transcribes an audio file using the Azure fast transcription API with diarization enabled.
    
    Parameters:
        file_path (str): Path to the local audio file.
    
    Returns:
        str: The transcribed text or an error message.
    """
    # Construct the endpoint URL (using the fast transcription API)
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_REGION")

    url = f"https://{service_region}.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2024-11-15"
    
    # Read the audio file in binary mode
    try:
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
    # Prepare the JSON definition to set the locale and enable diarization
    definition = {
        "locales": ["en-US"],
        "diarization": {"maxSpeakers": 2, "enabled": True}
    }
    
    # Create the multipart/form-data payload.
    # The "audio" field holds the file content,
    # The "definition" field holds the JSON configuration.
    files = {
        "audio": (file_path, audio_data),
        "definition": (None, json.dumps(definition), "application/json")
    }
    
    # Set the subscription key header
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key
    }
    
    # Make the POST request to the fast transcription endpoint
    response = requests.post(url, headers=headers, files=files)
    
    # Check for a successful response
    if response.status_code == 200:
        try:
            result = response.json()
            print(result)
            # Extract the transcribed text from "combinedPhrases"
            if "combinedPhrases" in result and result["combinedPhrases"]:
                transcription = "\n".join(phrase["text"] for phrase in result["combinedPhrases"])
                return transcription
            else:
                return "Transcription completed but no 'combinedPhrases' found in the response."
        except Exception as e:
            return f"Error parsing JSON response: {e}"
    else:
        return f"API error {response.status_code}: {response.text}"

# Example usage:
if __name__ == "__main__":
    
    # Replace with the path to your audio file
    audio_file_path = "output_e4ef7375f8354db59b67c08866726bb9.wav"
    
    transcript = transcribe_audio(audio_file_path)
    print("Transcription Result:")
    print(transcript)
