import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
logger = logging.getLogger(__name__)

# Function to initialize Chrome WebDriver
def initialize_driver(chromedriver_path, chrome_profile_path):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--log-level=3")  # Disable logging from WebDriver
    driver_service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

# Function to visit a website and catch any exceptions
async def visit_website(driver, url):
    try:
        await driver.get(url)
        logger.info(f"Successfully visited {url}")
    except Exception as e:
        logger.error(f"Error visiting {url}: {str(e)}")

# Main asynchronous function to orchestrate tasks
async def main():
    chrome_profile_path = r"C:\ChromeProfile"
    chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"
    website_url = "https://9gag.com/"
    wait_time = 10  # Seconds to stay on the website

    # Initialize Chrome WebDriver
    driver = initialize_driver(chromedriver_path, chrome_profile_path)

    # Visit the website
    await visit_website(driver, website_url)

    # Wait for a specified time
    await asyncio.sleep(wait_time)
    logger.info(f"Stayed on the website for {wait_time} seconds")

    # Close the WebDriver
    driver.quit()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
