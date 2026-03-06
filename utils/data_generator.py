import pandas as pd
import random
from datetime import datetime, timedelta


def generate_dataset(n=100):

    initiative_types = [
        "AI Document Search",
        "Customer Support Chatbot",
        "Fraud Detection System",
        "Supply Chain Forecasting",
        "Marketing Optimizer",
        "Invoice Automation",
        "Predictive Maintenance",
        "Sales Recommendation Engine",
        "Demand Forecasting",
        "Risk Analytics Platform"
    ]

    owners = ["Rahul", "Anita", "Vikram", "Priya", "Karan", "Neha", "Arjun", "Sneha"]

    statuses = ["On Track", "Delayed", "Completed"]

    data = []

    for i in range(n):

        start = datetime(2024,1,1) + timedelta(days=random.randint(0,120))
        end = start + timedelta(days=random.randint(60,180))

        kpi_target = random.randint(100,200)
        kpi_achieved = random.randint(60,200)

        benefit = random.randint(500000,2500000)

        data.append({
            "Initiative Name": random.choice(initiative_types) + f" {i+1}",
            "Owner": random.choice(owners),
            "Start Date": start.date(),
            "End Date": end.date(),
            "Status": random.choice(statuses),
            "KPI Target": kpi_target,
            "KPI Achieved": kpi_achieved,
            "Business Benefit": benefit
        })

    return pd.DataFrame(data)