import os
import glob
import pyautogui
import pyperclip
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Open the window using Win + 2; ensure you have the desired window positioned at slot 2 in your taskbar
logger.info("Open the window using Win + 2; ensure you have the desired window positioned at slot 2 in your taskbar")
pyautogui.hotkey('win', '2')
time.sleep(2)  # Wait for the window to open; adjust the sleep time based on your system's speed

def find_first_text_file(directory_path):
    """Find the first text file in a directory."""
    logger.info("Searching for the first text file in the directory")
    txt_files = glob.glob(os.path.join(directory_path, '*.txt'))
    return txt_files[0] if txt_files else None

def read_text_file(file_path):
    """Read the content of a text file."""
    logger.info("Reading content from text file")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return ""

def automate_gui_actions(text, x_coord, y_coord):
    """Automate GUI actions with given text and coordinates."""
    if text:  # Only proceed if there's text to paste
        
        
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
        
        logger.info("Clicking on specified coordinates (X: 1357, Y: 988)")
        pyautogui.click(x=1461, y=989)
        time.sleep(2)
        
        logger.info("All actions completed successfully")
        time.sleep(2)
    else:
        print("No text file found.")

def main_loop():
    """Main loop to repeat the script's logic."""
    # Loop configuration
    repeat_times = None  # Number of times to repeat the process, set to None for infinite loop
    count = 0
    
    while repeat_times is None or count < repeat_times:
        # Specify the directory path and coordinates
        directory_path = 'C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\media'
        x_coord = 1418
        y_coord = 995
        
        # Main logic
        txt_file_path = find_first_text_file(directory_path)
        text_content = read_text_file(txt_file_path)
        automate_gui_actions(text_content, x_coord, y_coord)
        
        count += 1
        logger.info(f"Loop iteration {count} completed")
        # Optional: Add a delay or condition to break the loop

if __name__ == "__main__":
    main_loop()
