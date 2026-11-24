"""
Patient Health Monitoring System - Patient Monitor Module
=========================================================
Core logic for evaluating patient health parameters and determining status.

This is an educational project for B.Tech college demonstration.
NOT intended for real medical diagnosis.
"""

import logging
from datetime import datetime

import config

logger = logging.getLogger(__name__)


def evaluate_heart_rate(hr):
    """
    Evaluate heart rate and return (status, reason).

    Args:
        hr (int/float): Heart rate in BPM.

    Returns:
        tuple: (status_string, reason_string or None)
    """
    if hr is None or not isinstance(hr, (int, float)):
        return config.STATUS_WARNING, "Heart rate data is invalid."

    if config.HR_NORMAL_LOW <= hr <= config.HR_NORMAL_HIGH:
        return config.STATUS_NORMAL, None
    elif hr < config.HR_CRITICAL_LOW or hr > config.HR_CRITICAL_HIGH:
        return config.STATUS_CRITICAL, f"Heart rate is critically abnormal ({hr} BPM)."
    elif hr < config.HR_NORMAL_LOW or hr > config.HR_NORMAL_HIGH:
        return config.STATUS_WARNING, f"Heart rate is abnormal ({hr} BPM)."
    else:
        return config.STATUS_NORMAL, None


def evaluate_spo2(spo2):
    """
    Evaluate SpO2 level and return (status, reason).

    Args:
        spo2 (int/float): SpO2 percentage.

    Returns:
        tuple: (status_string, reason_string or None)
    """
    if spo2 is None or not isinstance(spo2, (int, float)):
        return config.STATUS_WARNING, "SpO2 data is invalid."

    if spo2 >= config.SPO2_NORMAL:
        return config.STATUS_NORMAL, None
    elif spo2 >= config.SPO2_WARNING:
        return config.STATUS_WARNING, f"Oxygen level is low ({spo2}%)."
    elif spo2 >= config.SPO2_CRITICAL:
        return config.STATUS_CRITICAL, f"Oxygen level is critically low ({spo2}%)."
    else:
        return config.STATUS_CRITICAL, f"Oxygen level is dangerously low ({spo2}%)."


def evaluate_temperature(temp):
    """
    Evaluate body temperature and return (status, reason).

    Args:
        temp (float): Temperature in °C.

    Returns:
        tuple: (status_string, reason_string or None)
    """
    if temp is None or not isinstance(temp, (int, float)):
        return config.STATUS_WARNING, "Temperature data is invalid."

    if temp < config.TEMP_CRITICAL_LOW:
        return config.STATUS_CRITICAL, f"Temperature is critically low ({temp}°C)."
    elif config.TEMP_NORMAL_LOW <= temp <= config.TEMP_NORMAL_HIGH:
        return config.STATUS_NORMAL, None
    elif temp <= config.TEMP_WARNING_HIGH:
        return config.STATUS_WARNING, f"Temperature is elevated ({temp}°C)."
    elif temp >= config.TEMP_CRITICAL_HIGH:
        return config.STATUS_CRITICAL, f"Temperature is critically high ({temp}°C)."
    else:
        return config.STATUS_NORMAL, None


def calculate_overall_status(hr_status, spo2_status, temp_status):
    """
    Calculate overall patient status from individual parameter statuses.

    Priority: CRITICAL > WARNING > NORMAL

    Args:
        hr_status (str): Heart rate status.
        spo2_status (str): SpO2 status.
        temp_status (str): Temperature status.

    Returns:
        str: Overall status (NORMAL, WARNING, or CRITICAL).
    """
    statuses = [hr_status, spo2_status, temp_status]

    if config.STATUS_CRITICAL in statuses:
        return config.STATUS_CRITICAL
    elif config.STATUS_WARNING in statuses:
        return config.STATUS_WARNING
    else:
        return config.STATUS_NORMAL


