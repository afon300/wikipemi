from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

def initialize_driver():
    print("Starting Chrome browser...")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.implicitly_wait(5) # Wait up to 5s for an element to appear
        return driver
    except ValueError:
        print("❌ Error: Could not find or install the Chrome driver.")
        print("Make sure Google Chrome is installed on your system.")
        return None


def go_to_page(driver, url):
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        final_url = driver.current_url
        print(f"Final URL: {final_url}")
        return driver.page_source, final_url
    except WebDriverException as e:
        print(f"❌ Navigation error to {url}: {e}")
        return None, None