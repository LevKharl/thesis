import pandas as pd
import matplotlib.pyplot as plt

# Load the final dataset
final_dataset_file = 'data/final_dataset.csv'
df_final = pd.read_csv(final_dataset_file)

# Split the tags into a list
df_final['TAG_LIST'] = df_final['TAGS'].apply(lambda x: x.split('\t'))

# Function to remove prefixes from tags


def remove_prefix(tags, prefix):
    return [tag.replace(prefix, '') for tag in tags if tag.startswith(prefix)]

# Extract and count unique tags for each category without prefixes


def extract_tags(df, prefix):
    tags = df['TAG_LIST'].apply(lambda tags: remove_prefix(tags, prefix))
    tag_counts = tags.explode().value_counts()
    return tag_counts


# Get the counts for each tag type without prefixes
instrument_tag_counts = extract_tags(df_final, 'instrument---')
genre_tag_counts = extract_tags(df_final, 'genre---')
mood_theme_tag_counts = extract_tags(df_final, 'mood/theme---')

# Function to plot and save tag distribution


def plot_tag_distribution(tag_counts, title, xlabel, filename):
    plt.figure(figsize=(10, 6))
    tag_counts.plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f'{filename}.png')
    plt.close()


# Plotting and saving the distributions with appropriate filenames
plot_tag_distribution(instrument_tag_counts, 'Distribution of Instrument Tags',
                      'Instrument Tags', 'plots/instrument_tags_distribution')
plot_tag_distribution(
    genre_tag_counts, 'Distribution of Genre Tags', 'Genre Tags', 'plots/genre_tag_distribution')
plot_tag_distribution(mood_theme_tag_counts, 'Distribution of Mood/Theme Tags',
                      'Mood/Theme Tags', 'plots/mood_theme_tag_distribution')
