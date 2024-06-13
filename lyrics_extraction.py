import os
import pandas as pd
from bs4 import BeautifulSoup
import time

# set a timer
start = time.time()

# Folder containing the HTML files
folder_path = 'lyrics'

# List to hold track_id and lyrics
data = []

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        # filename = 'lyrics_0000215.html'
        # extract track_id = '0000215'
        track_id = filename.split('_')[-1].split('.')[0]
        track_id = "track_" + track_id
        file_path = os.path.join(folder_path, filename)

        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the div or any other tag that contains the lyrics
        lyrics_div = soup.find(
            'div', class_='col-sm-offset-2 col-sm-8 col-sm-offset-3 col-md-6')

        # Extract the text content of the lyrics
        if lyrics_div:
            lyrics = lyrics_div.get_text(separator='\n', strip=True)
        else:
            lyrics = None  # Handle case where lyrics are not found

        # Append track_id and lyrics to the data list
        data.append({'track_id': track_id, 'lyrics': lyrics})

# Create a DataFrame from the data list
df = pd.DataFrame(data, columns=['track_id', 'lyrics'])

# Save the DataFrame to a CSV file
output_csv = 'lyrics_dataset.csv'
df.to_csv(output_csv, index=False)

print(f'Dataset saved to {output_csv}')

# Calculate the elapsed time
end = time.time()
elapsed_time = end - start
print(f'Time taken: {elapsed_time:.2f} seconds')
