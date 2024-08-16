from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

# Constants
TAG_HYPHEN = '---'
CATEGORIES = ['genre', 'instrument', 'mood/theme']
OUTPUT_DIR = 'parsed_web_pages'
PROGRESS_FILE = 'progress.txt'
LYRICS_OUTPUT_DIR = 'lyrics'

# Ensure the output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LYRICS_OUTPUT_DIR, exist_ok=True)


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


def save_progress(track_id):
    with open(PROGRESS_FILE, 'a') as f:
        f.write(f"{track_id}\n")


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
    chrome_driver_path = '/Users/kharlashkin/Downloads/chromedriver-mac-arm64/chromedriver'
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

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


def extract_lyrics_url(soup):
    lyrics_link = soup.find(
        'a', href=True, string=lambda text: text and 'Lyrics' in text)
    if lyrics_link:
        return 'http://www.jamendo.com' + lyrics_link['href']
    return None


def scrape_lyrics(url, retries=3):
    if not url:
        return None

    chrome_driver_path = '/Users/kharlashkin/Downloads/chromedriver-mac-arm64/chromedriver'
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

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


if __name__ == '__main__':
    link = 'https://www.jamendo.com/track/2966'
    page_content = scrape_dynamic_content(link)
    if page_content:
        lyrics_url = extract_lyrics_url(page_content)
        print(f"Lyrics URL: {lyrics_url}")
        if lyrics_url:
            lyrics = scrape_lyrics(lyrics_url)
            print(f"Lyrics: {lyrics}")
        else:
            print("Lyrics URL not found.")
    else:
        print("Failed to retrieve page content.")
