import tarfile
import os
import hashlib
from pathlib import Path

# Path to the directory containing the tar files
tar_files_directory = '/scratch/project_2008167/lev_thesis/audio/'
# Path to the file containing the list of required tracks
track_ids_file = 'track_ids_to_download.txt'

# Load the list of required tracks
with open(track_ids_file, 'r') as f:
    required_tracks = [line.strip() for line in f]

# Function to compute SHA256 checksum


def compute_sha256(filename):
    with open(filename, 'rb') as f:
        contents = f.read()
        checksum = hashlib.sha256(contents).hexdigest()
        return checksum


# Read the checksum values for tracks
sha256_tracks_path = 'raw_30s_audio_sha256_tracks.txt'
sha256_tracks = {}
with open(sha256_tracks_path, 'r') as f:
    for line in f:
        checksum, filename = line.strip().split()
        sha256_tracks[filename] = checksum

# Function to extract required tracks from a tar file


def extract_required_tracks(tar_file_path, required_tracks, output_dir):
    with tarfile.open(tar_file_path, 'r') as tar:
        members = tar.getmembers()
        required_members = [m for m in members if m.name in required_tracks]

        for member in required_members:
            tar.extract(member, path=output_dir)
            extracted_file_path = os.path.join(output_dir, member.name)

            # Validate the checksum
            if compute_sha256(extracted_file_path) == sha256_tracks[member.name]:
                print(f'{member.name} extracted and validated successfully')
            else:
                print(f'{member.name} failed checksum validation, removing')
                os.remove(extracted_file_path)

        # Remove the tar file after extraction
        os.remove(tar_file_path)


# Directory to store the extracted audio files
output_directory = os.path.join(tar_files_directory, 'extracted_audio')
os.makedirs(output_directory, exist_ok=True)

# Process each tar file in the directory
for tar_file in os.listdir(tar_files_directory):
    if tar_file.endswith('.tar'):
        tar_file_path = os.path.join(tar_files_directory, tar_file)
        print(f'Processing {tar_file_path}')
        extract_required_tracks(
            tar_file_path, required_tracks, output_directory)

# Print completion message
print('Extraction complete')
