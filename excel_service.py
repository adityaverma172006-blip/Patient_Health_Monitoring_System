"""
Patient Health Monitoring System - Excel Service Module
=======================================================
Handles reading patient data from Excel (.xlsx) files.

This is an educational project for B.Tech college demonstration.
NOT intended for real medical diagnosis.
"""

import os
import logging

import pandas as pd

import config

logger = logging.getLogger(__name__)

# Required columns in the Excel file
REQUIRED_COLUMNS = [
    "Patient_ID",
    "Patient_Name",
    "Age",
    "Heart_Rate",
    "SpO2",
    "Temperature",
    "Timestamp",
]


def create_sample_excel(filepath=None):
    """
    Create a sample patient_data.xlsx file with example patients.

    Args:
        filepath (str): Path to create the Excel file.
                       Defaults to config.EXCEL_FILE.

    Returns:
        bool: True if created successfully, False otherwise.
    """
    if filepath is None:
        filepath = config.EXCEL_FILE

    try:
        data = {
            "Patient_ID": ["P001", "P002", "P003"],
            "Patient_Name": ["Rahul Sharma", "Priya Patel", "Amit Kumar"],
            "Age": [28, 45, 62],
            "Heart_Rate": [82, 105, 135],
            "SpO2": [98, 92, 86],
            "Temperature": [36.8, 38.2, 39.4],
            "Timestamp": [
                "2026-11-20 10:00:00",
                "2026-11-20 10:05:00",
                "2026-11-20 10:10:00",
            ],
        }

        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False, engine="openpyxl")
        logger.info("Sample Excel file created: %s", filepath)
        return True

    except Exception as e:
        logger.error("Failed to create sample Excel file: %s", e)
        return False


def read_patient_data(filepath=None):
    """
    Read patient data from an Excel file.

    Args:
        filepath (str): Path to the Excel file.
                       Defaults to config.EXCEL_FILE.

    Returns:
        tuple: (success: bool, data: list of dicts or error message: str)
    """
    if filepath is None:
        filepath = config.EXCEL_FILE

    # Check if file exists
    if not os.path.exists(filepath):
        msg = f"Excel file not found: {filepath}"
        logger.error(msg)
        return False, msg

    try:
        df = pd.read_excel(filepath, engine="openpyxl")
        logger.info("Excel file loaded: %s (%d rows)", filepath, len(df))

        # Validate required columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            msg = f"Missing columns in Excel file: {', '.join(missing_cols)}"
            logger.error(msg)
            return False, msg

        # Process each row
        patients = []
        errors = []

        for idx, row in df.iterrows():
            row_num = idx + 2  # Excel row (1-indexed header + 1-indexed data)
            try:
                patient = {
                    "patient_id": str(row["Patient_ID"]).strip(),
                    "patient_name": str(row["Patient_Name"]).strip(),
                    "age": _validate_numeric(row["Age"], "Age", row_num),
                    "heart_rate": _validate_numeric(
                        row["Heart_Rate"], "Heart_Rate", row_num
                    ),
                    "spo2": _validate_numeric(row["SpO2"], "SpO2", row_num),
                    "temperature": _validate_numeric(
                        row["Temperature"], "Temperature", row_num
                    ),
                    "timestamp": str(row["Timestamp"]),
                }
                patients.append(patient)
            except ValueError as e:
                errors.append(f"Row {row_num}: {e}")
                logger.warning("Skipping row %d: %s", row_num, e)

        if errors:
            print(f"\n  [!] {len(errors)} row(s) had validation issues:")
            for err in errors:
                print(f"      - {err}")

        if not patients:
            return False, "No valid patient data found in Excel file."

        logger.info(
            "Successfully read %d patient(s) from Excel.", len(patients)
        )
        return True, patients

    except Exception as e:
        msg = f"Error reading Excel file: {e}"
        logger.error(msg)
        return False, msg


def _validate_numeric(value, field_name, row_num):
    """
    Validate that a value is numeric.

    Args:
        value: The value to validate.
        field_name (str): Name of the field.
        row_num (int): Excel row number for error messages.

    Returns:
        float: The numeric value.

    Raises:
        ValueError: If the value is not numeric.
    """
    try:
        num = float(value)
        if pd.isna(num):
            raise ValueError(f"{field_name} is empty in row {row_num}")
        return num
    except (ValueError, TypeError):
        raise ValueError(
            f"Invalid {field_name} value '{value}' in row {row_num}"
        )
