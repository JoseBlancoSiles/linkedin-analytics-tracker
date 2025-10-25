from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from webdriver_manager.chrome import ChromeDriverManager
from linkedin_scraper import scrape_first_post_analytics, scrape_post_analytics_details, scrape_analytics_url_last_20_posts
import os
import time

if __name__ == "__main__":
    print("Starting LinkedIn Analytics Scraper...")

    options = Options()
    options.add_argument("--start-maximized")

    selenium_profile = r"C:\Users\HP\AppData\Local\Google\Chrome\SeleniumProfile"
    os.makedirs(selenium_profile, exist_ok=True)

    options.add_argument(f"user-data-dir={selenium_profile}")
    options.add_argument("profile-directory=Default")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.linkedin.com/in/josesilesb/recent-activity/shares/")
        time.sleep(5)

        links = scrape_analytics_url_last_20_posts(driver)
        print("Scraped links:", links)

        # if links:
        #     analytics_data = scrape_post_analytics_details(driver, links[0])
        # else:
        #     print("⚠️ No analytics links found.")

    finally:
        driver.quit()