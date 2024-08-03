import pandas as pd

# Load the dataset
file_path = 'data/final_dataset.csv'
data = pd.read_csv(file_path)

# Split the TAGS column to create a list of tags for each track
data['TAGS'] = data['TAGS'].str.split('\t')

# Function to identify tracks with 'genre---electronic' tag


def has_electronic(tags):
    # Filter out empty tags and remove any leading/trailing spaces
    tags = [tag.strip() for tag in tags if tag]
    return 'genre---electronic' in tags


# Filter to get tracks with 'genre---electronic'
electronic_tracks = data[data['TAGS'].apply(has_electronic)]

# Sort electronic tracks by the number of tags
electronic_tracks['tag_count'] = electronic_tracks['TAGS'].apply(len)
electronic_tracks = electronic_tracks.sort_values(by='tag_count')

# Remove exactly 1000 tracks
tracks_to_remove = electronic_tracks.head(1000)
filtered_data = data[~data['TRACK_ID'].isin(tracks_to_remove['TRACK_ID'])]

# Save the filtered data back to a CSV file
filtered_data_path = 'data/rebalanced_dataset.csv'
filtered_data.to_csv(filtered_data_path, index=False)

removed_count = len(tracks_to_remove)
print(f'Removed {removed_count} tracks')
