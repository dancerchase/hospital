from unittest.mock import MagicMock
from hospital import Hospital
from actions_for_commands import ActionsForCommands
from errors import PatientIDNotIntOrNegativeError


class TestActionsForCommands:
    class TestGetPatientStatus:

        def test_get_patient_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 1
            hospital = Hospital([2, 3])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()
            input_output_manager.send_message_patient_status_text.assert_called_once_with('Слегка болен')

        def test_get_patient_status_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

        def test_get_patient_status_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. ID пациента должно быть числом (целым, положительным)')

        def test_get_patient_status_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital([1, None, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

    class TestUpPatientStatus:

        def test_up_patient_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 1
            hospital = Hospital([0, 2])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()
            input_output_manager.send_message_new_status.assert_called_once_with('Болен')
            assert hospital._patients == [1, 2]

        def test_up_status_for_patient_maximum_status_patient_confirm_discharge(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            input_output_manager.request_for_discharge.return_value = True
            hospital = Hospital([0, 3, 1])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()
            input_output_manager.send_message_patient_discharge.assert_called_once()
            assert hospital._patients == [0, None, 1]

        def test_up_status_for_patient_maximum_status_patient_not_confirm_discharge(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            input_output_manager.request_for_discharge.return_value = False
            hospital = Hospital([0, 3, 1])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()
            input_output_manager.send_message_out_refusal_of_discharge.assert_called_once()
            assert hospital._patients == [0, 3, 1]

        def test_up_patient_status_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

        def test_up_patient_status_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. ID пациента должно быть числом (целым, положительным)')

        def test_up_patient_status_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital([1, None, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

    class TestDownPatientStatus:

        def test_down_patient_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital([3, 1])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()
            input_output_manager.send_message_new_status.assert_called_once_with('Тяжело болен')
            assert hospital._patients == [3, 0]

        def test_down_status_for_patient_minimum_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 1
            hospital = Hospital([0, 3])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()
            input_output_manager.send_message_new_status.send_message_with_received_text(
                'Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')
            assert hospital._patients == [0, 3]

        def test_down_patient_status_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

        def test_down_patient_status_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. ID пациента должно быть числом (целым, положительным)')

        def test_down_patient_status_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital([1, None, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

    class TestDischargePatient:

        def test_discharge_patient(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital([3, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()
            input_output_manager.send_message_patient_discharge.assert_called_once()
            assert hospital._patients == [3, None]

        def test_discharge_patient_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

        def test_discharge_patient_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital([2, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. ID пациента должно быть числом (целым, положительным)')

        def test_discharge_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital([1, None, 0])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()
            input_output_manager.send_message_with_received_text.assert_called_once_with(
                'Ошибка. В больнице нет пациента с таким ID')

    class TestGetHospitalStatistics:

        def test_get_hospital_statistics(self):
            input_output_manager = MagicMock()
            hospital = Hospital([3, 0, None, 2, 3])
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_hospital_statistics()
            input_output_manager.send_message_hospital_statistics_text.assert_called_once_with(
                {'Готов к выписке': 2, 'Тяжело болен': 1, 'Слегка болен': 1}, 4)
