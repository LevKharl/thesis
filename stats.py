import os
import json
import re
import pandas as pd


def count_files_in_folder(folder_path):
    """
    Count the number of files in the specified folder.

    :param folder_path: Path to the folder
    :return: Number of files in the folder
    """
    try:
        # List all entries in the directory
        entries = os.listdir(folder_path)
        # Filter out only the files
        files = [entry for entry in entries if os.path.isfile(
            os.path.join(folder_path, entry))]
        # Return the count of files
        return len(files)
    except FileNotFoundError:
        return "The specified folder was not found."
    except Exception as e:
        return f"An error occurred: {e}"


path = 'parsed_web_pages'
print(f"Total number of tracks '{path}': {count_files_in_folder(path)}")

path = 'lyrics'
print(f"Number of lyrics '{path}': {count_files_in_folder(path)}")


def count_files_with_specific_description(folder_path):
    """
    Count the number of files in the specified folder that contain a specific type of description.

    :param folder_path: Path to the folder
    :return: Number of files with a specific description
    """
    description_count = 0

    try:
        # List all entries in the directory
        entries = os.listdir(folder_path)
        # Filter out only the files
        files = [entry for entry in entries if os.path.isfile(
            os.path.join(folder_path, entry))]

        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()

                    # Extract the JSON-LD script content
                    json_ld_match = re.search(
                        r'<script type="application/ld\+json">(.*?)</script>', data, re.DOTALL)

                    if json_ld_match:
                        json_ld_content = json_ld_match.group(1)
                        json_data = json.loads(json_ld_content)

                        # Extract the description
                        artist_description = json_data.get('byArtist', {}).get(
                            'description', 'Description not found')
                        if artist_description != 'Description not found':
                            # print("Description:", artist_description)
                            description_count += 1
                    # else:
                        # print("JSON-LD script block not found")
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Skip files that cannot be decoded as JSON or UTF-8
                continue
    except FileNotFoundError:
        return "The specified folder was not found."
    except Exception as e:
        return f"An error occurred: {e}"

    return description_count


# Example usage
folder_path = 'parsed_web_pages'
# print(
# f"Number of files with specific description: {count_files_with_specific_description(folder_path)}")


def count_short_descriptions(file_path, word_limit):
    """
    Count the number of descriptions in the CSV file that have fewer than a specified number of words.

    :param file_path: Path to the CSV file
    :param word_limit: Maximum number of words for the description to be considered short
    :return: Number of descriptions with fewer than the specified number of words
    """
    short_description_count = 0

    try:
        df = pd.read_csv(file_path)
        descriptions = df['description'].dropna()

        for description in descriptions:
            word_count = len(description.split())
            if word_count < word_limit:
                short_description_count += 1
    except FileNotFoundError:
        return "The specified file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

    return short_description_count


# Example usage
file_path = 'data/descriptions.csv'
word_limits = [1000, 500, 100, 50, 20, 5]

for limit in word_limits:
    count = count_short_descriptions(file_path, limit)
    print(
        f"Number of files with short descriptions (less than {limit} words): {count}")
