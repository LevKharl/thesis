from pydub import AudioSegment
import os

# Directory containing the MP3 files
input_directory = '/scratch/project_2008167/lev_thesis/audio/trimmed_audio'
# Directory to save the WAV files
output_directory = '/scratch/project_2008167/lev_thesis/audio/wav_files'
os.makedirs(output_directory, exist_ok=True)


def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
        print(f'Converted and saved: {wav_path}')
    except Exception as e:
        print(f'Error converting {mp3_path}: {e}')


# Convert each MP3 file to WAV
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".mp3"):
            mp3_path = os.path.join(root, file)
            wav_path = os.path.join(
                output_directory, file.replace(".mp3", ".wav"))
            convert_mp3_to_wav(mp3_path, wav_path)

print("Conversion to WAV complete")
