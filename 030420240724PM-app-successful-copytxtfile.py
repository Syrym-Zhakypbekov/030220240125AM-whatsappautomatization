import os
import glob
import pyautogui
import pyperclip
import time
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to find the first text file in a directory
def find_first_text_file(directory_path):
    logger.info("Function to find the first text file in a directory")
    # Search for all .txt files in the directory
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))
    # Return the first .txt file found if any exist
    return txt_files[0] if txt_files else None

# Function to read the content of a text file
def read_text_file(file_path):
    logger.info("Function to read the content of a text file")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return ""

# Function to automate GUI actions
def automate_gui_actions(text, x_coord, y_coord):
    if text:  # Only proceed if there's text to paste
        # Copy the text to clipboard
        logger.info("Copy the text to clipboard")
        pyperclip.copy(text)
        
        # Open the window using Win + 2; ensure you have the desired window positioned at slot 2 in your taskbar
        logger.info("Open the window using Win + 2; ensure you have the desired window positioned at slot 2 in your taskbar")
        pyautogui.hotkey('win', '2')
        time.sleep(2)  # Wait for the window to open; adjust the sleep time based on your system's speed
        
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
        pyautogui.click(x=1357, y=988)
        
        logger.info("Waiting for 2 seconds before double-clicking")
        time.sleep(2)
        
        logger.info("Double-clicking on specified coordinates (X: 1375, Y: 790)")
        pyautogui.doubleClick(x=1375, y=790)
        
        logger.info("Waiting for 2 seconds before double-clicking again")
        time.sleep(2)
        
        logger.info("Double-clicking on specified coordinates (X: 992, Y: 501)")
        pyautogui.doubleClick(x=992, y=501)
        
        logger.info("Waiting for 2 seconds before triggering Enter button")
        time.sleep(2)
        
        logger.info("Pressing Enter button")
        pyautogui.press('enter')
        
        logger.info("All actions completed successfully")
    else:
        print("No text file found.")

# Specify the directory containing the text file
directory_path = 'C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\media'

# Find the first .txt file in the specified directory
txt_file_path = find_first_text_file(directory_path)

# Read the content of the found text file
text_content = read_text_file(txt_file_path)

# Specify the coordinates where you want to navigate
x_coord = 1418
y_coord = 995

# Automate GUI actions with the read content
automate_gui_actions(text_content, x_coord, y_coord)
