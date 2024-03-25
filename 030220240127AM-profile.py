from selenium import webdriver

# Set the path to the Chrome WebDriver executable
chrome_driver_path = "C:\\Users\\syrym\\Downloads\\030220240125AM-whatsappautomatization\\chromedriver.exe"

# Start the Chrome browser
browser = webdriver.Chrome(executable_path=chrome_driver_path)

# Example: Navigate to a website
website_url = "https://google.com"
browser.get(website_url)

# Example: Save some information
# You can save information by extracting it from the webpage using Selenium's find_element methods
# For example:
# element = browser.find_element_by_xpath("//xpath_of_element")
# information = element.text
# Then you can save the information to a file or database

# Close the browser session
# browser.quit()
