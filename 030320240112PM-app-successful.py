import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

# Paths for the Chrome profile and media directories
chrome_profile_path = "C:\\ChromeProfile"
pictures_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\pictures"
videos_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\videos"
chromedriver_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\chromedriver.exe"

async def download_file(file_url, folder_path):
    try:
        print(f"Starting download from: {file_url}")
        local_filename = file_url.split('/')[-1].split("?")[0]  # Remove URL parameters
        file_path = os.path.join(folder_path, local_filename)
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"File downloaded successfully and saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download the file: {e}")

async def find_and_download_media(driver, url):
    try:
        print(f"Accessing page: {url}")
        driver.get(url)
        print("Page loaded. Searching for the first article's media content...")
        
        # Wait for the dynamic content to load
        await asyncio.sleep(3)

        # Find the first <article> tag
        article = driver.find_element(By.CSS_SELECTOR, 'article')

        # Find the non-thumbnail image in the post-container div
        if article.find_elements(By.CSS_SELECTOR, 'div.post-container img'):
            print("Image found in the article.")
            media_url = article.find_element(By.CSS_SELECTOR, 'div.post-container img').get_attribute('src')
            await download_file(media_url, pictures_path)
        elif article.find_elements(By.CSS_SELECTOR, 'video source'):
            print("Video found in the article.")
            media_url = article.find_element(By.CSS_SELECTOR, 'video source').get_attribute('src')
            await download_file(media_url, videos_path)
        else:
            print("No image or video found in the first article.")
    except Exception as e:
        print(f"An error occurred while searching for media: {e}")

async def main():
    # Configure Chrome to use the provided Chrome profile
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--window-size=1920x1080")  # Specify window size
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources problem
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")



    # Initialize the WebDriver with the specified ChromeDriver executable
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # URL to open
        url = "https://9gag.com/top"
        # Wait for the dynamic content to load
        

        await find_and_download_media(driver, url)
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    finally:
        # Close the browser regardless of success or error
        print("Closing browser...")
        driver.quit()

# Run the main coroutine
asyncio.run(main())
