import os
import json
import re


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


path = 'lyrics'
print(f"Number of files in folder '{path}': {count_files_in_folder(path)}")


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
print(
    f"Number of files with specific description: {count_files_with_specific_description(folder_path)}")


def count_short_descriptions(folder_path, word_limit=2):
    """
    Count the number of files in the specified folder that contain descriptions with fewer than a specified number of words.

    :param folder_path: Path to the folder
    :param word_limit: Maximum number of words for the description to be considered short
    :return: Number of files with short descriptions
    """
    short_description_count = 0

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
                            # Count the number of words in the description
                            word_count = len(artist_description.split())
                            # print(
                            #     f"Description: has {word_count} words.")
                            if word_count < word_limit:
                                # print("Short Description:", artist_description)
                                short_description_count += 1
                    # else:
                        # print("JSON-LD script block not found")
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Error reading file {file}: {e}")
                # Skip files that cannot be decoded as JSON or UTF-8
                continue
    except FileNotFoundError:
        return "The specified folder was not found."
    except Exception as e:
        return f"An error occurred: {e}"

    return short_description_count


# Example usage
folder_path = 'parsed_web_pages'
word_limit = 1000
print(
    f"Number of files with short descriptions (less than {word_limit} words): {count_short_descriptions(folder_path, word_limit)}")
word_limit = 500
print(
    f"Number of files with short descriptions (less than {word_limit} words): {count_short_descriptions(folder_path, word_limit)}")
word_limit = 100
print(
    f"Number of files with short descriptions (less than {word_limit} words): {count_short_descriptions(folder_path, word_limit)}")
word_limit = 50
print(
    f"Number of files with short descriptions (less than {word_limit} words): {count_short_descriptions(folder_path, word_limit)}")
word_limit = 20
print(
    f"Number of files with short descriptions (less than {word_limit} words): {count_short_descriptions(folder_path, word_limit)}")
word_limit = 5
print(
    f"Number of files with short descriptions (less than {word_limit} words): {count_short_descriptions(folder_path, word_limit)}")
