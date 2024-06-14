import pandas as pd
from mtg_jamendo_dataset.scripts import commons

# File paths
description_file = 'data/filtered_descriptions.csv'
initial_data = 'data/raw_30s_cleantags_50artists.tsv'

# Load the description data
description_df = pd.read_csv(description_file)

# Function to handle TSV with variable fields


def read_variable_tsv(filepath):
    data = []
    with open(filepath, 'r') as file:
        headers = file.readline().strip().split('\t')
        for line in file:
            values = line.strip().split('\t', len(headers) - 1)
            row = dict(zip(headers, values))
            data.append(row)
    return pd.DataFrame(data)


# Read the TSV file using the custom function
df_tsv = read_variable_tsv(initial_data)

# Merge the two DataFrames on track_id
df_final = pd.merge(df_tsv, description_df, how='inner',
                    left_on='TRACK_ID', right_on='track_id')

# Sort the final DataFrame by track_id
df_final.sort_values(by='TRACK_ID', inplace=True)

# Display the first few rows and the count of non-null values
print(df_final.head())
print(df_final.isnull().sum())
df_final = df_final.drop(columns=['track_id'])

# Save the final dataset to a new CSV file
final_dataset_file = 'data/final_dataset.csv'
df_final.to_csv(final_dataset_file, index=False)

# Identify and save the missing tracks
merged_track_ids = set(df_final['track_id'])
all_track_ids = set(description_df['track_id'])

missing_track_ids = all_track_ids - merged_track_ids
missing_descriptions = description_df[description_df['track_id'].isin(
    missing_track_ids)]

missing_file = 'data/missing_tracks.csv'
missing_descriptions.to_csv(missing_file, index=False)

print(f"Number of missing tracks: {len(missing_track_ids)}")
print(f"Missing tracks saved to {missing_file}")
