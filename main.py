"""
Patient Health Monitoring System - Main Application
====================================================
Interactive terminal-based patient health monitoring with Blynk IoT integration.

Usage:
    python main.py

This is an educational project for B.Tech college demonstration.
NOT intended for real medical diagnosis.
"""

import sys
import os
import time
import logging
from datetime import datetime

# Setup logging before importing project modules
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/monitoring.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

import config
import patient_monitor
import excel_service
from blynk_service import BlynkService


# Global Blynk service instance
blynk = None
latest_result = None
latest_patient_info = None


def print_banner():
    """Print the application banner."""
    print("\n" + "=" * 50)
    print("   PATIENT HEALTH MONITORING SYSTEM")
    print("   Educational IoT Project")
    print("=" * 50)


def print_menu():
    """Print the interactive menu."""
    print("\n" + "=" * 50)
    print("                  MAIN MENU")
    print("=" * 50)
    print("  1. Enter patient data manually")
    print("  2. Read patient data from Excel")
    print("  3. Test normal/warning/critical conditions")
    print("  4. Monitor Blynk emergency switch")
    print("  5. Start automatic monitoring")
    print("  6. View latest patient data")
    print("  7. Check Blynk connection")
    print("  8. Launch Live Web Dashboard (Browser)")
    print("  9. Exit")
    print("=" * 50)


def startup_check():
    """
    Perform startup checks for the environment, .env file, and Blynk connection.
    """
    global blynk

    print("\n--- Startup Check ---\n")

    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  [OK] Python {py_version}")

    # Check .env file
    if os.path.exists(config.ENV_FILE):
        print(f"  [OK] Environment file found ({config.ENV_FILE})")
    else:
        print(f"  [WARNING] Environment file not found ({config.ENV_FILE})")
        print("           Blynk features will be disabled.")
        print("           Create a .env file with: BLYNK_AUTH_TOKEN=your_token")

    # Initialize Blynk service
    blynk = BlynkService()

    if blynk.is_configured():
        print(f"  [OK] Blynk token configured ({blynk.get_masked_token()})")

        # Test Blynk connection
        ok, msg = blynk.check_connection()
        if ok:
            print(f"  [OK] {msg}")
        else:
            print(f"  [WARNING] Blynk connection: {msg}")
            print("           Local monitoring will continue without Blynk.")
    else:
        print("  [WARNING] Blynk token not configured")
        print("           Local monitoring will work without Blynk.")

    # Check Excel file
    if os.path.exists(config.EXCEL_FILE):
        print(f"  [OK] Excel file found ({config.EXCEL_FILE})")
    else:
        print(f"  [INFO] Excel file not found. Creating sample file...")
        if excel_service.create_sample_excel():
            print(f"  [OK] Sample Excel file created ({config.EXCEL_FILE})")
        else:
            print(f"  [WARNING] Could not create sample Excel file.")

    # Check logs directory
    if os.path.exists("logs"):
        print("  [OK] Logs directory ready")
    else:
        os.makedirs("logs", exist_ok=True)
        print("  [OK] Logs directory created")

    logger.info("Application started. Startup checks completed.")
    print("\n" + "-" * 50)


def option_manual_input():
    """Option 1: Enter patient data manually."""
    global latest_result, latest_patient_info

    data = patient_monitor.get_manual_patient_data()
    if data is None:
        return

    heart_rate, spo2, temperature = data

    result = patient_monitor.evaluate_patient(heart_rate, spo2, temperature)
    patient_monitor.display_patient_result(result, patient_id="Manual Entry")

    latest_result = result
    latest_patient_info = {"patient_id": "Manual", "patient_name": "Manual Entry"}

    # Send to Blynk if available
    _send_to_blynk(heart_rate, spo2, temperature, result["overall_status"])


