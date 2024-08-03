import pandas as pd
import json

# Load the dataset
df = pd.read_csv('data/rebalanced_dataset.csv')

# Initialize an empty list to hold the JSON objects
jsonl_data = []

# Generate JSONL data
for index, row in df.iterrows():
    track_id = row['TRACK_ID']
    description = row['description']

    # Create the prompt for generating a prompt
    input_prompt = (
        f"Generate a detailed prompt for an AI music (track) generation model based on the following track information:\n"
        f"- Description: {description}\n\n"
        "The prompt should capture the essence of the track, including the mood, themes, and any distinctive musical elements. "
        "The output should be a single sentence that can be used as an input prompt for the AI music generation model. "
        "Ensure that the track length and any reference to an album are not mentioned in the output."
    )

    # Create JSON object
    json_obj = {
        'track_id': track_id,
        'input_prompt': input_prompt,
        'description': description
    }

    # Append the JSON object to the list
    jsonl_data.append(json_obj)

# Save to JSONL file
with open('data/prompts.jsonl', 'w') as f:
    for item in jsonl_data:
        f.write(json.dumps(item) + '\n')
