from unittest.mock import MagicMock
from hospital import Hospital
from actions_for_commands import ActionsForCommands
from errors import PatientIDNotIntOrNegativeError, PatientIDNotExistsError, AttemptLowerMinimumStatusError, \
    PatientStatusNotExistsError

base_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}


class TestActionsForCommands:
    class TestGetPatientStatus:

        def test_get_patient_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 1
            hospital = Hospital(patients=[2, 3], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()

            input_output_manager.send_message_patient_status.assert_called_once_with('Слегка болен')

        def test_get_patient_status_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

        def test_get_patient_status_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(
                str(PatientIDNotIntOrNegativeError()))

        def test_get_patient_status_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

    class TestUpPatientStatus:

        def test_up_patient_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 1
            hospital = Hospital(patients=[0, 2], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()

            assert hospital._patients == [1, 2]
            input_output_manager.send_message_new_status.assert_called_once_with('Болен')

        def test_up_status_for_patient_maximum_status_patient_confirm_discharge(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            input_output_manager.request_for_discharge.return_value = True
            hospital = Hospital(patients=[0, 3, 1], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()

            assert hospital._patients == [0, None, 1]
            input_output_manager.send_message_patient_discharge.assert_called_once()

        def test_up_status_for_patient_maximum_status_patient_not_confirm_discharge(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            input_output_manager.request_for_discharge.return_value = False
            hospital = Hospital(patients=[0, 3, 1], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()

            assert hospital._patients == [0, 3, 1]
            input_output_manager.send_message_out_refusal_of_discharge.assert_called_once()

        def test_up_patient_status_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

        def test_up_patient_status_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(
                str(PatientIDNotIntOrNegativeError()))

        def test_up_patient_status_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.up_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

    class TestDownPatientStatus:

        def test_down_patient_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital(patients=[3, 1], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()

            assert hospital._patients == [3, 0]
            input_output_manager.send_message_new_status.assert_called_once_with('Тяжело болен')

        def test_down_status_for_patient_minimum_status(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 1
            hospital = Hospital(patients=[0, 3], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()

            assert hospital._patients == [0, 3]
            input_output_manager.send_message_new_status.send_message_with_received_text(
                str(AttemptLowerMinimumStatusError()))

        def test_down_patient_status_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

        def test_down_patient_status_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(
                str(PatientIDNotIntOrNegativeError()))

        def test_down_patient_status_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.down_patient_status()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

    class TestDischargePatient:

        def test_discharge_patient(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital(patients=[3, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()

            assert hospital._patients == [3, None]
            input_output_manager.send_message_patient_discharge.assert_called_once()

        def test_discharge_patient_id_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 4
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

        def test_discharge_patient_id_not_int_or_negative(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.side_effect = PatientIDNotIntOrNegativeError()
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()

            input_output_manager.send_message_with_received_text.assert_called_once_with(
                str(PatientIDNotIntOrNegativeError()))

        def test_discharge_patient_already_discharged(self):
            input_output_manager = MagicMock()
            input_output_manager.get_patient_id.return_value = 2
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.discharge_patient()

            input_output_manager.send_message_with_received_text.assert_called_once_with(str(PatientIDNotExistsError()))

    class TestGetHospitalStatistics:

        def test_get_hospital_statistics(self):
            input_output_manager = MagicMock()
            hospital = Hospital(patients=[3, 0, None, 2, 3], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.get_hospital_statistics()

            input_output_manager.send_message_hospital_statistics_text.assert_called_once_with(
                {'Готов к выписке': 2, 'Тяжело болен': 1, 'Слегка болен': 1}, 4)

    class TestAddNewPatient:
        def test_add_new_patient(self):
            input_output_manager = MagicMock()
            hospital = Hospital(patients=[1, 2, None], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)
            input_output_manager.get_new_patient_status.return_value = "Готов к выписке"
            actions_for_commands.add_new_patient()

            assert hospital._patients == [1, 2, None, 3]
            input_output_manager.send_message_patient_added.assert_called_once_with(4)

        def test_add_new_patient_status_not_exists(self):
            input_output_manager = MagicMock()
            input_output_manager.get_new_patient_status.return_value = "несуществующий статус"
            hospital = Hospital(patients=[], statuses=base_statuses)
            actions_for_commands = ActionsForCommands(input_output_manager, hospital)

            actions_for_commands.add_new_patient()

            input_output_manager.send_message_with_received_text.assert_called_once_with(
                str(PatientStatusNotExistsError()))
