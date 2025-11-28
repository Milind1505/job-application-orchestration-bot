from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time


def apply_to_job(driver, job, user_context):
    """Clicks Easy Apply, skips all questions, and submits automatically."""

    print(f"🧠 Opening {job['title']} at {job['company']} ...")

    try:
        job_card = job.get("element")
        if job_card:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_card)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", job_card)
            print(f"💡 Clicked on job card for {job['title']}")
        else:
            print(f"⚙️ Opening direct link for {job['title']}")
            driver.get(job["link"])

        WebDriverWait(driver, 20).until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-search__job-details--container")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-details__main-content")),
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.jobs-hero__content"))
            )
        )

    except Exception as e:
        print(f"⚠️ Could not open job details: {e}")
        return False

    # --- Locate Easy Apply button ---
    easy_apply_button = None
    selectors = [
        "//button[contains(@class,'jobs-apply-button')]",
        "//button[contains(.,'Easy Apply')]",
        "//button[contains(@aria-label,'Easy Apply')]"
    ]

    for sel in selectors:
        try:
            btn = driver.find_element(By.XPATH, sel)
            if btn.is_displayed():
                easy_apply_button = btn
                break
        except NoSuchElementException:
            continue

    if not easy_apply_button:
        print(f"⚠️ No Easy Apply option for {job['title']} at {job['company']}. Skipping.")
        return False

    # --- Click Easy Apply ---
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", easy_apply_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", easy_apply_button)
        print(f"🚀 Easy Apply popup opened for {job['title']}")
        time.sleep(3)
    except Exception as e:
        print(f"⚠️ Failed to click Easy Apply: {e}")
        return False

    # --- Try to auto-progress through all steps ---
    for _ in range(5):  # up to 5 pages of 'Next'
        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Continue') or contains(.,'Next')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
            driver.execute_script("arguments[0].click();", next_btn)
            print("➡️ Clicked Next")
            time.sleep(3)
        except NoSuchElementException:
            break
        except Exception as e:
            print(f"⚠️ Could not click Next: {e}")
            break

    # --- Upload files if prompted ---
    try:
        upload_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
        if upload_inputs:
            upload_inputs[0].send_keys(user_context["cv_path"])
            if len(upload_inputs) > 1:
                upload_inputs[1].send_keys(user_context.get("cover_letter_path", ""))
            print("📎 Uploaded CV and cover letter.")
    except Exception:
        pass

    # --- Try to submit application ---
    try:
        submit_btn = driver.find_element(By.XPATH, "//button[contains(.,'Submit application')]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_btn)
        print(f"✅ Submitted {job['title']} at {job['company']}")
        return True
    except NoSuchElementException:
        print(f"⚠️ No Submit button visible for {job['title']}. Manual review may be required.")
        return False
    except Exception as e:
        print(f"⚠️ Submission failed: {e}")
        return False
