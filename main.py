import yaml
import os
from selenium import webdriver
from dotenv import load_dotenv

from modules.linkedin_login import linkedin_login
from modules.job_search import search_jobs
from modules.job_apply import apply_to_job
from modules.logger import log_application
from modules.weekly_summary import weekly_summary


def main():
    # Load credentials
    load_dotenv("config/credentials.env")

    # Load user preferences
    with open("config/user_config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    # Initialize browser
    driver = webdriver.Chrome()

    # Login to LinkedIn
    linkedin_login(driver)

    # Job search + apply loop
    for role in cfg["job_targets"]:
        for loc in cfg["preferred_locations"]:
            print(f"\n🔍 Searching for {role} roles in {loc}...")
            jobs = search_jobs(driver, role, loc)

            for job in jobs:
                success = apply_to_job(driver, job, cfg)
                if success:
                    log_application(job)

    # Weekly summary and close
    weekly_summary()
    driver.quit()
    print("\n✅ All done! Check logs/Applications.csv for details.")


if __name__ == "__main__":
    main()
