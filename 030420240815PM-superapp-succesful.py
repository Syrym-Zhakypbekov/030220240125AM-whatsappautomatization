import asyncio
import os
import glob
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pyautogui
import pyperclip
import time
import logging

# Configuration and paths
chrome_profile_path = r"C:\ChromeProfile"
media_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\media"
chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"
forbidden_chars = '<>:"/\\|?*'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Open the window using Win + 2; ensure you have the desired window positioned at slot 2 in your taskbar
logger.info("Open the window using Win + 2; ensure you have the desired window positioned at slot 2 in your taskbar")
pyautogui.hotkey('win', '2')
time.sleep(2)  # Wait for the window to open; adjust the sleep time based on your system's speed

# Helper functions (sanitization, folder clearing, text file handling, etc.)
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

def find_first_text_file(directory_path):
    """Find the first text file in a directory."""
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))
    return txt_files[0] if txt_files else None

def read_text_file(file_path):
    """Read the content of a text file."""
    if file_path:
        with open(file_path, 'r') as file:
            return file.read()
    else:
        return ""

def automate_gui_actions(text, x_coord, y_coord):
    """Automate GUI actions with given text and coordinates."""
    if text:
         # Copy the text to clipboard
        logger.info("Copy the text to clipboard")
        pyperclip.copy(text)
        time.sleep(2)
        
        # Navigate to the specified coordinates and click to focus
        logger.info("Navigate to the specified coordinates and click to focus")
        pyautogui.click(x_coord, y_coord)
        time.sleep(1)  # Wait for any possible animation or loading
        
        # Paste the content from the clipboard
        logger.info("Paste the content from the clipboard")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)  # Wait for the paste action to complete
        
        # Press Enter
        logger.info("Press Enter")
        pyautogui.press('enter')
        time.sleep(2)
        # # # # # # # # # # # # # # # # # # # # # #
        logger.info("Waiting for 2 seconds before clicking")
        time.sleep(2)
        
        logger.info("Clicking on specified coordinates (X: 1357, Y: 988)")
        pyautogui.click(x=1261, y=990)
        
        logger.info("Waiting for 2 seconds before double-clicking")
        time.sleep(2)
        
        logger.info("Double-clicking on specified coordinates (X: 1375, Y: 790)")
        pyautogui.doubleClick(x=1257, y=792)
        
        logger.info("Waiting for 2 seconds before double-clicking again")
        time.sleep(2)
        
        logger.info("Double-clicking on specified coordinates (X: 992, Y: 501)")
        pyautogui.doubleClick(x=1214, y=383)
        
        logger.info("Waiting for 2 seconds before triggering Enter button")
        time.sleep(2)
        
        logger.info("Pressing Enter button")
        pyautogui.press('enter')
        
        logger.info("Clicking on specified coordinates (X: 1357, Y: 988)")
        pyautogui.click(x=1321, y=995)
        time.sleep(2)
        
        logger.info("All actions completed successfully")
        time.sleep(2)
    else:
        print("No text file found.")

# Download and processing functions
async def download_file(file_url, folder_path, post_title):
    # Similar to the first script's download_file function, with modifications to call the GUI automation
    
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
    # Similar to the first script's find_and_download_media function
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
                
        # Inside find_and_download_media function, after downloading a file:
        if media_url:
            # Download the media file and save the title
            await download_file(media_url, folder_path, post_title)
            x_coord = 1321
            y_coord = 995
            # Find the downloaded txt file and read its content
            txt_file_path = find_first_text_file(folder_path)
            text_content = read_text_file(txt_file_path)
            
            # Perform GUI actions with the content
            automate_gui_actions(text_content, x_coord, y_coord)  # Specify correct coordinates


        
        await download_file(media_url, folder_path, post_title)
async def main():
    # Setup browser and initiate media downloading, followed by GUI automation for pasting text into WhatsApp
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
if __name__ == "__main__":
    asyncio.run(main())
