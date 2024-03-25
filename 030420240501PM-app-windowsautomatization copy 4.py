import pyautogui
import asyncio
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def click_and_press():
    try:
        logger.info("Simulating pressing Win + 2")
        pyautogui.hotkey('win', '2')
        
        logger.info("Waiting for 2 seconds before clicking")
        await asyncio.sleep(2)
        
        logger.info("Clicking on specified coordinates (X: 1357, Y: 988)")
        pyautogui.click(x=1357, y=988)
        
        logger.info("Waiting for 2 seconds before double-clicking")
        await asyncio.sleep(2)
        
        logger.info("Double-clicking on specified coordinates (X: 1375, Y: 790)")
        pyautogui.doubleClick(x=1375, y=790)
        
        logger.info("Waiting for 2 seconds before double-clicking again")
        await asyncio.sleep(2)
        
        logger.info("Double-clicking on specified coordinates (X: 992, Y: 501)")
        pyautogui.doubleClick(x=992, y=501)
        
        logger.info("Waiting for 2 seconds before triggering Enter button")
        await asyncio.sleep(2)
        
        logger.info("Pressing Enter button")
        pyautogui.press('enter')
        
        logger.info("All actions completed successfully")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

async def main():
    try:
        await click_and_press()
    except Exception as e:
        logger.error(f"An error occurred in main function: {e}")

# Run the main function asynchronously
asyncio.run(main())
