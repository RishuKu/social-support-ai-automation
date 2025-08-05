# extraction_agent/bank_statement_extractor.py

import pandas as pd
import logging

def extract_from_bank_statement(excel_path: str) -> dict:
    try:
        # Read Excel file using openpyxl
        logging.info("Reading Excel file from path: %s", excel_path)
        df = pd.read_excel(excel_path, engine='openpyxl')

        # Show first few rows for debug
        logging.debug("First 5 rows:\n%s", df.head().to_string())

        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        logging.info("Cleaned Columns in Excel: %s", df.columns.tolist())

        # Validate required columns
        required_cols = ["Description", "Amount (AED)"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: '{col}'")

        # Ensure Amount column is numeric
        df["Amount (AED)"] = pd.to_numeric(df["Amount (AED)"], errors="coerce")
        logging.debug("Amount column converted to numeric")

        # Find salary/income row
        income_row = df[df["Description"].str.contains("Salary", case=False, na=False)]

        if not income_row.empty:
            income = float(income_row["Amount (AED)"].values[0])
        else:
            income = 0.0
            logging.warning("No salary/income row found.")

        # Determine employment status
        employment_status = "employed" if income > 0 else "unemployed"

        logging.info("Extracted income: %s, employment_status: %s", income, employment_status)

        return {
            "income": income,
            "employment_status": employment_status
        }

    except Exception as e:
        logging.exception("Failed to extract from bank statement Excel file: %s", e)
        raise ValueError("Failed to read or parse bank statement Excel file. Ensure correct format.") from e
