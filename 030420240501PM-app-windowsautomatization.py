import pyautogui
import time
import pyperclip

# Function to simulate keyboard shortcuts
def press_hotkey(key1, key2):
    pyautogui.hotkey(key1, key2)
    time.sleep(1)  # Wait a bit for the action to complete

# Function to press the Enter key
def press_enter():
    pyautogui.press('enter')
    time.sleep(1)  # Wait a bit for the message to be sent

# Function to perform the copy-paste-send sequence for text
def copy_paste_send_text(text, coordinates, repeat_count=5, repeat_interval=5):
    # Move the mouse to the specific location and click to focus on the application
    pyautogui.click(coordinates[0], coordinates[1])
    time.sleep(1)  # Wait a bit to ensure the application is focused

    for _ in range(repeat_count):  # Repeat the process as needed
        # Copy to clipboard (assuming the text or file is already selected)
        pyperclip.copy(text)
        
        # Paste the copied content
        press_hotkey('ctrl', 'v')
        
        # Send the message
        press_enter()
        
        # Wait for the specified interval before repeating
        time.sleep(repeat_interval)

# Function to perform the copy-paste-send sequence for media files
def copy_paste_send_media(file_path, coordinates, repeat_count=1, repeat_interval=5):
    # Move the mouse to the specific location and click to focus on the application
    pyautogui.click(coordinates[0], coordinates[1])
    time.sleep(1)  # Wait a bit to ensure the application is focused

    for _ in range(repeat_count):  # Repeat the process as needed
        # Copy the file path to clipboard
        pyperclip.copy(file_path)
        
        # Paste the file path into the chat (assuming a dialog box)
        press_hotkey('ctrl', 'v')
        
        # Send the media file (may vary depending on application interface)
        # Here, we simulate pressing the Enter key to confirm the file selection
        press_enter()
        
        # Wait for the specified interval before repeating
        time.sleep(repeat_interval)

# Coordinates for the WhatsApp application input field
coordinates = (1442, 994)

# Define file paths
text_file_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\pictures\\Weekly science by science alert.txt"
media_file_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\pictures\\a2KQ5dp_460s.jpg"

# Copy and paste the title of the text file
with open(text_file_path, 'r') as file:
    first_line = file.readline().strip()  # Read the first line (title) of the text file

# Call the function to perform the copy-paste-send sequence for the text
copy_paste_send_text(first_line, coordinates)

# Call the function to perform the copy-paste-send sequence for the media file
copy_paste_send_media(media_file_path, coordinates)
