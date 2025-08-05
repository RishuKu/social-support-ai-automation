# create_bank_statement.py

import pandas as pd

# Define the bank statement data
data = {
    "Date": ["01-07-2025", "05-07-2025", "10-07-2025", "15-07-2025"],
    "Description": ["Salary Credit", "Rent Payment", "Groceries", "Utility Bill"],
    "Amount (AED)": [8500, -4000, -500, -1000],
    "Balance (AED)": [12500, 8500, 8000, 7000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel file using openpyxl
df.to_excel("bank_statement.xlsx", index=False, engine="openpyxl")

print("bank_statement.xlsx created successfully.")
