import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import requests
import os

# Paths for the Chrome profile and media directories
chrome_profile_path = r"C:\ChromeProfile"
pictures_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\pictures"
videos_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\videos"
chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"

def clear_folder(folder_path):
    """Clear all files in the specified folder."""
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

async def download_file(file_url, folder_path):
    # Clear the target folder before downloading a new file
    clear_folder(folder_path)
    
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
    except Exception as e:
        print(f"Download failed: {e}")

async def find_and_download_media(driver, scroll_pause_time):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the end of the page or new content is taking too long to load.")
            break
        last_height = new_height
        
        articles = driver.find_elements(By.CSS_SELECTOR, 'article')
        if articles:
            last_article = articles[-1]
            print("Processing the last loaded article...")
            media_url = ''
            try:
                media_url = last_article.find_element(By.CSS_SELECTOR, 'div.post-container img').get_attribute('src')
                folder_path = pictures_path
            except NoSuchElementException:
                print("No image found in the article. Looking for video...")
                try:
                    media_url = last_article.find_element(By.CSS_SELECTOR, 'video source').get_attribute('src')
                    folder_path = videos_path
                except NoSuchElementException:
                    print("No video found in the article.")
                    continue

            await download_file(media_url, folder_path)

async def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://9gag.com/")
        await asyncio.sleep(5)  # Wait for initial content to load
        await find_and_download_media(driver, 5)  # Scroll and download media
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

asyncio.run(main())






