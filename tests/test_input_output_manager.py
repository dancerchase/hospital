import pytest
from unittest.mock import MagicMock
from input_output.input_output_manager import InputOutputManager
from errors import PatientIDNotIntOrNegativeError


class TestInputOutputManager:
    class TestRequestForDischarge:

        def test_request_for_discharge_confirm(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            console.request_for_discharge.return_value = 'да'
            assert input_output_manager.request_for_discharge()
            console.request_for_discharge.assert_called_once()

        def test_request_for_discharge_not_confirm(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            console.request_for_discharge.return_value = 'нет'
            assert not input_output_manager.request_for_discharge()
            console.request_for_discharge.assert_called_once()

    class TestGetPatientId:

        def test_get_patient_id(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            console.get_patient_id.return_value = '55'
            assert input_output_manager.get_patient_id() == 55
            console.get_patient_id.assert_called_once()

        @pytest.mark.parametrize('invalid_data', ['0', '-1', 'asd', '', ' '])
        def test_get_patient_id_invalid_data(self, invalid_data):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            console.get_patient_id.return_value = invalid_data
            with pytest.raises(PatientIDNotIntOrNegativeError):
                input_output_manager.get_patient_id()
            console.get_patient_id.assert_called_once()

    class TestGetCommandFromUser:

        def test_get_command_from_user(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            console.get_command_from_user.return_value = 'узнать статус пациента'
            assert input_output_manager.get_command_from_user() == 'узнать статус пациента'
            console.get_command_from_user.assert_called_once()

    class TestConvertPatientIdFromStrToPositiveInt:
        def test_convert_patient_id_from_str_to_positive_int(self):
            assert InputOutputManager._convert_patient_id_from_str_to_positive_int('56') == 56

        @pytest.mark.parametrize('invalid_data', ['0', '-1', 'asd', '', ' '])
        def test_convert_patient_id_from_str_to_positive_int_invalid_data(self, invalid_data):
            with pytest.raises(PatientIDNotIntOrNegativeError):
                InputOutputManager._convert_patient_id_from_str_to_positive_int(invalid_data)

    class TestSendMessage:

        def test_send_message_command_not_exist_error(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_command_not_exist_error()
            console.send_message_command_not_exist_error.assert_called_once()

        def test_send_message_new_status(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_new_status('Болен')
            console.send_message_new_status.assert_called_once_with('Болен')

        def test_send_message_out_refusal_of_discharge(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_out_refusal_of_discharge()
            console.send_message_out_refusal_of_discharge.assert_called_once()

        def test_send_message_patient_discharge(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_patient_discharge()
            console.send_message_patient_discharge.assert_called_once()

        def test_send_message_application_stop(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_application_stop()
            console.send_message_application_stop.assert_called_once()

        def test_send_message_hospital_statistics_text(self):
            console = MagicMock()
            statistics = {'Болен': 5, 'Готов к выписке': 1}
            total_patients = 6
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_hospital_statistics_text(statistics, total_patients)
            console.send_message_hospital_statistics_text.assert_called_once_with(statistics, total_patients)

        def test_send_message_patient_status_text(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_patient_status_text('Болен')
            console.send_message_patient_status_text.assert_called_once_with('Болен')

        def test_send_message_with_received_text(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_with_received_text('Текст ошибки')
            console.send_message_with_received_text.assert_called_once_with('Текст ошибки')
