import ctypes
import pyautogui
import time
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants needed for the operation
CF_HDROP = 15
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040
GHND = GMEM_MOVEABLE | GMEM_ZEROINIT

# Function to copy file to clipboard
async def copy_file_to_clipboard(file_path):
    try:
        # Allocate and lock a global memory block
        h_global_mem = ctypes.windll.kernel32.GlobalAlloc(GHND, ctypes.sizeof(ctypes.c_wchar) * (len(file_path) + 1))
        p_global_mem = ctypes.windll.kernel32.GlobalLock(h_global_mem)
        
        # Copy the file path to the allocated memory
        ctypes.cdll.msvcrt.wcscpy(ctypes.c_wchar_p(p_global_mem), file_path)
        
        # Unlock the global memory block
        ctypes.windll.kernel32.GlobalUnlock(h_global_mem)
        
        # Open the clipboard and clear its contents
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        
        # Set the clipboard data to point to the file
        ctypes.windll.user32.SetClipboardData(CF_HDROP, h_global_mem)
        
        # Close the clipboard
        ctypes.windll.user32.CloseClipboard()
        logging.info("File copied to clipboard.")
    except Exception as e:
        logging.error(f"Error copying file to clipboard: {e}")

# Function to simulate the "Ctrl+V" action to paste from clipboard
async def paste_from_clipboard():
    try:
        pyautogui.hotkey('ctrl', 'v')
        logging.info("Pasted content from clipboard.")
        await asyncio.sleep(1)  # Wait for a second to ensure the paste action is completed
    except Exception as e:
        logging.error(f"Error pasting content from clipboard: {e}")

# Function to simulate the Enter key press
async def send_enter():
    try:
        pyautogui.press('enter')
        logging.info("Enter key pressed.")
        await asyncio.sleep(1)  # Wait for a second to ensure the send action is completed
    except Exception as e:
        logging.error(f"Error pressing Enter key: {e}")

# Main function to execute the script
async def main(coordinates, media_file_path):
    try:
        # Click on the WhatsApp application to bring it to focus
        pyautogui.click(coordinates[0], coordinates[1])
        logging.info("Clicked on WhatsApp application.")
        
        # Copy the media file to the clipboard
        await copy_file_to_clipboard(media_file_path)
        
        # Paste the media file from the clipboard into WhatsApp
        await paste_from_clipboard()
        
        # Send the media file
        await send_enter()
        logging.info("Media file sent.")
    except Exception as e:
        logging.error(f"Error in main function: {e}")

# Coordinates for the WhatsApp application input field
coordinates = (1442, 994)

# Define file paths
media_file_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\videos\\awZqQ1Q_460svvp9.webm"

# Run the main function
asyncio.run(main(coordinates, media_file_path))
