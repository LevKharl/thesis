import requests
from bs4 import BeautifulSoup
import time


def fetch_web_page(url, retries=3, backoff_factor=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                print(soup.title.string)
                return soup
            else:
                print(
                    f"Failed to retrieve content from {url} with status code {response.status_code}")
                # Exponential backoff
                time.sleep(backoff_factor * (2 ** attempt))
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
    return None


# Example usage
url = 'http://www.jamendo.com/track/214'
page_content = fetch_web_page(url)
if page_content:
    print(page_content.prettify())
