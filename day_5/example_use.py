from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Launch Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to page
driver.get("https://quotes.toscrape.com/js/")

# Find element (after JS runs)
quotes = driver.find_elements(By.CLASS_NAME, "quote")
print(f"Found {len(quotes)} quotes")

# Close browser
driver.quit()

