
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import tempfile
import shutil  # Add this import

# from mtg_jamendo_dataset.scripts import commons

# Constants
TAG_HYPHEN = '---'
CATEGORIES = ['genre', 'instrument', 'mood/theme']
OUTPUT_DIR = 'parsed_web_pages'
PROGRESS_FILE = 'progress.txt'
LYRICS_OUTPUT_DIR = 'lyrics'

# Ensure the output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LYRICS_OUTPUT_DIR, exist_ok=True)

# Load the data from the input file
input_file = 'data/raw_30s_cleantags_50artists.tsv'
# tracks, tags, extra = commons.read_file(input_file)


def read_metadata_file(tsv_file):
    metadata = {}
    with open(tsv_file, encoding='utf-8') as fp:
        reader = csv.reader(fp, delimiter='\t')
        next(reader, None)  # skip header
        for row in reader:
            track_id = get_id(row[0])
            metadata[track_id] = {
                'artist_id': get_id(row[1]),
                'album_id': get_id(row[2]),
                'track_name': row[3],
                'artist_name': row[4],
                'album_name': row[5],
                'release_date': row[6],
                'url': row[7]
            }
    return metadata


def get_id(identifier):
    return int(identifier.split('_')[-1])


# Read the raw metadata file
raw_metadata_file = 'data/raw.meta.tsv'
raw_metadata = read_metadata_file(raw_metadata_file)

# Function to save progress


def save_progress(track_id):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"{track_id}\n")

# Function to check progress


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()


# Load progress
completed_tracks = load_progress()


def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_dynamic_content(url, retries=3):

    # chrome_driver_path = r'C:/Users/levkh/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    chrome_driver_path = '/Users/kharlashkin/Downloads/chromedriver-mac-arm64/chromedriver'
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

    # Create a temporary directory for Chrome to use
    # temp_dir = tempfile.mkdtemp()
    # options.add_argument(f'--user-data-dir={temp_dir}')

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for attempt in range(retries):
            try:
                driver.get(url)
                print("Page loaded successfully.")

                scroll_to_bottom(driver)
                print("Scrolled to bottom and all content loaded.")

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                print("Page source retrieved successfully.")

                return soup
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)  # Wait before retrying
        return None

    finally:
        driver.quit()
        # Use shutil.rmtree to remove the directory and its contents
        # shutil.rmtree(temp_dir)


def extract_lyrics_url(soup):
    lyrics_link = soup.find(
        'a', href=True, string=lambda text: text and 'Lyrics' in text)
    if lyrics_link:
        return 'http://www.jamendo.com' + lyrics_link['href']
    return None


def scrape_lyrics(url, retries=3):
    if not url:
        return None

    # chrome_driver_path = r'C:/Users/levkh/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    chrome_driver_path = '/Users/kharlashkin/Downloads/chromedriver-mac-arm64/chromedriver'

    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

    # Create a temporary directory for Chrome to use
    # temp_dir = tempfile.mkdtemp()
    # options.add_argument(f'--user-data-dir={temp_dir}')

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for attempt in range(retries):
            try:
                driver.get(url)
                print("Lyrics page loaded successfully.")

                scroll_to_bottom(driver)
                print("Scrolled to bottom and all content loaded.")

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                print("Lyrics page source retrieved successfully.")

                return soup
            except Exception as e:
                print(f"Attempt {attempt + 1} to fetch lyrics failed: {e}")
                time.sleep(5)  # Wait before retrying
        return None

    finally:
        driver.quit()
        # Use shutil.rmtree to remove the directory and its contents
        # shutil.rmtree(temp_dir)


# Iterate through the filtered metadata and parse each web page
for track_id, data in raw_metadata.items():
    if str(track_id) in completed_tracks:
        print(f"Skipping track ID {track_id} as it is already processed.")
        continue

    url = data['url']
    print(f"Parsing web page for track ID {track_id} at URL {url}")
    page_content = scrape_dynamic_content(url)

    if page_content:
        # Save the parsed content to a file
        track_filename = f"{OUTPUT_DIR}/track_{track_id:07d}.html"
        with open(track_filename, 'w', encoding='utf-8') as f:
            f.write(page_content.prettify())
        print(f"Saved content for track ID {track_id} to {track_filename}")

        # Extract and save lyrics
        lyrics_url = extract_lyrics_url(page_content)
        if lyrics_url:
            lyrics = scrape_lyrics(lyrics_url)
            if lyrics:
                lyrics_filename = f"{LYRICS_OUTPUT_DIR}/lyrics_{track_id:07d}.html"
                with open(lyrics_filename, 'w', encoding='utf-8') as f:
                    f.write(lyrics.prettify())
                print(
                    f"Saved lyrics for track ID {track_id} to {lyrics_filename}")
            else:
                print(f"Failed to retrieve lyrics for track ID {track_id}")

        # Save progress
        save_progress(track_id)
        print(f"Progress saved for track ID {track_id}")
    else:
        print(f"Failed to retrieve content for track ID {track_id}")
