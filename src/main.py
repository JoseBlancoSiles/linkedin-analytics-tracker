import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from utils import convert_to_csv
from utils import append_to_google_sheet
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from webdriver_manager.chrome import ChromeDriverManager
from linkedin_scraper import scrape_all_post_analytics_details, scrape_analytics_url_last_20_posts

if __name__ == "__main__":
    print("Starting LinkedIn Analytics Scraper...")

    options = Options()
    options.add_argument("--start-maximized")

    # Load selenium profile path from environment variable
    selenium_profile = os.getenv("SELENIUM_PROFILE")
    if not selenium_profile:
        raise ValueError("SELENIUM_PROFILE is not set in the .env file.")
    os.makedirs(selenium_profile, exist_ok=True)

    options.add_argument(f"user-data-dir={selenium_profile}")
    options.add_argument("profile-directory=Default")
    
    # Load LinkedIn username from environment variable. If you don't know, go to your LinkedIn profile and check the URL. It's the part after linkedin.com/in/
    linkedin_username = os.getenv("LINKEDIN_USERNAME")
    if not linkedin_username:
        raise ValueError("LINKEDIN_USERNAME is not set in the .env file.")

    # Install Chrome driver always to avoid version mismatch
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # This URL is like your Feed but only shows your posts (and reposts)
    driver.get(f"https://www.linkedin.com/in/{linkedin_username}/recent-activity/shares/")
    time.sleep(5)

    links = scrape_analytics_url_last_20_posts(driver)
    print(f"\nTotal links collected: {len(links)}")

    if links:
        all_analytics = scrape_all_post_analytics_details(driver, links)

        # Optional CSV backup
        convert_to_csv(all_analytics)

        # Append to Google Sheet
        append_to_google_sheet(all_analytics)
    else:
        print("No analytics links found.")

    driver.quit()