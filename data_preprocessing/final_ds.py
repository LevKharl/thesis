import pandas as pd

# Load the dataset
df = pd.read_csv("data/cleaned_final_dataset.csv")

# Convert TAGS from string representation to list
df['TAGS'] = df['TAGS'].apply(lambda x: eval(x))

# Combine prompts with tags, handling cases where TAGS list might be empty


def create_input_text(row):
    if row['TAGS']:
        return f"[{row['TAGS'][0]}] {row['prompt']}"
    else:
        return row['prompt']


df['input_text'] = df.apply(create_input_text, axis=1)

# Save the combined dataset
df.to_csv("data/super_final_dataset.csv", index=False)
