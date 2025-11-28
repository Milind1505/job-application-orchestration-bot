# modules/job_search.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, random

def search_jobs(driver, role, location, retries=0):
    """Robust job search scraper for LinkedIn (2025-proof)."""
    MAX_RETRIES = 2
    print(f"🔎 Opening search for {role} in {location}…")

    search_url = (
        f"https://www.linkedin.com/jobs/search/?keywords={role.replace(' ', '%20')}"
        f"&location={location.replace(' ', '%20')}&f_AL=true"
    )
    driver.get(search_url)
    time.sleep(4 + random.random() * 2)

    try:
        # ✅ Wait for main results region (2025 LinkedIn structure)
        possible_selectors = [
            "section.jobs-search-results-list",
            "ul.jobs-search__results-list",
            "div.jobs-search-results",
            "div.two-pane-serp-page__results-list"
        ]

        results_box = None
        for sel in possible_selectors:
            try:
                results_box = WebDriverWait(driver, 12).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                )
                if results_box:
                    break
            except TimeoutException:
                continue

        if not results_box:
            # Sometimes rendered in iframe
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    if driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list"):
                        results_box = True
                        break
                    driver.switch_to.default_content()
                except Exception:
                    driver.switch_to.default_content()
                    continue

        if not results_box:
            raise TimeoutException("Job results container not found.")

        # ✅ Scroll to load more jobs dynamically
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2 + random.random())
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # ✅ Collect job cards (new layout)
        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.base-card__full-link, a.base-card__full-link")
        if not job_cards:
            job_cards = driver.find_elements(By.XPATH, "//a[contains(@class,'job-card-container__link')]")

        print(f"🧩 Found {len(job_cards)} jobs for {role} in {location}.")

        jobs = []
        for card in job_cards:
            try:
                title = card.text.strip().split("\n")[0]
                link = card.get_attribute("href")
                jobs.append({"title": title or "Unknown", "company": "Unknown", "link": link})
            except Exception:
                continue

        if not jobs and retries < MAX_RETRIES:
            print(f"⚠️ No jobs detected for {location}. Retrying ({retries+1}/{MAX_RETRIES})…")
            time.sleep(5)
            return search_jobs(driver, role, location, retries + 1)

        return jobs

    except TimeoutException:
        if retries < MAX_RETRIES:
            print(f"⚠️ Timeout while loading {location}. Retrying ({retries+1}/{MAX_RETRIES})…")
            time.sleep(5)
            return search_jobs(driver, role, location, retries + 1)
        else:
            print(f"❌ Failed to load job results for {location} after retries.")
            return []

    except Exception as e:
        print(f"⚠️ Search failed for {location}: {e}")
        return []
