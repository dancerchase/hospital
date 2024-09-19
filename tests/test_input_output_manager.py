import pytest
from unittest.mock import MagicMock, call
from input_output.input_output_manager import InputOutputManager
from errors import PatientIDNotIntOrNegativeError


class TestInputOutputManager:
    class TestRequestForDischarge:

        def test_request_for_discharge_confirm(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            console.input.return_value = 'да'

            assert input_output_manager.request_for_discharge()
            console.input.assert_called_once_with('Желаете этого клиента выписать? (да/нет): ')

        def test_request_for_discharge_not_confirm(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            console.input.return_value = 'нет'

            assert not input_output_manager.request_for_discharge()
            console.input.assert_called_once_with('Желаете этого клиента выписать? (да/нет): ')

    class TestGetPatientId:

        def test_get_patient_id(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            console.input.return_value = '55'

            assert input_output_manager.get_patient_id() == 55
            console.input.assert_called_once_with('Введите ID пациента: ')

        @pytest.mark.parametrize('invalid_data', ['0', '-1', 'asd', '', ' '])
        def test_get_patient_id_invalid_data(self, invalid_data):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            console.input.return_value = invalid_data

            with pytest.raises(PatientIDNotIntOrNegativeError):
                input_output_manager.get_patient_id()

            console.input.assert_called_once_with('Введите ID пациента: ')

    class TestGetCommandFromUser:

        def test_get_command_from_user(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            console.input.return_value = 'узнать статус пациента'

            assert input_output_manager.get_command_from_user() == 'узнать статус пациента'
            console.input.assert_called_once_with('Введите команду: ')

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

            console.print.assert_called_once_with('Неизвестная команда! Попробуйте ещё раз')

        def test_send_message_new_status(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            new_status = 'Болен'

            input_output_manager.send_message_new_status(new_status)

            console.print.assert_called_once_with(f'Новый статус пациента: "Болен"')

        def test_send_message_out_refusal_of_discharge(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_out_refusal_of_discharge()

            console.print.assert_called_once_with('Пациент остался в статусе "Готов к выписке"')

        def test_send_message_patient_discharge(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_patient_discharge()

            console.print.assert_called_once_with('Пациент выписан из больницы')

        def test_send_message_application_stop(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_application_stop()

            console.print.assert_called_once_with('Сеанс завершён.')

        def test_send_message_hospital_statistics_text(self):
            console = MagicMock()
            statistics = {'Болен': 5, 'Готов к выписке': 1}
            total_patients = 6
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_hospital_statistics_text(statistics, total_patients)

            console.print.assert_has_calls([
                call.print('В больнице на данный момент находится 6 чел., из них:' +
                           '\n    - в статусе "Болен": 5 чел.' +
                           '\n    - в статусе "Готов к выписке": 1 чел.')])

        def test_send_message_patient_status_text(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)
            patient_status = 'Болен'

            input_output_manager.send_message_patient_status(patient_status)

            console.print.assert_called_once_with(f'Статус пациента: "Болен"')

        def test_send_message_with_received_text(self):
            console = MagicMock()
            input_output_manager = InputOutputManager(console)

            input_output_manager.send_message_with_received_text('Текст ошибки')

            console.print.assert_called_once_with('Текст ошибки')
