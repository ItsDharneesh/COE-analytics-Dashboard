import pandas as pd

def clean_data(df):

    # Convert dates
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["End Date"] = pd.to_datetime(df["End Date"])

    # Standardize status
    df["Status"] = df["Status"].str.title()

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df["Business Benefit"] = df["Business Benefit"].fillna(0)

    # KPI Achievement %
    df["KPI %"] = (df["KPI Achieved"] / df["KPI Target"]) * 100

    return df