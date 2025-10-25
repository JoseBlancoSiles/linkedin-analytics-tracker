from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_analytics_url_last_20_posts(driver, max_posts=20):
    """
    Scrape analytics links of up to `max_posts` LinkedIn posts.
    Ignores posts without "View analytics".
    """
    links = []
    wait = WebDriverWait(driver, 10)
    scroll_pause = 3
    scroll_position = 0

    while len(links) < max_posts:
        time.sleep(2)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        scroll_position += 1000
        time.sleep(scroll_pause)

        try:
            # Find all "View analytics" spans currently visible
            analytics_spans = driver.find_elements(By.XPATH, "//span[text()='View analytics']")
            for span in analytics_spans:
                try:
                    post_container = span.find_element(By.XPATH, "./ancestor::div[@data-urn]")
                    post_urn = post_container.get_attribute("data-urn")
                    href = f"https://www.linkedin.com/analytics/post-summary/{post_urn}/"
                    if href not in links:
                        links.append(href)
                        print(f"📎 Found analytics link ({len(links)}): {href}")
                        if len(links) >= max_posts:
                            break
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Could not find analytics span in this scroll: {e}")

        # Stop if reached bottom
        if len(links) >= max_posts or "You're all caught up" in driver.page_source:
            break

    if links:
        print(f"✅ Collected {len(links)} analytics links.")
    else:
        print("⚠️ No analytics links found.")

    return links

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
