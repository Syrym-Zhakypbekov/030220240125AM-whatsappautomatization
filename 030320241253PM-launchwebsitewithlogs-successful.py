import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

async def open_website(url):
    # Initialize the driver to None for proper error handling in the finally block
    driver = None
    try:
        # Configure Chrome to use a pre-saved profile for persistent login state
        options = Options()
        options.add_argument("user-data-dir=C:\\ChromeProfile")  # Path to your Chrome profile

        # Specify the exact path for the ChromeDriver executable
        service = Service("C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\chromedriver.exe")

        # Log the initialization of the WebDriver
        print("Initializing the WebDriver with the provided Chrome profile and driver...")
        
        # Initialize the WebDriver with the Chrome service and options
        driver = webdriver.Chrome(service=service, options=options)
        
        # Log the website opening action
        print(f"Attempting to open {url}...")
        
        # Use WebDriver to open the URL
        driver.get(url)
        
        # Log the successful opening of the website
        print(f"Successfully opened {url}.")
        
        # Artificially wait using asyncio.sleep to mimic asynchronous behavior
        # This gives the page time to load
        await asyncio.sleep(5)  # Wait for 5 seconds for the website to load completely
        print(f"Waiting completed, the page should be fully loaded now.")

    except WebDriverException as e:
        # Log any WebDriverException that occurs
        print(f"An error occurred while trying to open {url}: {e}")

    finally:
        # Check if the driver was successfully initialized before trying to close it
        if driver:
            # Log the browser closing action
            print("Closing the browser...")
            
            # Close the browser
            driver.quit()
            
            # Log the successful closure of the browser
            print("Browser closed successfully.")

# URL to open
url = "https://9gag.com/"

# Run the coroutine to open the website
asyncio.run(open_website(url))
