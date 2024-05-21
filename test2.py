import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


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


def scrape_dynamic_content_with_scroll(url):
    chrome_driver_path = '/Users/kharlashkin/Downloads/chromedriver-mac-arm64/chromedriver'
    options = Options()
    # Comment out headless for debugging
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

    service = Service(chrome_driver_path, log_path='chromedriver.log')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        print("Page loaded successfully.")

        # Scroll to the bottom of the page to load all content
        scroll_to_bottom(driver)
        print("Scrolled to bottom and all content loaded.")

        # Get the page source after the content has loaded
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print("Page source retrieved successfully.")

        # Process the whole page content as needed
        print(soup.prettify())  # Print the entire HTML for debugging

        return soup

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()


# Example usage
url = 'http://www.jamendo.com/track/214'
scrape_dynamic_content_with_scroll(url)
