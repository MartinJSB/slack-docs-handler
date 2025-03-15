import re
import os
import subprocess
import uuid
import gdown

def download_audio_from_drive(drive_url, output_audio=f"output_{uuid.uuid4().hex}.wav"):
    try:
        # Extract file ID from a typical Google Drive share link.
        file_id_match = re.search(r"/d/([^/]+)", drive_url)
        if file_id_match:
            file_id = file_id_match.group(1)
        else:
            # If no match, assume drive_url is already a file ID.
            file_id = drive_url

        # Construct the download URL.
        download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        
        # Generate a unique temporary file name.
        temp_video = f"temp_video_{uuid.uuid4().hex}.mp4"
        
        # Attempt to download the video.
        try:
            gdown.download(download_url, temp_video, quiet=False)
        except Exception as e:
            raise Exception(f"Failed to download video: {e}")
        
        # Prepare and run the ffmpeg command to extract audio as WAV.
        command = [
            "ffmpeg",
            "-i", temp_video,
            "-vn",             # disable video stream
            "-acodec", "pcm_s16le",  # WAV format
            "-ac", "2",
            "-ar", "44100",
            output_audio
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e}")

        # Remove the temporary video file.
        try:
            os.remove(temp_video)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file {temp_video}: {e}")
        
        # Return success response.
        return {"status": "success", "message": f"Audio file saved as: {output_audio}"}
    
    except Exception as error:
        # Return error response with error details.
        return {"status": "error", "message": str(error)}
