from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from webdriver_manager.chrome import ChromeDriverManager
from linkedin_scraper import scrape_first_post_analytics
import time
import os

if __name__ == "__main__":
    print("🚀 Starting LinkedIn Analytics Scraper...")

    options = Options()
    options.add_argument("--start-maximized")

    # Dedicated Selenium profile folder
    selenium_profile = r"C:\Users\HP\AppData\Local\Google\Chrome\SeleniumProfile"
    os.makedirs(selenium_profile, exist_ok=True)

    options.add_argument(f"user-data-dir={selenium_profile}")
    options.add_argument("profile-directory=Default")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Go directly to your LinkedIn activity feed
    driver.get("https://www.linkedin.com/in/josesilesb/recent-activity/shares/")
    time.sleep(5)  # wait for page to load

    # Scrape first post analytics link
    links = scrape_first_post_analytics(driver)
    print("Scraped links:", links)

    driver.quit()
