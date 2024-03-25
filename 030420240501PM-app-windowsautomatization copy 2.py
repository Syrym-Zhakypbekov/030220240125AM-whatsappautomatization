import pyautogui
import time
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to simulate a mouse click at a specific location
async def click_file(coordinates):
    try:
        pyautogui.click(coordinates)
        logging.info("Clicked on file.")
        await asyncio.sleep(1)  # Wait for a second to ensure the click action is completed
    except Exception as e:
        logging.error(f"Error clicking on file: {e}")

# Function to simulate the "Ctrl+C" action to copy selected file
async def copy_selected_file():
    try:
        pyautogui.hotkey('ctrl', 'c')
        logging.info("Selected file copied to clipboard.")
        await asyncio.sleep(1)  # Wait for a second to ensure the copy action is completed
    except Exception as e:
        logging.error(f"Error copying selected file: {e}")

# Main function to execute the script
async def main(file_coordinates):
    try:
        # Ensure the file explorer window is active
        pyautogui.getWindowsWithTitle('Downloads')[0].activate()
        logging.info("Activated file explorer window.")

        # Click on the specified file
        await click_file(file_coordinates)
        
        # Copy the selected file
        await copy_selected_file()
        logging.info("File operation completed.")
    except Exception as e:
        logging.error(f"Error in main function: {e}")

# Coordinates where the file is located in the file explorer
file_coordinates = (295, 224)  # Replace x and y with the actual coordinates

# Run the main function
asyncio.run(main(file_coordinates))
