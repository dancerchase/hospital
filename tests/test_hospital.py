import unittest
from hospital import Hospital
from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError


class TestHospital(unittest.TestCase):

    def setUp(self):
        self._hospital = Hospital()

    def test_get_patient_status_text_valid_sick(self):
        patient_id = 1
        self.assertEqual(self._hospital.get_patient_status_text(patient_id), "Болен")

    def test_get_patient_status_text_valid_very_sick(self):
        patient_id = 2
        self._hospital.down_status_for_patient(patient_id)
        self.assertEqual(self._hospital.get_patient_status_text(patient_id), "Тяжело болен")

    def test_get_patient_status_text_valid_slightly_sick(self):
        patient_id = 3
        self._hospital.up_status_for_patient(patient_id)
        self.assertEqual(self._hospital.get_patient_status_text(patient_id), "Слегка болен")

    def test_get_patient_status_text_valid_ready_to_discharge(self):
        patient_id = 4
        self._hospital.up_status_for_patient(patient_id)
        self._hospital.up_status_for_patient(patient_id)
        self.assertEqual(self._hospital.get_patient_status_text(patient_id), "Готов к выписке")

    def test_get_patient_status_text_invalid_id_too_high(self):
        with self.assertRaises(PatientIDNotExistsError):
            self._hospital.get_patient_status_text(201)

    def test_get_patient_status_text_patient_already_discharged(self):
        patient_id = 5
        self._hospital.patient_discharge(patient_id)
        with self.assertRaises(PatientIDNotExistsError):
            self._hospital.get_patient_status_text(patient_id)

    def test_down_status_for_patient(self):
        patient_id = 6
        self._hospital.down_status_for_patient(patient_id)
        self.assertEqual(self._hospital.get_patient_status_text(patient_id), "Тяжело болен")

    def test_down_status_for_patient_minimum_status(self):
        patient_id = 7
        self._hospital.down_status_for_patient(patient_id)
        with self.assertRaises(AttemptLowerMinimumStatusError):
            self._hospital.down_status_for_patient(patient_id)

    def test_down_status_for_patient_already_discharged(self):
        patient_id = 13
        self._hospital.patient_discharge(patient_id)
        with self.assertRaises(PatientIDNotExistsError):
            self._hospital.get_patient_status_text(patient_id)

    def test_get_statistics_patients_statuses(self):
        self._hospital.up_status_for_patient(8)
        self._hospital.up_status_for_patient(8)
        self._hospital.up_status_for_patient(9)
        self._hospital.down_status_for_patient(10)
        self._hospital.patient_discharge(11)
        self._hospital.get_patient_status_text(12)
        statistics = self._hospital.get_statistics_patients_statuses()
        self.assertEqual(statistics, {'Болен': 196, 'Слегка болен': 1, 'Тяжело болен': 1, 'Готов к выписке': 1})

    def test_get_total_number_patients(self):
        self.assertEqual(self._hospital.get_total_number_patients(), 200)
        self._hospital.patient_discharge(13)
        self._hospital.up_status_for_patient(14)
        self._hospital.down_status_for_patient(15)
        self._hospital.get_patient_status_text(15)
        self.assertEqual(self._hospital.get_total_number_patients(), 199)


if __name__ == '__main__':
    unittest.main()
