from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def simple_navigation(url):
    chrome_driver_path = '/Users/kharlashkin/Downloads/chromedriver-mac-arm64/chromedriver'
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Comment out for debugging
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disables GPU hardware acceleration
    # Ensures consistent viewport size
    options.add_argument('--window-size=1920,1200')

    service = Service(chrome_driver_path, log_path='chromedriver.log')
    service.command_line_args().extend(['--verbose'])
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        print("Page title is:", driver.title)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


# Example usage
url = 'http://www.jamendo.com/track/214'
simple_navigation(url)
