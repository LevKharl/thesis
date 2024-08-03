import json


def rename_field(input_file_path, output_file_path):
    # Read the JSONL file
    with open(input_file_path, 'r') as f:
        data = [json.loads(line) for line in f]

    # Rename 'input_prompt' to 'prompt'
    renamed_data = [{'prompt': record['input_prompt']} for record in data]

    # Write the renamed data to a new JSONL file
    with open(output_file_path, 'w') as f:
        for record in renamed_data:
            f.write(json.dumps(record) + '\n')


# Define the file paths
input_file_path = 'data/prompts.jsonl'
output_file_path = 'data/input_prompts_only.jsonl'

# Run the renaming function
rename_field(input_file_path, output_file_path)
