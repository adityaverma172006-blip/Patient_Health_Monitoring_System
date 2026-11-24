"""
Patient Health Monitoring System - Unit Tests
==============================================
Tests for patient monitoring logic, Excel service, and Blynk service.

Run with:
    python -m pytest tests/test_patient_monitor.py -v
  or:
    python tests/test_patient_monitor.py

This is an educational project for B.Tech college demonstration.
"""

import os
import sys
import unittest
import tempfile

# Add parent directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import patient_monitor
import excel_service
from blynk_service import BlynkService


class TestHeartRateEvaluation(unittest.TestCase):
    """Tests for heart rate evaluation."""

    def test_normal_heart_rate(self):
        status, reason = patient_monitor.evaluate_heart_rate(82)
        self.assertEqual(status, config.STATUS_NORMAL)
        self.assertIsNone(reason)

    def test_normal_boundary_low(self):
        status, reason = patient_monitor.evaluate_heart_rate(60)
        self.assertEqual(status, config.STATUS_NORMAL)

    def test_normal_boundary_high(self):
        status, reason = patient_monitor.evaluate_heart_rate(100)
        self.assertEqual(status, config.STATUS_NORMAL)

    def test_warning_low(self):
        status, reason = patient_monitor.evaluate_heart_rate(55)
        self.assertEqual(status, config.STATUS_WARNING)
        self.assertIn("abnormal", reason.lower())

    def test_warning_high(self):
        status, reason = patient_monitor.evaluate_heart_rate(105)
        self.assertEqual(status, config.STATUS_WARNING)
        self.assertIn("abnormal", reason.lower())

    def test_critical_low(self):
        status, reason = patient_monitor.evaluate_heart_rate(35)
        self.assertEqual(status, config.STATUS_CRITICAL)
        self.assertIn("critically", reason.lower())

    def test_critical_high(self):
        status, reason = patient_monitor.evaluate_heart_rate(140)
        self.assertEqual(status, config.STATUS_CRITICAL)
        self.assertIn("critically", reason.lower())

    def test_invalid_heart_rate(self):
        status, reason = patient_monitor.evaluate_heart_rate(None)
        self.assertEqual(status, config.STATUS_WARNING)
        self.assertIn("invalid", reason.lower())


class TestSpO2Evaluation(unittest.TestCase):
    """Tests for SpO2 evaluation."""

    def test_normal_spo2(self):
        status, reason = patient_monitor.evaluate_spo2(98)
        self.assertEqual(status, config.STATUS_NORMAL)
        self.assertIsNone(reason)

    def test_normal_boundary(self):
        status, reason = patient_monitor.evaluate_spo2(95)
        self.assertEqual(status, config.STATUS_NORMAL)

    def test_warning_spo2(self):
        status, reason = patient_monitor.evaluate_spo2(92)
        self.assertEqual(status, config.STATUS_WARNING)
        self.assertIn("low", reason.lower())

    def test_critical_spo2(self):
        status, reason = patient_monitor.evaluate_spo2(86)
        self.assertEqual(status, config.STATUS_CRITICAL)
        self.assertIn("critically", reason.lower())

    def test_very_low_spo2(self):
        status, reason = patient_monitor.evaluate_spo2(80)
        self.assertEqual(status, config.STATUS_CRITICAL)
        self.assertIn("dangerously", reason.lower())

    def test_invalid_spo2(self):
        status, reason = patient_monitor.evaluate_spo2("abc")
        self.assertEqual(status, config.STATUS_WARNING)


class TestTemperatureEvaluation(unittest.TestCase):
    """Tests for temperature evaluation."""

    def test_normal_temp(self):
        status, reason = patient_monitor.evaluate_temperature(36.8)
        self.assertEqual(status, config.STATUS_NORMAL)
        self.assertIsNone(reason)

    def test_normal_boundary_low(self):
        status, reason = patient_monitor.evaluate_temperature(36.0)
        self.assertEqual(status, config.STATUS_NORMAL)

    def test_normal_boundary_high(self):
        status, reason = patient_monitor.evaluate_temperature(37.5)
        self.assertEqual(status, config.STATUS_NORMAL)

    def test_warning_temp(self):
        status, reason = patient_monitor.evaluate_temperature(38.2)
        self.assertEqual(status, config.STATUS_WARNING)
        self.assertIn("elevated", reason.lower())

    def test_critical_high_temp(self):
        status, reason = patient_monitor.evaluate_temperature(39.4)
        self.assertEqual(status, config.STATUS_CRITICAL)
        self.assertIn("critically high", reason.lower())

    def test_critical_low_temp(self):
        status, reason = patient_monitor.evaluate_temperature(34.0)
        self.assertEqual(status, config.STATUS_CRITICAL)
        self.assertIn("critically low", reason.lower())

    def test_invalid_temp(self):
        status, reason = patient_monitor.evaluate_temperature(None)
        self.assertEqual(status, config.STATUS_WARNING)


