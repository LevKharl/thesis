import pandas as pd

# Paths to the input files
tsv_file_path = 'data/raw_30s_cleantags_50artists.tsv'
lyrics_csv_path = 'lyrics_dataset.csv'

# Read the TSV file
df_tsv = pd.read_csv(tsv_file_path, sep='\t')

# Read the CSV file with lyrics
df_lyrics = pd.read_csv(lyrics_csv_path)

# Merge the two DataFrames on track_id
df_final = pd.merge(df_tsv, df_lyrics, how='left', left_on='TRACK_ID', right_on='track_id')

# Drop the redundant track_id column from lyrics dataset
df_final.drop(columns=['track_id'], inplace=True)

# Save the final merged DataFrame to a new TSV file
output_tsv = 'final_dataset_with_lyrics.tsv'
df_final.to_csv(output_tsv, sep='\t', index=False)

print(f'Final dataset saved to {output_tsv}')
