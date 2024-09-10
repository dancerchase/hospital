import unittest
from input_output_manager import InputOutputManager
from errors import PatientIDNotIntOrNegativeError


class TestInputOutputManager(unittest.TestCase):
    def setUp(self):
        self.input_output_manager = InputOutputManager()

    def test_convert_patient_id_from_str_to_positive_int(self):
        self.assertEqual(InputOutputManager.convert_patient_id_from_str_to_positive_int('1'), 1)
        self.assertEqual(InputOutputManager.convert_patient_id_from_str_to_positive_int('200'), 200)

    def test_convert_patient_id_from_str_to_positive_int_invalid(self):
        with self.assertRaises(PatientIDNotIntOrNegativeError):
            InputOutputManager.convert_patient_id_from_str_to_positive_int('0')
            InputOutputManager.convert_patient_id_from_str_to_positive_int('-1')
            InputOutputManager.convert_patient_id_from_str_to_positive_int('asd')
            InputOutputManager.convert_patient_id_from_str_to_positive_int('')
            InputOutputManager.convert_patient_id_from_str_to_positive_int(' ')

