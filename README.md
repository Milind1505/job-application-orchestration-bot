# 🤖 LinkedIn Auto Apply Bot

This repository contains a fully automated **LinkedIn Easy Apply Bot** built using **Python** and **Selenium**.  
It logs into your LinkedIn account, searches for job listings across specific roles and locations, filters out “Easy Apply” opportunities, and automatically applies — handling multiple job applications in a single run.

---

## 🚀 Overview

The goal of this project is to streamline and automate the tedious process of applying for jobs on LinkedIn, especially for data, AI, and tech roles that allow **Easy Apply**.  
The bot:
- Logs into your LinkedIn account (via credentials or saved cookies)
- Searches based on pre-configured job titles and locations
- Detects and applies only to **Easy Apply** job posts
- Clicks through application steps (Next → Submit)
- Logs all application details for review and analysis

---

## 🧠 Features

✅ **Automated Job Search** – Finds jobs using LinkedIn search filters for titles and regions  
✅ **Easy Apply Only** – Skips complex multi-step applications  
✅ **Auto Login & Cookie Handling** – Saves session cookies to avoid repeated logins  
✅ **Smart Retry & Error Handling** – Manages LinkedIn timeouts and dynamic UI changes  
✅ **Activity Logging** – Records applied roles in `logs/Applications.csv`  
✅ **Configurable Roles & Locations** – Defined once via YAML and reused  
✅ **Headless Mode (Optional)** – Runs silently without opening Chrome UI  

---

## 🧩 Folder Structure


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
If uploading manually, skip this step.  
If using Git:
```bash
git clone https://github.com/your-username/linkedin-auto-apply-bot.git
cd linkedin-auto-apply-bot


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
If uploading manually, skip this step.  
If using Git:
```bash
git clone https://github.com/your-username/linkedin-auto-apply-bot.git
cd linkedin-auto-apply-bot
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

job_targets:
  - "Data Scientist"
  - "Machine Learning Engineer"
  - "AI Engineer"

preferred_locations:
  - "London"
  - "Cambridge"
  - "United Kingdom"
  - "Berlin"
  - "Amsterdam"

python main.py
