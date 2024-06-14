import pandas as pd

# Load the final dataset
final_dataset_file = 'data/final_dataset.csv'
df_final = pd.read_csv(final_dataset_file)

# Split the tags into a list
df_final['TAG_LIST'] = df_final['TAGS'].apply(lambda x: x.split('\t'))

# Function to remove prefixes from tags


def remove_prefix(tags, prefix):
    return [tag.replace(prefix, '') for tag in tags if tag.startswith(prefix)]


# Calculate the total number of tags per track
df_final['TAG_COUNT'] = df_final['TAG_LIST'].apply(len)

# Calculate the average number of tags per track
average_tags_per_track = df_final['TAG_COUNT'].mean()

# Count tracks with instrument-related tags, genre-related tags, and mood/theme-related tags
df_final['HAS_INSTRUMENT'] = df_final['TAG_LIST'].apply(
    lambda tags: any('instrument---' in tag for tag in tags))
df_final['HAS_GENRE'] = df_final['TAG_LIST'].apply(
    lambda tags: any('genre---' in tag for tag in tags))
df_final['HAS_MOOD_THEME'] = df_final['TAG_LIST'].apply(
    lambda tags: any('mood/theme---' in tag for tag in tags))

count_instrument = df_final['HAS_INSTRUMENT'].sum()
count_genre = df_final['HAS_GENRE'].sum()
count_mood_theme = df_final['HAS_MOOD_THEME'].sum()

# Extract unique values for each type of tag and remove prefixes
unique_instrument_tags = set(
    tag.replace('instrument---', '') for tags in df_final['TAG_LIST'] for tag in tags if 'instrument---' in tag)
unique_genre_tags = set(
    tag.replace('genre---', '') for tags in df_final['TAG_LIST'] for tag in tags if 'genre---' in tag)
unique_mood_theme_tags = set(
    tag.replace('mood/theme---', '') for tags in df_final['TAG_LIST'] for tag in tags if 'mood/theme---' in tag)

# Print results
print(f"Average number of tags per track: {average_tags_per_track:.2f}")
print(f"Number of tracks with instrument tags: {count_instrument}")
print(f"Number of tracks with genre tags: {count_genre}")
print(f"Number of tracks with mood/theme tags: {count_mood_theme}")
print(f"Number of unique instrument tags: {len(unique_instrument_tags)}")
print(f"Number of unique genre tags: {len(unique_genre_tags)}")
print(f"Number of unique mood/theme tags: {len(unique_mood_theme_tags)}")

# Save the analysis results to a CSV file
analysis_results = {
    'average_tags_per_track': [average_tags_per_track],
    'count_instrument': [count_instrument],
    'count_genre': [count_genre],
    'count_mood_theme': [count_mood_theme],
    'unique_instrument_tags': [list(unique_instrument_tags)],
    'unique_genre_tags': [list(unique_genre_tags)],
    'unique_mood_theme_tags': [list(unique_mood_theme_tags)],
}

df_analysis = pd.DataFrame(analysis_results)
analysis_file = 'data/tag_analysis_results.csv'
df_analysis.to_csv(analysis_file, index=False)

print(f"Analysis results saved to {analysis_file}")