def option_read_excel():
    """Option 2: Read patient data from Excel."""
    global latest_result, latest_patient_info

    print(f"\n  Reading from: {config.EXCEL_FILE}")

    ok, data = excel_service.read_patient_data()

    if not ok:
        print(f"\n  [ERROR] {data}")
        return

    patients = data
    print(f"\n  Found {len(patients)} patient(s) in Excel file.\n")

    for patient in patients:
        hr = patient["heart_rate"]
        spo2 = patient["spo2"]
        temp = patient["temperature"]

        result = patient_monitor.evaluate_patient(hr, spo2, temp)
        patient_monitor.display_patient_result(
            result,
            patient_id=patient["patient_id"],
            patient_name=patient["patient_name"],
        )

        latest_result = result
        latest_patient_info = {
            "patient_id": patient["patient_id"],
            "patient_name": patient["patient_name"],
        }

    # Ask if user wants to send last patient data to Blynk
    if blynk and blynk.is_configured():
        try:
            choice = input(
                "  Send last patient's data to Blynk? (y/n): "
            ).strip().lower()
            if choice == "y":
                last = patients[-1]
                _send_to_blynk(
                    last["heart_rate"],
                    last["spo2"],
                    last["temperature"],
                    latest_result["overall_status"],
                )
        except KeyboardInterrupt:
            print("\n  Cancelled.")


def option_test_conditions():
    """Option 3: Test all three conditions using simulation data."""
    global latest_result, latest_patient_info

    print("\n--- Testing Normal / Warning / Critical Conditions ---\n")
    print("  Using predefined simulation patients:\n")

    sim_patients = patient_monitor.get_simulation_patients()

    for patient in sim_patients:
        hr = patient["heart_rate"]
        spo2 = patient["spo2"]
        temp = patient["temperature"]

        result = patient_monitor.evaluate_patient(hr, spo2, temp)
        patient_monitor.display_patient_result(
            result,
            patient_id=patient["patient_id"],
            patient_name=patient["patient_name"],
        )

        latest_result = result
        latest_patient_info = {
            "patient_id": patient["patient_id"],
            "patient_name": patient["patient_name"],
        }


