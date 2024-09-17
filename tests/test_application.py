import pytest
from unittest.mock import MagicMock, call
from hospital import Hospital
from actions_for_commands import ActionsForCommands
from input_output.input_output_manager import InputOutputManager
from application import Application


class TestApplication:

    def test_one_base_scenario(self):
        console = MagicMock()
        input_output_manager = InputOutputManager(console)
        hospital = Hospital()
        actions_for_commands = ActionsForCommands(input_output_manager, hospital)
        application = Application(input_output_manager, actions_for_commands)

        # step 1
        console.input.return_value = 'узнать статус пациента'
        console.input.return_value = '200'

        input_output_manager.get_command_from_user()
        input_output_manager.get_patient_id()

        input_output_manager.send_message_patient_status('Болен')

        # step 2
        console.input.return_value = 'status up'
        console.input.return_value = '2'

        input_output_manager.get_command_from_user()
        input_output_manager.get_patient_id()

        input_output_manager.send_message_new_status('Слегка болен')

        # step 3
        console.input.return_value = 'status down'
        console.input.return_value = '3'

        input_output_manager.get_command_from_user()
        input_output_manager.get_patient_id()

        input_output_manager.send_message_new_status('Тяжело болен')

        # step 4
        console.input.return_value = 'discharge'
        console.input.return_value = '4'

        input_output_manager.get_command_from_user()
        input_output_manager.get_patient_id()

        input_output_manager.send_message_patient_discharge()

        # step 5
        console.input.return_value = 'рассчитать статистику'

        input_output_manager.get_command_from_user()

        input_output_manager.send_message_hospital_statistics_text(
            {'Болен': 197, 'Слегка болен': 1, 'Тяжело болен': 1}, 199)

        # step 6
        console.input.return_value = 'стоп'

        input_output_manager.get_command_from_user()

        input_output_manager.send_message_application_stop()

        # start
        application.run_application()

        console.assert_has_calls([
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.output('Статус пациента: "Болен"'),
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.output('Новый статус пациента: "Слегка болен"'),
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.output('Новый статус пациента: "Тяжело болен"'),
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.output('Пациент выписан из больницы'),
            call.input('Введите команду: '),
            call.output('В больнице на данный момент находится 199 чел., из них:'),
            call.output('    - в статусе "Болен": 197 чел.'),
            call.output('    - в статусе "Слегка болен": 1 чел.'),
            call.output('    - в статусе "Тяжело болен": 1 чел.'),
            call.input('Введите команду: '),
            call.output('Сеанс завершён.')
        ])
