import uuid
from pydub import AudioSegment
import os

def compress_wav(file_path, target_size_mb=50, output_path=f"output_{uuid.uuid4().hex}.wav"):
    """
    Compresses a WAV file to half its size if it's over 150MB.
    
    Args:
        file_path (str): Path to the input WAV file.
        output_path (str, optional): Path to save the compressed WAV file. If None, it overwrites the original.
        target_size_mb (int, optional): Target size in MB after compression. Defaults to half of 150MB.
        
    Returns:
        str: Path to the compressed WAV file.
    """
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
    
    if file_size_mb <= target_size_mb * 2:
        print("File is not large enough to compress. No action taken.")
        return file_path  # Return original file
    
    print(f"Original file size: {file_size_mb:.2f} MB")

    # Load audio file
    audio = AudioSegment.from_wav(file_path)
    
    # Estimate target bitrate to achieve half the size
    duration_sec = len(audio) / 1000  
    target_bitrate = int((target_size_mb * 4 * 1024 * 1024) / duration_sec)  # Convert MB to bits per second

    # Export with new bitrate
    audio.export(output_path, format="wav", bitrate=f"{target_bitrate}k")
    
    new_size_mb = os.path.getsize(output_path) / (1024 * 1024)  # Get new size
    print(f"Compressed file saved: {output_path} ({new_size_mb:.2f} MB)")

    if new_size_mb >= target_size_mb:
        return compress_wav(output_path, target_size_mb, output_path,)
    
    return output_path

if __name__ == "__main__":
    # Replace with the path to your audio file
    audio_file_path = "output_e4ef7375f8354db59b67c08866726bb9.wav"
    
    compressed_file_path = compress_wav(audio_file_path)
    print("Compression Result:", compressed_file_path)