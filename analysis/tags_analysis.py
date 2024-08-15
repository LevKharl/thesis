import pandas as pd
import ast
from collections import Counter

# Load the final dataset
final_dataset_file = 'data/final_ready_dataset.csv'
df_final = pd.read_csv(final_dataset_file)

# Convert TAGS column from string representation of list to actual list
df_final['TAG_LIST'] = df_final['TAGS'].apply(lambda x: ast.literal_eval(x))

# Function to count tag frequencies


def count_tags(tag_list, prefix):
    return Counter(tag.replace(prefix, '') for tags in tag_list for tag in tags if tag.startswith(prefix))


# Count genre, mood/theme, and instrument tags
genre_tag_counts = count_tags(df_final['TAG_LIST'], 'genre---')
mood_theme_tag_counts = count_tags(df_final['TAG_LIST'], 'mood/theme---')
instrument_tag_counts = count_tags(df_final['TAG_LIST'], 'instrument---')

# Print stats for genre tags
print("Genre tag counts:")
for tag, count in genre_tag_counts.items():
    print(f"{tag}: {count}")

# Print stats for mood/theme tags
print("Mood/theme tag counts:")
for tag, count in mood_theme_tag_counts.items():
    print(f"{tag}: {count}")

# Print stats for instrument tags
print("Instrument tag counts:")
for tag, count in instrument_tag_counts.items():
    print(f"{tag}: {count}")

# Calculate new stats for overall tags
average_tags_per_track = df_final['TAG_LIST'].apply(len).mean()
count_instrument = df_final['TAG_LIST'].apply(lambda tags: any(
    tag.startswith('instrument---') for tag in tags)).sum()
count_genre = df_final['TAG_LIST'].apply(lambda tags: any(
    tag.startswith('genre---') for tag in tags)).sum()
count_mood_theme = df_final['TAG_LIST'].apply(lambda tags: any(
    tag.startswith('mood/theme---') for tag in tags)).sum()
unique_instrument_tags = set(
    tag for tags in df_final['TAG_LIST'] for tag in tags if tag.startswith('instrument---'))
unique_genre_tags = set(
    tag for tags in df_final['TAG_LIST'] for tag in tags if tag.startswith('genre---'))
unique_mood_theme_tags = set(
    tag for tags in df_final['TAG_LIST'] for tag in tags if tag.startswith('mood/theme---'))

# Print new stats
print(f"Average number of tags per track: {average_tags_per_track:.2f}")
print(f"Number of tracks with instrument tags: {count_instrument}")
print(f"Number of tracks with genre tags: {count_genre}")
print(f"Number of tracks with mood/theme tags: {count_mood_theme}")
print(f"Number of unique instrument tags: {len(unique_instrument_tags)}")
print(f"Number of unique genre tags: {len(unique_genre_tags)}")
print(f"Number of unique mood/theme tags: {len(unique_mood_theme_tags)}")