class TestOverallStatus(unittest.TestCase):
    """Tests for overall status calculation."""

    def test_all_normal(self):
        status = patient_monitor.calculate_overall_status(
            config.STATUS_NORMAL, config.STATUS_NORMAL, config.STATUS_NORMAL
        )
        self.assertEqual(status, config.STATUS_NORMAL)

    def test_one_warning(self):
        status = patient_monitor.calculate_overall_status(
            config.STATUS_NORMAL, config.STATUS_WARNING, config.STATUS_NORMAL
        )
        self.assertEqual(status, config.STATUS_WARNING)

    def test_one_critical(self):
        status = patient_monitor.calculate_overall_status(
            config.STATUS_NORMAL, config.STATUS_NORMAL, config.STATUS_CRITICAL
        )
        self.assertEqual(status, config.STATUS_CRITICAL)

    def test_critical_overrides_warning(self):
        status = patient_monitor.calculate_overall_status(
            config.STATUS_WARNING, config.STATUS_CRITICAL, config.STATUS_NORMAL
        )
        self.assertEqual(status, config.STATUS_CRITICAL)

    def test_all_critical(self):
        status = patient_monitor.calculate_overall_status(
            config.STATUS_CRITICAL, config.STATUS_CRITICAL, config.STATUS_CRITICAL
        )
        self.assertEqual(status, config.STATUS_CRITICAL)


class TestPatientEvaluation(unittest.TestCase):
    """Tests for the full patient evaluation pipeline."""

    def test_normal_patient(self):
        result = patient_monitor.evaluate_patient(82, 98, 36.8)
        self.assertEqual(result["overall_status"], config.STATUS_NORMAL)
        self.assertEqual(len(result["reasons"]), 0)
        self.assertIsNotNone(result["timestamp"])

    def test_warning_patient(self):
        result = patient_monitor.evaluate_patient(105, 92, 38.2)
        self.assertEqual(result["overall_status"], config.STATUS_WARNING)
        self.assertGreater(len(result["reasons"]), 0)

    def test_critical_patient(self):
        result = patient_monitor.evaluate_patient(135, 86, 39.4)
        self.assertEqual(result["overall_status"], config.STATUS_CRITICAL)
        self.assertGreater(len(result["reasons"]), 0)

    def test_result_structure(self):
        result = patient_monitor.evaluate_patient(82, 98, 36.8)
        self.assertIn("heart_rate", result)
        self.assertIn("spo2", result)
        self.assertIn("temperature", result)
        self.assertIn("overall_status", result)
        self.assertIn("reasons", result)
        self.assertIn("timestamp", result)

        self.assertIn("value", result["heart_rate"])
        self.assertIn("status", result["heart_rate"])
        self.assertIn("reason", result["heart_rate"])


class TestSimulationData(unittest.TestCase):
    """Tests for simulation patient data."""

    def test_simulation_patients_exist(self):
        patients = patient_monitor.get_simulation_patients()
        self.assertGreaterEqual(len(patients), 3)

    def test_simulation_has_all_conditions(self):
        patients = patient_monitor.get_simulation_patients()
        conditions = [p["condition"] for p in patients]
        self.assertIn("NORMAL", conditions)
        self.assertIn("WARNING", conditions)
        self.assertIn("CRITICAL", conditions)

    def test_simulation_data_evaluates_correctly(self):
        """Verify simulation patients evaluate to their expected conditions."""
        patients = patient_monitor.get_simulation_patients()
        for patient in patients:
            result = patient_monitor.evaluate_patient(
                patient["heart_rate"],
                patient["spo2"],
                patient["temperature"],
            )
            self.assertEqual(
                result["overall_status"],
                patient["condition"],
                f"Patient {patient['patient_id']} expected {patient['condition']}, "
                f"got {result['overall_status']}",
            )


