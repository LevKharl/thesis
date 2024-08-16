import pandas as pd
import json

# Load the dataset
df = pd.read_csv('data/rebalanced_dataset.csv')

# List of 50 different prompts
prompts = [
    "Create a detailed prompt for an AI music generation model using the following track details:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and key musical elements in one sentence. Avoid mentioning track length or album references.",
    "Develop a prompt for an AI music generation model using the provided track details:\n- Description: {description} /nThe prompt should succinctly convey the track's mood, themes, and distinctive musical features. Do not include track length or album references.",
    "Formulate a prompt for an AI music generation model based on the following track details:\n- Description: {description} /nEnsure the prompt captures the track's mood, themes, and unique musical characteristics in a single sentence. Exclude any mention of track length or album.",
    "Create a single-sentence prompt for an AI music generation model using this track information:\n- Description: {description} /nThe prompt should reflect the essence of the track, including its mood, themes, and musical elements, without referencing track length or album.",
    "Generate a prompt for an AI music generation model with the following track description:\n- Description: {description} /nThe prompt should capture the mood, themes, and musical essence in one sentence. Avoid mentioning track length or album.",
    "Develop a prompt for an AI music model using the given track information:\n- Description: {description} /nCraft a sentence that captures the track's mood, themes, and musical elements, without including track length or album references.",
    "Create a detailed AI music generation model prompt based on this track description:\n- Description: {description} /nThe prompt should encapsulate the mood, themes, and distinctive musical elements in one sentence, with no reference to track length or album.",
    "Write a prompt for an AI music model using the following track description:\n- Description: {description} /nThe prompt should summarize the track's mood, themes, and musical characteristics in a single sentence, without mentioning track length or album.",
    "Generate an AI music model prompt based on the following track details:\n- Description: {description} /nThe prompt should capture the track's mood, themes, and unique musical elements in a concise sentence, excluding track length or album references.",
    "Formulate a single-sentence prompt for an AI music model using this track information:\n- Description: {description} /nThe prompt should encapsulate the mood, themes, and key musical elements, without referring to track length or album.",
    "Create a detailed AI music prompt based on the following track information:\n- Description: {description} /nThe prompt should summarize the mood, themes, and distinctive musical elements in one sentence, without including track length or album references.",
    "Develop a concise prompt for an AI music generation model using this track description:\n- Description: {description} /nEnsure the prompt captures the essence of the track, including mood, themes, and musical elements, without referencing track length or album.",
    "Write a prompt for an AI music generation model using the given track details:\n- Description: {description} /nThe prompt should capture the mood, themes, and key musical elements in a single sentence, excluding any mention of track length or album.",
    "Formulate a prompt for an AI music model using this track information:\n- Description: {description} /nCraft a sentence that encapsulates the track's mood, themes, and unique musical characteristics, without mentioning track length or album.",
    "Generate a detailed AI music model prompt based on the following track description:\n- Description: {description} /nThe prompt should succinctly convey the track's mood, themes, and musical elements in one sentence, with no reference to track length or album.",
    "Create a single-sentence prompt for an AI music generation model using this track information:\n- Description: {description} /nThe prompt should capture the track's mood, themes, and distinctive musical features, without mentioning track length or album.",
    "Write a prompt for an AI music model based on the following track details:\n- Description: {description} /nThe prompt should summarize the mood, themes, and key musical elements in one sentence, excluding references to track length or album.",
    "Develop an AI music generation prompt using the provided track description:\n- Description: {description} /nCraft a sentence that encapsulates the track's mood, themes, and musical essence, without mentioning track length or album.",
    "Generate a prompt for an AI music model based on this track information:\n- Description: {description} /nThe prompt should capture the mood, themes, and distinctive musical elements in a single sentence, excluding any reference to track length or album.",
    "Create a detailed AI music generation model prompt using the given track description:\n- Description: {description} /nEnsure the prompt encapsulates the track's mood, themes, and musical elements, without referencing track length or album.",
    "Formulate a single-sentence prompt for an AI music model with this track information:\n- Description: {description} /nThe prompt should summarize the track's mood, themes, and key musical features, excluding any mention of track length or album.",
    "Write a prompt for an AI music generation model using this track description:\n- Description: {description} /nCraft a sentence that captures the track's mood, themes, and musical elements, without referencing track length or album.",
    "Generate a prompt for an AI music model based on the following track details:\n- Description: {description} /nThe prompt should encapsulate the mood, themes, and distinctive musical characteristics in one sentence, with no reference to track length or album.",
    "Create a detailed AI music prompt using this track information:\n- Description: {description} /nThe prompt should summarize the track's mood, themes, and key musical elements in a single sentence, without including references to track length or album.",
    "Write a single-sentence prompt for an AI music generation model using the given track details:\n- Description: {description} /nThe prompt should capture the mood, themes, and distinctive musical elements, without mentioning track length or album.",
    "Develop a concise prompt for an AI music generation model based on this track description:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and musical essence in one sentence, without referencing track length or album.",
    "Formulate a prompt for an AI music model with the following track description:\n- Description: {description} /nCraft a sentence that captures the mood, themes, and key musical elements, without mentioning track length or album.",
    "Create a detailed AI music generation model prompt based on this track information:\n- Description: {description} /nThe prompt should succinctly convey the track's mood, themes, and musical characteristics in a single sentence, excluding references to track length or album.",
    "Generate a single-sentence prompt for an AI music model using the provided track description:\n- Description: {description} /nThe prompt should capture the mood, themes, and distinctive musical features, without referencing track length or album.",
    "Write a prompt for an AI music generation model using this track information:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and key musical elements in one sentence, excluding any mention of track length or album.",
    "Develop a detailed AI music generation model prompt based on the following track description:\n- Description: {description} /nEnsure the prompt captures the mood, themes, and distinctive musical elements in a single sentence, without including track length or album references.",
    "Create a concise prompt for an AI music model using the given track details:\n- Description: {description} /nThe prompt should reflect the track's mood, themes, and musical essence in one sentence, excluding references to track length or album.",
    "Generate a prompt for an AI music generation model with the following track description:\n- Description: {description} /nThe prompt should summarize the mood, themes, and key musical elements in one sentence, without mentioning track length or album.",
    "Formulate a single-sentence prompt for an AI music model using this track description:\n- Description: {description} /nCraft a sentence that captures the track's mood, themes, and distinctive musical elements, without referencing track length or album.",
    "Write a prompt for an AI music generation model using the provided track information:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and musical characteristics in a concise sentence, excluding any reference to track length or album.",
    "Develop a detailed AI music prompt based on the following track details:\n- Description: {description} /nEnsure the prompt captures the mood, themes, and key musical elements in one sentence, without mentioning track length or album.",
    "Generate a prompt for an AI music model using this track description:\n- Description: {description} /nThe prompt should succinctly convey the track's mood, themes, and distinctive musical elements, without referencing track length or album.",
    "Create a single-sentence prompt for an AI music generation model with the following track information:\n- Description: {description} /nThe prompt should capture the track's mood, themes, and musical characteristics, excluding any reference to track length or album.",
    "Write a prompt for an AI music model based on this track description:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and key musical elements in one sentence, without mentioning track length or album.",
    "Formulate a concise prompt for an AI music generation model using the given track details:\n- Description: {description} /nThe prompt should reflect the mood, themes, and musical essence of the track, without including track length or album references.",
    "Create a prompt for an AI music generation model using this track information:\n- Description: {description} /nCraft a sentence that captures the track's mood, themes, and distinctive musical elements, excluding references to track length or album.",
    "Generate a single-sentence prompt for an AI music model based on the provided track description:\n- Description: {description} /nThe prompt should summarize the track's mood, themes, and musical characteristics, without referencing track length or album.",
    "Write a detailed AI music prompt using this track description:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and distinctive musical elements in one sentence, without mentioning track length or album.",
    "Develop a prompt for an AI music generation model using the following track information:\n- Description: {description} /nThe prompt should reflect the track's mood, themes, and key musical elements, excluding references to track length or album.",
    "Create a concise prompt for an AI music model using this track description:\n- Description: {description} /nThe prompt should capture the track's mood, themes, and musical characteristics, without mentioning track length or album.",
    "Generate a detailed prompt for an AI music generation model based on the given track details:\n- Description: {description} /nEnsure the prompt encapsulates the track's mood, themes, and distinctive musical elements in one sentence, excluding any reference to track length or album.",
    "Write a prompt for an AI music model using this track information:\n- Description: {description} /nCraft a sentence that summarizes the track's mood, themes, and musical essence, without mentioning track length or album.",
    "Formulate a single-sentence prompt for an AI music generation model with the following track description:\n- Description: {description} /nThe prompt should capture the track's mood, themes, and key musical elements, excluding references to track length or album.",
    "Create a prompt for an AI music model using this track description:\n- Description: {description} /nThe prompt should encapsulate the track's mood, themes, and distinctive musical elements in one sentence, without mentioning track length or album.",
    "Generate a concise prompt for an AI music generation model based on the following track details:\n- Description: {description} /nEnsure the prompt reflects the track's mood, themes, and musical characteristics in one sentence, excluding references to track length or album."
]


# Initialize an empty list to hold the JSON objects
jsonl_data = []

# Generate JSONL data
for index, row in df.iterrows():
    track_id = row['TRACK_ID']
    description = row['description']

    # Select the appropriate prompt for this iteration
    current_prompt = prompts[index % len(prompts)]

    # Create the input prompt by substituting the description
    input_prompt = current_prompt.replace("{description}", description)

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
