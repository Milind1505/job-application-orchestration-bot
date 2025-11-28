import pandas as pd

def weekly_summary():
    df = pd.read_csv("logs/Applications.csv", names=["Job Title","Company","Date","Method","Status","Follow-up","Notes"])
    print("\n📊 Weekly Summary:")
    print(f"Total applications: {len(df)}")
    print(f"Unique companies: {df['Company'].nunique()}")
