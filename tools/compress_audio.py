import os
import numpy as np
from scipy.io import wavfile

def compress_wav(file_path, max_size_bytes=100*1024*1024):
    """
    Compresses a .wav file repeatedly by downsampling until its file size is below max_size_bytes.
    
    Each compression iteration takes every other sample and halves the sample rate.
    The compressed files are saved with an appended suffix indicating the iteration.
    
    Parameters:
        file_path (str): Path to the original .wav file.
        max_size_bytes (int): Maximum allowed file size in bytes (default 100 MB).
        
    Returns:
        str: The path to the final compressed .wav file.
    """
    current_file = file_path
    iteration = 0
    
    while os.path.getsize(current_file) > max_size_bytes:
        # Read current WAV file
        sample_rate, data = wavfile.read(current_file)
        
        # Downsample: take every other sample
        new_data = data[::2]
        # Halve the sample rate to maintain playback duration
        new_sample_rate = sample_rate // 2
        
        # Create a new file name by appending an iteration marker before the extension.
        base, ext = os.path.splitext(file_path)
        new_file = f"{base}_compressed_{iteration}{ext}"
        
        # Write the compressed file
        wavfile.write(new_file, new_sample_rate, new_data)
        
        print(f"Iteration {iteration}: Compressed file saved at {new_file} with size {os.path.getsize(new_file) / (1024*1024):.2f} MB")
        
        # Prepare for the next iteration if needed
        if os.path.exists(current_file):
            os.remove(current_file)

        current_file = new_file
        iteration += 1
        
    return current_file

# Example usage:
if __name__ == "__main__":
    original_file = "example.wav"
    final_file = compress_wav(original_file)
    print(f"Final compressed file saved at: {final_file}")
