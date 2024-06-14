import os
import json
import re
import csv
import html


def remove_emojis(text):
    """
    Remove emojis from the text.
    """
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def preprocess_description(description):
    """
    Preprocess the description by unescaping HTML entities and removing unwanted content.
    """
    # Unescape HTML entities
    description = html.unescape(description)

    # Remove email addresses
    description = re.sub(r'\S+@\S+', '', description)

    # Remove URLs
    description = re.sub(r'http\S+|www.\S+', '', description)

    # Remove phone numbers
    description = re.sub(r'\b\d{10}\b', '', description)

    # Remove bank account numbers
    description = re.sub(r'\b\d{16}\b', '', description)

    # Remove specific unwanted words and phrases
    unwanted_words = [
        'Other Links:', 'Bandcamp', 'Soundcloud', 'CDBaby', 'Spotify', 'Youtube',
        'Facebook', 'Mail', 'Website', 'iTunes:', 'INSTAGRAM:', 'TikTok:', 'WIKIPEDIA', 'Telegram',
        'Twitter', 'Instagram', 'Facebook', 'YouTube', 'Spotify', 'Apple Music', 'Amazon Music',
        'Deezer', 'Tidal', 'Pandora', 'Google Play', 'Soundcloud', 'Bandcamp', 'iTunes', 'Follow',
        'Subscribe', 'Listen', 'Stream', 'Download', 'Buy', 'Support', 'Donate', 'Check out',
        'YOUTUBE', 'SPOTIFY', 'INSTAGRAM', 'FACEBOOK', 'TWITTER', 'SOUNDCLOUD', 'BANDCAMP', 'ITUNES',
        'AMAZON', 'APPLE MUSIC', 'DEEZER', 'TIDAL', 'PANDORA', 'GOOGLE PLAY', 'YOUTUBE MUSIC', 'YOUTUBE CHANNEL',
        'SPOTIFY PLAYLIST', 'INSTAGRAM PROFILE', 'FACEBOOK PAGE', 'TWITTER PROFILE', 'SOUNDCLOUD PROFILE'
    ]

    # Compile regex patterns for performance
    unwanted_pattern = re.compile(
        r'\b(?:' + '|'.join(unwanted_words) + r')\b', flags=re.IGNORECASE)
    repeating_colons_pattern = re.compile(r'(:\s*:)+')
    repeating_dashes_pattern = re.compile(r'(-\s*-)+')
    br_tag_pattern = re.compile(r'<br\s*/?>')
    # Pattern to remove sequences like '•••'
    dots_pattern = re.compile(r'[•]+')
    # Pattern to remove repeating dots like '...'
    repeating_dots_pattern = re.compile(r'\.{2,}')
    # Pattern to remove sequences like '/>====='
    separators_pattern = re.compile(r'/>\s*={5,}')

    description = unwanted_pattern.sub('', description)
    description = repeating_colons_pattern.sub(':', description)
    description = repeating_dashes_pattern.sub('-', description)
    description = br_tag_pattern.sub(' ', description)
    description = dots_pattern.sub('', description)
    description = repeating_dots_pattern.sub('', description)
    description = separators_pattern.sub('', description)

    # Remove any remaining unwanted text patterns
    description = re.sub(r'Check out other projects as well:.*',
                         '', description, flags=re.IGNORECASE)

    # Remove emojis
    description = remove_emojis(description)

    # Remove extra whitespace and leading/trailing punctuation
    description = re.sub(r'\s+', ' ', description).strip()
    description = re.sub(r'^[\W_]+|[\W_]+$', '', description)

    return description


def extract_descriptions(folder_path, min_word_limit, max_word_limit):
    """
    Extract descriptions from parsed web-pages and save to a CSV file.
    """
    short_descriptions = []

    try:
        # List all entries in the directory
        entries = os.listdir(folder_path)
        # Filter out only the files
        files = [entry for entry in entries if os.path.isfile(
            os.path.join(folder_path, entry))]

        for file in files:
            if not file.endswith('.html'):
                continue

            track_id = file.split('_')[-1].split('.')[0]
            track_id = "track_" + track_id
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

                        # Extract the description from the context if available
                        artist_description = None
                        if '@context' in json_data:
                            artist_description = json_data.get(
                                'byArtist', {}).get('description')

                        # If no context-specific description is found, fallback to other descriptions
                        if not artist_description:
                            if 'inAlbum' in json_data and isinstance(json_data['inAlbum'], list):
                                for album in json_data['inAlbum']:
                                    if 'description' in album:
                                        artist_description = album['description']
                                        break

                        if artist_description:
                            # Preprocess the description
                            artist_description = preprocess_description(
                                artist_description)
                            # Count the number of words in the description
                            word_count = len(artist_description.split())
                            if min_word_limit <= word_count <= max_word_limit:
                                short_descriptions.append({
                                    "track_id": track_id,
                                    "description": artist_description
                                })

            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Error reading file {file}: {e}")
                # Skip files that cannot be decoded as JSON or UTF-8
                continue
    except FileNotFoundError:
        return "The specified folder was not found."
    except Exception as e:
        return f"An error occurred: {e}"

    # Save descriptions to CSV
    csv_file_path = os.path.join(folder_path, 'descriptions.csv')
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['track_id', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for desc in short_descriptions:
                writer.writerow(desc)
    except Exception as e:
        return f"An error occurred while writing to the CSV file: {e}"

    return f"{len(short_descriptions)} short descriptions saved to {csv_file_path}"


# Example usage
folder_path = 'parsed_web_pages'
min_word_limit = 20
max_word_limit = 1000

result = extract_descriptions(folder_path, min_word_limit, max_word_limit)
print(result)
