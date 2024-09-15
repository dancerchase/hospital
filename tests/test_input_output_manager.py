import pytest
from input_output_manager import InputOutputManager
from errors import PatientIDNotIntOrNegativeError


class TestInputOutputManager:

    def test_convert_patient_id_from_str_to_positive_int(self):
        assert InputOutputManager._convert_patient_id_from_str_to_positive_int('56') == 56

    @pytest.mark.parametrize('invalid_data', ['0', '-1', 'asd', '', ' '])
    def test_convert_patient_id_from_str_to_positive_int_invalid_data(self, invalid_data):
        with pytest.raises(PatientIDNotIntOrNegativeError):
            InputOutputManager._convert_patient_id_from_str_to_positive_int(invalid_data)


