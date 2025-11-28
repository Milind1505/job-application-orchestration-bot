from selenium import webdriver
from selenium.webdriver.common.by import By
import os, time

def linkedin_login(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(os.getenv("LINKEDIN_EMAIL"))
    driver.find_element(By.ID, "password").send_keys(os.getenv("LINKEDIN_PASS"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)
    print("✅ Logged in successfully.")