def option_emergency_switch():
    """Option 4: Monitor Blynk emergency switch (V4) continuously."""
    if not blynk or not blynk.is_configured():
        print("\n  [ERROR] Blynk is not configured. Cannot monitor emergency switch.")
        print("         Configure your Blynk token in the .env file.")
        return

    print("\n--- Emergency Switch Monitor ---")
    print("  Monitoring Blynk V4 (Emergency Switch)")
    print("  Press Ctrl+C to stop.\n")

    last_state = None
    logger.info("Emergency switch monitoring started.")

    try:
        while True:
            ok, value = blynk.get_emergency_switch()

            if ok:
                current_state = int(value)

                if current_state != last_state:
                    # State changed
                    if current_state == 1:
                        print("\n  " + "!" * 44)
                        print("  !!! EMERGENCY SWITCH ACTIVATED (V4 = ON) !!!")
                        print("  " + "!" * 44)
                        logger.critical("EMERGENCY SWITCH ACTIVATED!")
                    else:
                        print(f"  [{datetime.now().strftime('%H:%M:%S')}] "
                              f"Emergency Switch: OFF")
                        logger.info("Emergency switch deactivated.")

                    last_state = current_state
                else:
                    # Same state - print status periodically
                    state_str = "ON" if current_state == 1 else "OFF"
                    print(f"  [{datetime.now().strftime('%H:%M:%S')}] "
                          f"Emergency Switch: {state_str} (no change)")

            else:
                print(f"  [{datetime.now().strftime('%H:%M:%S')}] "
                      f"[ERROR] {value}")

            time.sleep(config.EMERGENCY_POLL_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n  Emergency switch monitoring stopped.")
        logger.info("Emergency switch monitoring stopped by user.")


def option_automatic_monitoring():
    """Option 5: Start automatic monitoring with simulation data."""
    global latest_result, latest_patient_info

    print("\n--- Automatic Monitoring Mode ---")
    print("  Using simulation data for demonstration.")
    print("  Press Ctrl+C to stop.\n")

    logger.info("Automatic monitoring started.")

    sim_patients = patient_monitor.get_simulation_patients()
    patient_index = 0

    try:
        while True:
            patient = sim_patients[patient_index % len(sim_patients)]
            hr = patient["heart_rate"]
            spo2 = patient["spo2"]
            temp = patient["temperature"]

            result = patient_monitor.evaluate_patient(hr, spo2, temp)
            patient_monitor.display_patient_result(
                result,
                patient_id=patient["patient_id"],
                patient_name=patient["patient_name"],
            )

            latest_result = result
            latest_patient_info = {
                "patient_id": patient["patient_id"],
                "patient_name": patient["patient_name"],
            }

            # Send to Blynk
            blynk_msg = _send_to_blynk(
                hr, spo2, temp, result["overall_status"]
            )
            if blynk_msg:
                print(f"  Blynk: {blynk_msg}")

            patient_index += 1

            print(f"\n  Next reading in {config.MONITORING_INTERVAL} seconds...")
            print("  (Press Ctrl+C to stop)\n")
            time.sleep(config.MONITORING_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n  Automatic monitoring stopped.")
        logger.info("Automatic monitoring stopped by user.")


def option_view_latest():
    """Option 6: View the latest patient data."""
    global latest_result, latest_patient_info

    if latest_result is None:
        print("\n  [INFO] No patient data available yet.")
        print("         Use option 1, 2, 3, or 5 to process patient data first.")
        return

    print("\n--- Latest Patient Data ---")

    patient_id = latest_patient_info.get("patient_id", "Unknown")
    patient_name = latest_patient_info.get("patient_name", "Unknown")

    patient_monitor.display_patient_result(
        latest_result,
        patient_id=patient_id,
        patient_name=patient_name,
    )


def option_check_blynk():
    """Option 7: Check Blynk connection."""
    global blynk

    print("\n--- Blynk Connection Check ---\n")

    if not blynk:
        blynk = BlynkService()

    if not blynk.is_configured():
        print("  [ERROR] Blynk token not configured.")
        print("          Edit .env file and add: BLYNK_AUTH_TOKEN=your_token")
        return

    print(f"  Token: {blynk.get_masked_token()}")

    ok, msg = blynk.check_connection()
    if ok:
        print(f"  [OK] {msg}")
    else:
        print(f"  [ERROR] {msg}")
        print("          Local monitoring will continue without Blynk.")


def option_web_dashboard():
    """Option 8: Launch interactive Live Web Dashboard in default browser."""
    import webbrowser
    html_path = os.path.abspath("index.html")
    if os.path.exists(html_path):
        print(f"\n  [OK] Opening Live Web Dashboard in your browser...")
        print(f"  File: {html_path}")
        webbrowser.open(f"file:///{html_path}")
    else:
        print("\n  [ERROR] index.html not found.")


def _send_to_blynk(heart_rate, spo2, temperature, status_str):
    """
    Helper to send patient data to Blynk.

    Args:
        heart_rate (float): Heart rate.
        spo2 (float): SpO2.
        temperature (float): Temperature.
        status_str (str): Status string (NORMAL/WARNING/CRITICAL).

    Returns:
        str: Status message.
    """
    if not blynk or not blynk.is_configured():
        return "Blynk not configured (local mode)"

    status_code = config.STATUS_CODES.get(status_str, 0)
    ok, msg = blynk.send_patient_data(heart_rate, spo2, temperature, status_code)

    if ok:
        return "Data sent to Blynk ✓"
    else:
        return f"Blynk update failed: {msg}"


def main():
    """Main application entry point."""
    print_banner()
    startup_check()

    while True:
        try:
            print_menu()
            choice = input("  Enter your choice (1-9): ").strip()

            if choice == "1":
                option_manual_input()
            elif choice == "2":
                option_read_excel()
            elif choice == "3":
                option_test_conditions()
            elif choice == "4":
                option_emergency_switch()
            elif choice == "5":
                option_automatic_monitoring()
            elif choice == "6":
                option_view_latest()
            elif choice == "7":
                option_check_blynk()
            elif choice == "8":
                option_web_dashboard()
            elif choice == "9":
                print("\n  Exiting Patient Health Monitoring System.")
                print("  Thank you!\n")
                logger.info("Application exited by user.")
                break
            else:
                print(f"\n  [!] Invalid choice: '{choice}'. Please enter 1-9.")

        except KeyboardInterrupt:
            print("\n\n  Use option 8 to exit, or press Ctrl+C again to force quit.")
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n  Force quit.")
                logger.info("Application force-quit by user.")
                break

        except Exception as e:
            print(f"\n  [ERROR] Unexpected error: {e}")
            logger.error("Unexpected error in main loop: %s", e, exc_info=True)


if __name__ == "__main__":
    main()
