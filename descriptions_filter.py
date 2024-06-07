import pandas as pd


def filter_short_descriptions(file_path, word_limit, output_file_path):
    """
    Filter descriptions in the CSV file that have fewer than a specified number of words and save to a new CSV file.

    :param file_path: Path to the input CSV file
    :param word_limit: Maximum number of words for the description to be included in the new CSV file
    :param output_file_path: Path to the output CSV file
    """
    try:
        df = pd.read_csv(file_path)
        descriptions = df['description'].dropna()  # Drop null descriptions

        short_descriptions = df[descriptions.apply(
            lambda x: len(x.split()) < word_limit)]

        short_descriptions.to_csv(output_file_path, index=False)
        print(f"Filtered dataset saved to {output_file_path}")

    except FileNotFoundError:
        print("The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
file_path = 'data/descriptions.csv'
output_file_path = 'data/filtered_descriptions.csv'
word_limit = 100

filter_short_descriptions(file_path, word_limit, output_file_path)
