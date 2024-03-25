# import asyncio
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException
# import requests
# import os
# 
# # Paths for the Chrome profile and media directories
# chrome_profile_path = r"C:\ChromeProfile"
# pictures_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\pictures"
# videos_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\videos"
# chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"
# 
# def clear_folder(folder_path, temp_title_file=None):
#     """Clear all files in the specified folder except for the current .txt file."""
#     for the_file in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, the_file)
#         if temp_title_file and file_path == temp_title_file:
#             continue  # Skip the temporary title file
#         try:
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#         except Exception as e:
#             print(e)
# 
# 
# async def download_file(file_url, folder_path, temp_title_file=None):
#     # Clear the target folder before downloading a new file
#     clear_folder(folder_path, temp_title_file=temp_title_file)
# 
#     
#     try:
#         print(f"Starting download from: {file_url}")
#         local_filename = file_url.split('/')[-1].split("?")[0]  # Remove URL parameters
#         file_path = os.path.join(folder_path, local_filename)
#         with requests.get(file_url, stream=True) as r:
#             r.raise_for_status()
#             with open(file_path, 'wb') as f:
#                 for chunk in r.iter_content(chunk_size=8192):
#                     f.write(chunk)
#         print(f"File downloaded and saved to: {file_path}")
#         
#         # If the download is successful, and there is a temp title file, delete it
#         if temp_title_file:
#             os.unlink(temp_title_file)
#         return local_filename  # Return the name of the downloaded file
#     except Exception as e:
#         print(f"Download failed: {e}")
#         return None
# 
# 
# async def find_and_download_media(driver, scroll_pause_time, temp_title_file=None):
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         await asyncio.sleep(scroll_pause_time)
#         
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             print("Reached the end of the page or new content is taking too long to load.")
#             break
#         last_height = new_height
#         
#         # Find the title of the last article
#         post_titles = driver.find_elements(By.CSS_SELECTOR, 'h2[data-v-7f40ae1b]')
#         if post_titles:
#             post_title = post_titles[-1].text  # Get the text of the last post title
#             print(f"Post title: {post_title}")
# 
#         articles = driver.find_elements(By.CSS_SELECTOR, 'article')
#         if articles:
#             last_article = articles[-1]
#             print("Processing the last loaded article...")
#             media_url = ''
#             folder_path = ''
# 
#             try:
#                 media_element = last_article.find_element(By.CSS_SELECTOR, 'div.post-container img')
#                 media_url = media_element.get_attribute('src')
#                 folder_path = pictures_path
#             except NoSuchElementException:
#                 try:
#                     media_element = last_article.find_element(By.CSS_SELECTOR, 'video source')
#                     media_url = media_element.get_attribute('src')
#                     folder_path = videos_path
#                 except NoSuchElementException:
#                     print("No image or video found in the article.")
#                     continue
# 
#         # If we found media, save the post title and download the file
#         if media_url:
#             # Clear the folder first but keep the .txt file
#             # clear_folder(folder_path, keep_txt=True)
#             # clear_folder(folder_path, temp_title_file=temp_title_file)
# 
#             
#             # Download the media file and get the filename
#             downloaded_filename = await download_file(media_url, folder_path)
#             
#             if downloaded_filename:
#                 # Construct the new title file path
#                 sanitized_title = "".join(x for x in post_title if x.isalnum() or x in " -_")
#                 new_title_file_path = os.path.join(folder_path, f"{sanitized_title}.txt")
#                 # new_title_file_path = os.path.join(folder_path, f"{downloaded_filename}.txt")
#                 
#                 # Delete old .txt file if exists
#                 txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
#                 for txt_file in txt_files:
#                     txt_file_path = os.path.join(folder_path, txt_file)
#                     os.unlink(txt_file_path)
#                 
#                 # Save the new post title to the .txt file
#                 try:
#                     with open(new_title_file_path, 'w') as f:
#                         f.write(post_title)
#                     print(f"Post title saved to: {new_title_file_path}")
#                 except Exception as e:
#                     print(f"Failed to save post title to file: {e}")
#             
#            
# 
#             # Download the media file
#             await download_file(media_url, folder_path)
#                 
# 
# async def main():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument(f"user-data-dir={chrome_profile_path}")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-infobars")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--log-level=3") 
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# 
#     service = Service(chromedriver_path)
#     driver = webdriver.Chrome(service=service, options=options)
# 
#     try:
#         driver.get("https://9gag.com/")
#         await asyncio.sleep(5)  # Wait for initial content to load
#         await find_and_download_media(driver, 5)  # Scroll and download media
#     except Exception as e:
#         print(f"Error during processing: {e}")
#     finally:
#         driver.quit()
#         print("Browser closed.")
# 
# asyncio.run(main())
# 
# 
# 
# 
# 
# 
# 

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Set up the paths for the necessary directories and files
pictures_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\pictures"
videos_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\videos"
chromedriver_path = r"C:\Users\syrym\Downloads\030220240125AM-whatsappautomatization\chromedriver.exe"

def clear_folder(folder_path):
    # Clear all files in the specified folder
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

def download_file(file_url, folder_path, post_title):
    # Clear the folder before downloading new file
    clear_folder(folder_path)
    
    # Start the download
    local_filename = file_url.split('/')[-1].split("?")[0]
    file_path = os.path.join(folder_path, local_filename)
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    # Save the title to a txt file
    title_file_path = os.path.join(folder_path, f"{post_title}.txt")
    with open(title_file_path, 'w') as f:
        f.write(post_title)

def setup_driver(chrome_profile_path):
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
    return driver

def find_media_and_download(driver, pictures_path, videos_path):
    # Get the last post title
    posts = driver.find_elements(By.CSS_SELECTOR, 'h2[data-v-7f40ae1b]')
    if posts:
        post_title = posts[-1].text.replace(' ', '_')
    else:
        return

    # Find the last article and its media
    articles = driver.find_elements(By.CSS_SELECTOR, 'article')
    if articles:
        last_article = articles[-1]
        try:
            media_element = last_article.find_element(By.CSS_SELECTOR, 'div.post-container img')
            media_url = media_element.get_attribute('src')
            download_file(media_url, pictures_path, post_title)
        except NoSuchElementException:
            try:
                media_element = last_article.find_element(By.CSS_SELECTOR, 'video source')
                media_url = media_element.get_attribute('src')
                download_file(media_url, videos_path, post_title)
            except NoSuchElementException:
                return

# Main script execution
if __name__ == "__main__":
    driver = setup_driver(chrome_profile_path)
    driver.get("https://9gag.com/")
    find_media_and_download(driver, pictures_path, videos_path)
    driver.quit()
