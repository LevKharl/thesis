import pandas as pd

# Load the rebalanced dataset
rebalanced_dataset_path = 'data/rebalanced_dataset.csv'
rebalanced_data = pd.read_csv(rebalanced_dataset_path)

# Extract list of track IDs to download
track_ids_to_download = rebalanced_data['PATH'].tolist()

# Save the list of track IDs to a file
track_ids_file_path = 'data/track_ids_to_download.txt'
with open(track_ids_file_path, 'w') as f:
    for track_id in track_ids_to_download:
        f.write(f"{track_id}\n")

print(f"Track IDs saved to {track_ids_file_path}")