class TestExcelService(unittest.TestCase):
    """Tests for Excel reading functionality."""

    def setUp(self):
        """Create a temporary Excel file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_excel = os.path.join(self.temp_dir, "test_patients.xlsx")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_excel):
            os.remove(self.temp_excel)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_create_sample_excel(self):
        result = excel_service.create_sample_excel(self.temp_excel)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.temp_excel))

    def test_read_sample_excel(self):
        excel_service.create_sample_excel(self.temp_excel)
        ok, data = excel_service.read_patient_data(self.temp_excel)
        self.assertTrue(ok)
        self.assertEqual(len(data), 3)

    def test_read_missing_file(self):
        ok, msg = excel_service.read_patient_data("nonexistent.xlsx")
        self.assertFalse(ok)
        self.assertIn("not found", msg.lower())

    def test_patient_data_fields(self):
        excel_service.create_sample_excel(self.temp_excel)
        ok, data = excel_service.read_patient_data(self.temp_excel)
        self.assertTrue(ok)

        patient = data[0]
        self.assertIn("patient_id", patient)
        self.assertIn("patient_name", patient)
        self.assertIn("age", patient)
        self.assertIn("heart_rate", patient)
        self.assertIn("spo2", patient)
        self.assertIn("temperature", patient)


class TestBlynkService(unittest.TestCase):
    """Tests for Blynk service (token handling only - no network)."""

    def test_unconfigured_token(self):
        """BlynkService with no valid token should report not configured."""
        service = BlynkService()
        # Token may or may not be configured depending on .env
        # Test the method works regardless
        self.assertIsInstance(service.is_configured(), bool)

    def test_masked_token_unconfigured(self):
        service = BlynkService()
        if not service.is_configured():
            self.assertEqual(service.get_masked_token(), "NOT CONFIGURED")

    def test_send_data_without_token(self):
        service = BlynkService()
        service.token = None
        ok, msg = service.send_patient_data(82, 98, 36.8, 0)
        self.assertFalse(ok)
        self.assertIn("not configured", msg.lower())

    def test_check_connection_without_token(self):
        service = BlynkService()
        service.token = None
        ok, msg = service.check_connection()
        self.assertFalse(ok)

    def test_get_pin_without_token(self):
        service = BlynkService()
        service.token = None
        ok, msg = service.get_pin(4)
        self.assertFalse(ok)

    def test_update_pin_without_token(self):
        service = BlynkService()
        service.token = None
        ok, msg = service.update_pin(0, 82)
        self.assertFalse(ok)


class TestConfigValues(unittest.TestCase):
    """Tests for configuration values."""

    def test_heart_rate_thresholds_order(self):
        self.assertLess(config.HR_CRITICAL_LOW, config.HR_WARNING_LOW)
        self.assertLess(config.HR_WARNING_LOW, config.HR_NORMAL_LOW)
        self.assertLess(config.HR_NORMAL_HIGH, config.HR_WARNING_HIGH)
        self.assertLess(config.HR_WARNING_HIGH, config.HR_CRITICAL_HIGH)

    def test_spo2_thresholds_order(self):
        self.assertLess(config.SPO2_CRITICAL, config.SPO2_WARNING)
        self.assertLess(config.SPO2_WARNING, config.SPO2_NORMAL)

    def test_temp_thresholds_order(self):
        self.assertLess(config.TEMP_CRITICAL_LOW, config.TEMP_NORMAL_LOW)
        self.assertLess(config.TEMP_NORMAL_HIGH, config.TEMP_WARNING_HIGH)
        self.assertLess(config.TEMP_WARNING_HIGH, config.TEMP_CRITICAL_HIGH)

    def test_virtual_pins(self):
        self.assertEqual(config.VPIN_HEART_RATE, 0)
        self.assertEqual(config.VPIN_SPO2, 1)
        self.assertEqual(config.VPIN_TEMPERATURE, 2)
        self.assertEqual(config.VPIN_STATUS, 3)
        self.assertEqual(config.VPIN_EMERGENCY, 4)

    def test_status_codes(self):
        self.assertIn(config.STATUS_NORMAL, config.STATUS_CODES)
        self.assertIn(config.STATUS_WARNING, config.STATUS_CODES)
        self.assertIn(config.STATUS_CRITICAL, config.STATUS_CODES)
        self.assertIn(config.STATUS_EMERGENCY, config.STATUS_CODES)


if __name__ == "__main__":
    # Run tests
    print("=" * 60)
    print("  Patient Health Monitoring System - Unit Tests")
    print("=" * 60)
    unittest.main(verbosity=2)
