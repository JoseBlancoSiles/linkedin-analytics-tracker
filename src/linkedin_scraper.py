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
        print(f"Collected {len(links)} analytics links.")
    else:
        print("⚠️ No analytics links found.")

    return links

def scrape_all_post_analytics_details(driver, analytics_urls):
    """
    Scrape analytics details for multiple LinkedIn posts.
    Returns a list of dictionaries like:
    [
        {
            "url": "<analytics_url>",
            "Impressions": "5,074",
            "Members reached": "2,958",
            "Profile viewers from this post": "12",
            "Followers gained from this post": "8",
            "Reactions": "78",
            "Comments": "16",
            "Reposts": "7",
            "Saves": "73",
            "Sends on LinkedIn": "8"
        },
        ...
    ]
    """
    all_data = []

    for i, url in enumerate(analytics_urls, start=1):
        print(f"\n🔍 Scraping analytics ({i}/{len(analytics_urls)}): {url}")
        post_data = {"url": url}

        try:
            driver.get(url)
            time.sleep(5)

            # --- Top metrics (Impressions, Members reached) ---
            top_items = driver.find_elements(
                By.CSS_SELECTOR, "ul.member-analytics-addon-summary > li.member-analytics-addon-summary__list-item"
            )
            for li in top_items:
                try:
                    value = li.find_element(By.CSS_SELECTOR, "div.display-flex > p.text-body-medium-bold").get_attribute("innerText").strip()
                    label = li.find_element(By.CSS_SELECTOR, "p.member-analytics-addon-list-item__description").get_attribute("innerText").strip()
                    post_data[label] = value
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
                    post_data[label] = value
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
                    post_data[label] = value
                except:
                    continue

            print(f"Scraped analytics for post {i}: {len(post_data)} metrics")
            all_data.append(post_data)

        except Exception as e:
            print(f"⚠️ Could not scrape analytics for {url}: {e}")
            all_data.append(post_data)

    print(f"\nFinished scraping {len(all_data)} posts.")
    return all_data
