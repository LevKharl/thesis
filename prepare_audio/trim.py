from pydub import AudioSegment
import os

# Directory containing the extracted audio files
input_directory = '/scratch/project_2008167/lev_thesis/audio/extracted_audio'
# Directory to save the trimmed audio files
output_directory = '/scratch/project_2008167/lev_thesis/audio/trimmed_audio'
os.makedirs(output_directory, exist_ok=True)

# Desired length of the audio samples in milliseconds
desired_length_ms = 30 * 1000  # 30 seconds

# Function to trim an audio file


def trim_audio(file_path, output_path, length_ms):
    try:
        audio = AudioSegment.from_file(file_path)
        if len(audio) > length_ms:
            trimmed_audio = audio[:length_ms]
            trimmed_audio.export(output_path, format="mp3")
            print(f'Trimmed and saved: {output_path}')
        else:
            print(
                f'Skipping {file_path} as it is shorter than {length_ms / 1000} seconds.')

        # Delete the original file to save space
        os.remove(file_path)
        print(f'Deleted original file: {file_path}')

    except Exception as e:
        print(f'Error processing {file_path}: {e}')


# Process each audio file in the input directory
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".mp3"):
            input_path = os.path.join(root, file)
            output_path = os.path.join(output_directory, file)
            trim_audio(input_path, output_path, desired_length_ms)

print("Trimming complete")
