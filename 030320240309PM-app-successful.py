import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
import os
from time import time

# Paths for the Chrome profile and media directories
chrome_profile_path = r"C:\ChromeProfile"
pictures_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\pictures"
videos_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\videos"
chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"

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
        print(f"File downloaded and saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Download failed: {e}")

async def find_and_download_media(driver, scroll_pause_time):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        try:
            # Scroll down to the bottom of the page
            print("Scrolling down to load more articles...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load the page
            await asyncio.sleep(scroll_pause_time)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the end of the page or new content is taking too long to load.")
                break
            last_height = new_height
            
            # Download media from the newly loaded article
            articles = driver.find_elements(By.CSS_SELECTOR, 'article')
            last_article = articles[-1]
            print(f"Processing the last loaded article...")
            media_url = ''
            try:
                media_url = last_article.find_element(By.CSS_SELECTOR, 'div.post-container img').get_attribute('src')
            except NoSuchElementException:
                print("No image found in the article. Looking for video...")
                try:
                    media_url = last_article.find_element(By.CSS_SELECTOR, 'video source').get_attribute('src')
                except NoSuchElementException:
                    print("No video found in the article.")

            if media_url:
                if '.webp' in media_url or '.jpg' in media_url:
                    await download_file(media_url, pictures_path)
                elif '.mp4' in media_url:
                    await download_file(media_url, videos_path)

        except Exception as e:
            print(f"An error occurred while scrolling and downloading media: {e}")

async def main():
    
    

    # Configure Chrome to use the specified profile
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources problem
    options.add_argument("start-maximized")  # Maximize window to ensure all elements are in view
    options.add_argument("disable-infobars")  # Disable infobars
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    # Disable browser logging
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'browser': 'OFF'}
    
    
    # Initialize the WebDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # URL to open
        url = "https://9gag.com/"
        driver.get(url)
        await asyncio.sleep(5)  # Allow initial page content to load
        await find_and_download_media(driver, 5)  # Scroll and download media
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        print("Closing the browser...")
        driver.quit()

# Run the script
asyncio.run(main())
