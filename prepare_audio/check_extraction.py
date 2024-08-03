import os

# Path to the directory where the extracted audio files are stored
output_directory = '/scratch/project_2008167/lev_thesis/audio/extracted_audio'
# Path to the file containing the list of required tracks
track_ids_file = 'track_ids_to_download.txt'

# Load the list of required tracks
with open(track_ids_file, 'r') as f:
    required_tracks = [line.strip() for line in f]

# Function to check if a file exists


def file_exists(file_path):
    return os.path.isfile(file_path)


# Check the existence of each required track
missing_tracks = []
for track in required_tracks:
    track_path = os.path.join(output_directory, track)
    if not file_exists(track_path):
        missing_tracks.append(track)

# Report the results
if missing_tracks:
    print(f"Missing tracks: {len(missing_tracks)}")
    for track in missing_tracks:
        print(track)
else:
    print("All required tracks are present.")

# Optionally, save the list of missing tracks to a file
missing_tracks_file = os.path.join(output_directory, 'missing_tracks.txt')
with open(missing_tracks_file, 'w') as f:
    for track in missing_tracks:
        f.write(track + '\n')
