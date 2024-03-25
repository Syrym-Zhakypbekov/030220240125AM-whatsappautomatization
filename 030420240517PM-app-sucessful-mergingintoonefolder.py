import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import requests
import os

# Paths for the Chrome profile and media directory
chrome_profile_path = r"C:\ChromeProfile"
media_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\media"
chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"

# Forbidden characters in Windows filenames
forbidden_chars = '<>:"/\\|?*'

def sanitize_filename(filename):
    """Sanitize filename by replacing forbidden characters with underscores."""
    return ''.join('_' if c in forbidden_chars else c for c in filename)

def clear_folder(folder_path):
    """Clear all files in the specified folder."""
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

async def download_file(file_url, folder_path, post_title):
    
    # Clear the target folder before downloading a new file
    clear_folder(folder_path)
    
    """Download file and save post title to a txt file in the specified folder."""
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        print(f"Starting download from: {file_url}")
        local_filename = sanitize_filename(file_url.split('/')[-1].split("?")[0])  # Remove URL parameters and sanitize
        file_path = os.path.join(folder_path, local_filename)
        
        # Download the media file
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"File downloaded and saved to: {file_path}")
        
        # Save the title to a txt file
        sanitized_title = sanitize_filename(post_title)
        if not sanitized_title.strip():
            sanitized_title = "salych is gay"  # Default title if post title is not usable
        title_file_path = os.path.join(folder_path, f"{sanitized_title}.txt")
        with open(title_file_path, 'w') as f:
            f.write(post_title)
        print(f"Title saved to: {title_file_path}")
        
        return local_filename  # Return the name of the downloaded file
    except Exception as e:
        print(f"Download failed: {e}")
        return None

async def find_and_download_media(driver, scroll_pause_time):
    """Find and download media from the page."""
    # Implementation remains the same as in your original script, 
    # but replace `pictures_path` and `videos_path` with `media_path`.
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the end of the page or new content is taking too long to load.")
            break
        last_height = new_height
        
        # Get the last post title
        print("Processing the last post of article...")
        posts = driver.find_elements(By.CSS_SELECTOR, 'h2[data-v-7f40ae1b]')
        if posts:
            post_title = posts[-1].text if posts else "funny_meme"
            print(f"Post title: {post_title}")
        else:
            return print(f"Problems with renaming the last post of article: cant use these characters:")

        articles = driver.find_elements(By.CSS_SELECTOR, 'article')
        if articles:
            last_article = articles[-1]
            print("Processing the last loaded article...")
            media_url = ''
            folder_path = ''

            try:
                media_element = last_article.find_element(By.CSS_SELECTOR, 'div.post-container img')
                media_url = media_element.get_attribute('src')
                folder_path = media_path
            except NoSuchElementException:
                try:
                    media_element = last_article.find_element(By.CSS_SELECTOR, 'video source')
                    media_url = media_element.get_attribute('src')
                    folder_path = media_path
                except NoSuchElementException:
                    print("No image or video found in the article.")
                    continue

        
        await download_file(media_url, folder_path, post_title)

async def main():
    """Main function to setup browser and download media."""
    # Setup and instantiation of the browser remains the same as in your original script.
    # Make sure to replace usage of `pictures_path` and `videos_path` with `media_path`.
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

# Ensure asyncio.run(main()) is called under a conditional block to avoid errors when importing this script elsewhere.
if __name__ == "__main__":
    asyncio.run(main())
