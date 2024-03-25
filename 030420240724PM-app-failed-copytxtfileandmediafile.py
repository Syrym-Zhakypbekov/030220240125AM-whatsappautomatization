import os
import glob
import pyautogui
import pyperclip
import time
import logging

# Function to find files in a directory by extension
def find_files_by_extension(directory_path, extensions):
    all_files = []
    for ext in extensions:
        all_files.extend(glob.glob(os.path.join(directory_path, f'*.{ext}')))
    return all_files

# Function to read the content of a text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to automate GUI actions for text
def automate_gui_text_actions(text, x_coord, y_coord):
    # Copy the text to clipboard
    pyperclip.copy(text)
    # Open the window using Win + 2; adjust based on your setup
    pyautogui.hotkey('win', '2')
    time.sleep(2)  
    pyautogui.click(x_coord, y_coord)
    time.sleep(1)  
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)  
    pyautogui.press('enter')

# Function to automate GUI actions for media file
def automate_gui_media_actions(file_path, x_coord, y_coord):
    # Assuming the application can handle file paths pasted directly
    # and will open/load the file accordingly
    pyperclip.copy(file_path)
    time.sleep(1)  # Ensure clipboard is updated
    pyautogui.click(x_coord, y_coord)
    time.sleep(1)  # Wait for focus
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)  # Wait for the paste action to complete
    pyautogui.press('enter')

# Directory containing the files
directory_path = 'C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\media'

# Text file handling
text_files = find_files_by_extension(directory_path, ['txt'])
if text_files:
    text_content = read_text_file(text_files[0])
    automate_gui_text_actions(text_content, 1418, 995)

# Media file handling
media_extensions = ['mp4', 'jpeg', 'png', 'jpg', 'webm']  # Extend this list as needed
media_files = find_files_by_extension(directory_path, media_extensions)
if media_files:
    # Assuming the first media file is the target; adjust logic if necessary
    automate_gui_media_actions(media_files[0], 1418, 995)
