import pandas as pd
import ast
from collections import Counter

# Load the final dataset
final_dataset_file = 'data/final_ready_dataset.csv'
df_final = pd.read_csv(final_dataset_file)

# Convert TAGS column from string representation of list to actual list
df_final['TAG_LIST'] = df_final['TAGS'].apply(lambda x: ast.literal_eval(x))

# Define the threshold
threshold = 100

# Your genre tag counts data
genre_tag_counts = {
    'pop': 2004, 'popfolk': 620, 'ambient': 2233, 'downtempo': 317, 'easylistening': 1209,
    'electronic': 2644, 'lounge': 684, 'triphop': 497, 'chillout': 1030, 'breakbeat': 103,
    'techno': 403, 'newage': 719, 'jazz': 816, 'fusion': 136, 'soundtrack': 2216, 'world': 541,
    'trance': 294, 'classical': 1431, 'orchestral': 800, 'folk': 885, 'instrumentalpop': 264,
    'chanson': 76, 'funk': 336, 'ethno': 156, 'blues': 280, 'metal': 272, 'rock': 1561,
    'alternative': 1025, 'indie': 709, 'rnb': 138, 'dub': 98, 'experimental': 1401, 'reggae': 139,
    'darkwave': 70, 'gothic': 70, 'newwave': 35, 'hardrock': 120, 'hard': 35, 'progressive': 341,
    'ethnicrock': 28, 'hiphop': 787, 'idm': 73, 'contemporary': 101, 'oriental': 36, 'minimal': 117,
    'celtic': 118, 'groove': 65, 'ska': 12, 'poprock': 637, 'grunge': 167, 'dance': 519,
    'postrock': 105, 'symphonic': 172, 'punkrock': 110, 'rocknroll': 54, 'jazzfunk': 37,
    'psychedelic': 249, 'country': 111, 'electropop': 182, 'house': 315, 'atmospheric': 446,
    'industrial': 142, 'drumnbass': 82, 'tribal': 70, 'worldfusion': 38, 'synthpop': 111,
    'darkambient': 189, 'club': 116, 'alternativerock': 39, 'disco': 40, 'instrumentalrock': 116,
    'improvisation': 106, 'latin': 125, 'rap': 246, 'acidjazz': 56, 'singersongwriter': 261,
    'medieval': 37, 'eurodance': 40, 'choir': 50, 'edm': 98, 'deephouse': 77, 'bossanova': 46,
    'swing': 50, '70s': 29, 'soul': 168, 'electronica': 75, 'classicrock': 55, 'african': 31,
    'jazzfusion': 99, 'dubstep': 91, 'bluesrock': 22, '60s': 30, '90s': 48, '80s': 51,
    'heavymetal': 33
}

# Mood/theme tag counts data
mood_theme_tag_counts = {
    'background': 83, 'film': 342, 'melodic': 231, 'children': 226, 'relaxing': 393,
    'heavy': 35, 'dark': 512, 'calm': 155, 'dramatic': 101, 'epic': 323, 'powerful': 71,
    'inspiring': 311, 'upbeat': 218, 'uplifting': 307, 'soundscape': 236, 'emotional': 285,
    'slow': 281, 'love': 267, 'drama': 112, 'horror': 55, 'adventure': 158, 'nature': 71,
    'funny': 90, 'happy': 525, 'positive': 197, 'fun': 117, 'melancholic': 156, 'romantic': 180,
    'hopeful': 63, 'sad': 233, 'documentary': 174, 'soft': 119, 'dream': 241, 'meditative': 259,
    'advertising': 281, 'corporate': 276, 'ballad': 89, 'action': 131, 'energetic': 366,
    'travel': 59, 'space': 104, 'cool': 100, 'commercial': 104, 'sport': 78, 'mellow': 35,
    'sexy': 38, 'christmas': 208, 'groovy': 38, 'fast': 55, 'retro': 32, 'ambiental': 51,
    'party': 78, 'movie': 170, 'motivational': 216, 'game': 48, 'holiday': 40, 'deep': 65,
    'trailer': 120, 'summer': 42
}

# Instrument tag counts data
instrument_tag_counts = {
    'synthesizer': 2047, 'beat': 104, 'voice': 540, 'guitar': 1295, 'computer': 854,
    'keyboard': 588, 'bass': 1591, 'saxophone': 344, 'piano': 2012, 'pipeorgan': 91,
    'trumpet': 450, 'rhodes': 334, 'cello': 444, 'violin': 562, 'acousticbassguitar': 68,
    'electricguitar': 1400, 'acousticguitar': 581, 'sampler': 223, 'harp': 308,
    'accordion': 124, 'drummachine': 559, 'flute': 341, 'clarinet': 234, 'drums': 1701,
    'orchestra': 252, 'electricpiano': 449, 'strings': 509, 'ukulele': 158, 'organ': 48,
    'classicalguitar': 266, 'harmonica': 65, 'horn': 196, 'viola': 74, 'brass': 289,
    'trombone': 262, 'percussion': 220, 'oboe': 89, 'bell': 256, 'bongo': 182,
    'doublebass': 116, 'pad': 71
}

# Filter the tags based on the threshold
selected_genre_tags = {f'genre---{tag}' for tag,
                       count in genre_tag_counts.items() if count >= threshold}
selected_mood_theme_tags = {f'mood/theme---{tag}' for tag,
                            count in mood_theme_tag_counts.items() if count >= threshold}
selected_instrument_tags = {f'instrument---{tag}' for tag,
                            count in instrument_tag_counts.items() if count >= threshold}

# Combine all selected tags
selected_tags = selected_genre_tags | selected_mood_theme_tags | selected_instrument_tags

# Function to filter tags based on selected tags


def filter_tags(tags, selected_tags):
    return [tag for tag in tags if tag in selected_tags]


# Apply the filter to TAG_LIST
df_final['TAG_LIST'] = df_final['TAG_LIST'].apply(
    lambda tags: filter_tags(tags, selected_tags))

# Combine TAG_LIST back into a single string, or set to empty list if no tags remain
df_final['TAGS'] = df_final['TAG_LIST'].apply(
    lambda tags: str(tags) if tags else '[]')

# Save the cleaned dataset to a new CSV file
cleaned_dataset_file = 'data/cleaned_final_dataset.csv'
df_final.to_csv(cleaned_dataset_file, index=False)

print(f"Cleaned dataset saved to {cleaned_dataset_file}")

# Print selected tags
print("Selected Genre Tags:")
for tag in selected_genre_tags:
    print(tag)

print("\nSelected Mood/Theme Tags:")
for tag in selected_mood_theme_tags:
    print(tag)

print("\nSelected Instrument Tags:")
for tag in selected_instrument_tags:
    print(tag)
