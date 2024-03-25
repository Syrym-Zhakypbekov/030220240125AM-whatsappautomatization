import pyautogui
import time
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(filename='automation_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to simulate keyboard shortcuts
async def press_enter():
    try:
        logging.info("Pressing Enter key")
        pyautogui.press('enter')
        await asyncio.sleep(1)  # Adding a delay for the action
        logging.info("Enter key pressed")
    except Exception as e:
        logging.error(f"Error while pressing Enter key: {e}")

# Function to click on a specific coordinate
async def click_coordinate(x, y, times=1, description=""):
    try:
        logging.info(f"Clicking on coordinate ({x}, {y}) {times} times - {description}")
        for _ in range(times):
            pyautogui.click(x, y)
            await asyncio.sleep(0.5)  # Adding a delay between clicks
        logging.info("Clicking completed")
    except Exception as e:
        logging.error(f"Error while clicking on coordinate ({x}, {y}): {e}")

# Function to perform the entire action
async def perform_action():
    try:
        # Click on the second coordinate
        await click_coordinate(*coordinate_2, description="Clicking on second coordinate")
        
        # Double click on the additional coordinate
        await click_coordinate(*additional_coordinate, times=2, description="Double clicking on additional coordinate")
        
        # Wait for 2 seconds
        await asyncio.sleep(2)
        
        # Press Enter after the last double click
        await press_enter()
        
        # Wait for a short duration
        await asyncio.sleep(1)
        
        # Double click on the final coordinate
        await click_coordinate(*final_coordinate, times=2, description="Double clicking on final coordinate")
    except Exception as e:
        logging.error(f"Error while performing action: {e}")

# Define coordinates
coordinate_2 = (1347, 792)
additional_coordinate = (1408, 988)
final_coordinate = (770, 491)

# Main function to execute the actions
async def main():
    await perform_action()
    await perform_action()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