def evaluate_patient(heart_rate, spo2, temperature):
    """
    Evaluate all patient parameters and return a comprehensive result.

    Args:
        heart_rate (int/float): Heart rate in BPM.
        spo2 (int/float): SpO2 percentage.
        temperature (float): Temperature in °C.

    Returns:
        dict: {
            'heart_rate': {'value': ..., 'status': ..., 'reason': ...},
            'spo2': {'value': ..., 'status': ..., 'reason': ...},
            'temperature': {'value': ..., 'status': ..., 'reason': ...},
            'overall_status': ...,
            'reasons': [...],
            'timestamp': ...,
        }
    """
    hr_status, hr_reason = evaluate_heart_rate(heart_rate)
    spo2_status, spo2_reason = evaluate_spo2(spo2)
    temp_status, temp_reason = evaluate_temperature(temperature)

    overall_status = calculate_overall_status(hr_status, spo2_status, temp_status)

    reasons = []
    if hr_reason:
        reasons.append(hr_reason)
    if spo2_reason:
        reasons.append(spo2_reason)
    if temp_reason:
        reasons.append(temp_reason)

    result = {
        "heart_rate": {
            "value": heart_rate,
            "status": hr_status,
            "reason": hr_reason,
        },
        "spo2": {
            "value": spo2,
            "status": spo2_status,
            "reason": spo2_reason,
        },
        "temperature": {
            "value": temperature,
            "status": temp_status,
            "reason": temp_reason,
        },
        "overall_status": overall_status,
        "reasons": reasons,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Log the evaluation
    logger.info(
        "Patient evaluated: HR=%s, SpO2=%s, Temp=%s → %s",
        heart_rate, spo2, temperature, overall_status,
    )
    if reasons:
        for reason in reasons:
            if overall_status == config.STATUS_CRITICAL:
                logger.critical("ALERT: %s", reason)
            else:
                logger.warning("Warning: %s", reason)

    return result


def display_patient_result(result, patient_id=None, patient_name=None):
    """
    Display patient evaluation results in a formatted way.

    Args:
        result (dict): Result from evaluate_patient().
        patient_id (str, optional): Patient ID.
        patient_name (str, optional): Patient name.
    """
    overall = result["overall_status"]

    if overall == config.STATUS_CRITICAL:
        print("\n" + "!" * 50)
        print("        CRITICAL CONDITION DETECTED")
        if patient_id:
            print(f"        Patient: {patient_id}", end="")
            if patient_name:
                print(f" ({patient_name})")
            else:
                print()
        print("!" * 50)
    elif overall == config.STATUS_WARNING:
        print("\n" + "*" * 50)
        print("        WARNING CONDITION DETECTED")
        if patient_id:
            print(f"        Patient: {patient_id}", end="")
            if patient_name:
                print(f" ({patient_name})")
            else:
                print()
        print("*" * 50)
    else:
        print("\n" + "-" * 50)
        print("        PATIENT MONITORING")
        if patient_id:
            print(f"        Patient: {patient_id}", end="")
            if patient_name:
                print(f" ({patient_name})")
            else:
                print()
        print("-" * 50)

    print(f"\n  Heart Rate   : {result['heart_rate']['value']} BPM "
          f"[{result['heart_rate']['status']}]")
    print(f"  SpO2         : {result['spo2']['value']}% "
          f"[{result['spo2']['status']}]")
    print(f"  Temperature  : {result['temperature']['value']}°C "
          f"[{result['temperature']['status']}]")
    print(f"\n  Overall Status: {overall}")
    print(f"  Timestamp     : {result['timestamp']}")

    if result["reasons"]:
        print("\n  Reasons:")
        for reason in result["reasons"]:
            print(f"    - {reason}")

    print()


def get_manual_patient_data():
    """
    Get patient data from manual terminal input with validation.

    Returns:
        tuple: (heart_rate, spo2, temperature) or None if input cancelled.
    """
    print("\n--- Enter Patient Data Manually ---\n")

    try:
        # Heart Rate
        while True:
            hr_input = input("  Enter Heart Rate (BPM, e.g. 82): ").strip()
            if not hr_input:
                print("  [!] Heart rate cannot be empty.")
                continue
            try:
                heart_rate = float(hr_input)
                if heart_rate <= 0 or heart_rate > 300:
                    print("  [!] Heart rate must be between 1 and 300 BPM.")
                    continue
                break
            except ValueError:
                print("  [!] Please enter a valid number.")

        # SpO2
        while True:
            spo2_input = input("  Enter SpO2 (%, e.g. 98): ").strip()
            if not spo2_input:
                print("  [!] SpO2 cannot be empty.")
                continue
            try:
                spo2 = float(spo2_input)
                if spo2 < 0 or spo2 > 100:
                    print("  [!] SpO2 must be between 0 and 100%.")
                    continue
                break
            except ValueError:
                print("  [!] Please enter a valid number.")

        # Temperature
        while True:
            temp_input = input("  Enter Temperature (°C, e.g. 36.8): ").strip()
            if not temp_input:
                print("  [!] Temperature cannot be empty.")
                continue
            try:
                temperature = float(temp_input)
                if temperature < 20 or temperature > 50:
                    print("  [!] Temperature must be between 20 and 50°C.")
                    continue
                break
            except ValueError:
                print("  [!] Please enter a valid number.")

        return heart_rate, spo2, temperature

    except KeyboardInterrupt:
        print("\n  [!] Input cancelled.")
        return None


def get_simulation_patients():
    """
    Return predefined simulation patient data for demonstration.

    Returns:
        list: List of patient dictionaries.
    """
    return config.SIMULATION_PATIENTS.copy()
