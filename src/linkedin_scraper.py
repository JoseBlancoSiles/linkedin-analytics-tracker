from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_first_post_analytics(driver):
    """
    Scrape the analytics link of the first LinkedIn post in the feed.
    Works with the current LinkedIn DOM structure.
    """
    time.sleep(5)  # allow feed to load
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

def scrape_post_analytics_details(driver, analytics_url):
    """
    Scrape all available metrics from the LinkedIn post analytics page.
    Returns a dictionary of {metric_name: value}.
    """
    try:
        driver.get(analytics_url)
        time.sleep(5)  # wait for React content

        analytics_data = {}

        # --- Top metrics (Impressions, Members reached) ---
        top_items = driver.find_elements(
            By.CSS_SELECTOR, "ul.member-analytics-addon-summary > li.member-analytics-addon-summary__list-item"
        )
        for li in top_items:
            try:
                value = li.find_element(By.CSS_SELECTOR, "div.display-flex > p.text-body-medium-bold").get_attribute("innerText").strip()
                label = li.find_element(By.CSS_SELECTOR, "p.member-analytics-addon-list-item__description").get_attribute("innerText").strip()
                analytics_data[label] = value
            except:
                continue

        # --- Profile metrics (Profile viewers, Followers gained) ---
        profile_items = driver.find_elements(
            By.CSS_SELECTOR, "ul.list-style-none.t-14 li.member-analytics-addon-metric-row-list__item"
        )
        for li in profile_items:
            try:
                label = li.find_element(By.CSS_SELECTOR, "span.member-analytics-addon-metric-row-list-item__title--color").get_attribute("innerText").strip()
                value = li.find_element(By.CSS_SELECTOR, "span.member-analytics-addon-metric-row-list-item__value").get_attribute("innerText").strip()
                analytics_data[label] = value
            except:
                continue

        # --- Social engagement (Reactions, Comments, Reposts, Saves, Sends) ---
        social_items = driver.find_elements(
            By.CSS_SELECTOR, "ul[aria-labelledby] li.member-analytics-addon__cta-list-item"
        )
        for li in social_items:
            try:
                label = li.find_element(By.CSS_SELECTOR, "span.member-analytics-addon__cta-list-item-title").get_attribute("innerText").strip()
                value = li.find_element(By.CSS_SELECTOR, "span.member-analytics-addon__cta-list-item-text").get_attribute("innerText").strip()
                analytics_data[label] = value
            except:
                continue

        print("📊 Scraped analytics data:", analytics_data)
        return analytics_data

    except Exception as e:
        print(f"⚠️ Could not scrape analytics details: {e}")
        return {}
