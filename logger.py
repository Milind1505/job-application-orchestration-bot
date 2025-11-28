import pandas as pd
from datetime import datetime

def log_application(job, method="Easy Apply", status="Submitted", notes=""):
    entry = {
        "Job Title": job["title"],
        "Company": job["company"],
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Method": method,
        "Status": status,
        "Follow-up": "",
        "Notes": notes
    }
    df = pd.DataFrame([entry])
    df.to_csv("logs/Applications.csv", mode="a", index=False, header=False)
