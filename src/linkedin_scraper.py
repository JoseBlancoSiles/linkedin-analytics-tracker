from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_first_post_analytics(driver):
    """
    Scrape the analytics link of the first LinkedIn post in the feed.
    Works with the current LinkedIn DOM structure.
    """
    # Wait a bit to ensure content loads
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)

    try:
        wait = WebDriverWait(driver, 20)

        # Find the first "View analytics" span
        analytics_span = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='View analytics']")
            )
        )

        # The post container usually has a data-urn with the post ID
        post_container = analytics_span.find_element(By.XPATH, "./ancestor::div[@data-urn]")
        post_urn = post_container.get_attribute("data-urn")

        if post_urn:
            href = f"https://www.linkedin.com/analytics/post-summary/{post_urn}/"
            print("📎 First post analytics link:", href)
            return [href]
        else:
            print("⚠️ Could not find post URN.")
            return []

    except Exception as e:
        print(f"⚠️ Could not find analytics link: {e}")
        return []