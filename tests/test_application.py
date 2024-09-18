import pytest
from unittest.mock import MagicMock, call
from hospital import Hospital
from actions_for_commands import ActionsForCommands
from input_output.input_output_manager import InputOutputManager
from application import Application


class TestApplication:

    def test_first_base_scenario(self):
        console = MagicMock()
        input_output_manager = InputOutputManager(console)
        hospital = Hospital([1, 1, 1, 1, 1])
        actions_for_commands = ActionsForCommands(input_output_manager, hospital)
        application = Application(input_output_manager, actions_for_commands)
        console.input.side_effect = [
            'узнать статус пациента',
            '5',
            'status up',
            '2',
            'status down',
            '3',
            'discharge',
            '4',
            'рассчитать статистику',
            'стоп']

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
            call.output('В больнице на данный момент находится 4 чел., из них:'),
            call.output('    - в статусе "Болен": 2 чел.'),
            call.output('    - в статусе "Слегка болен": 1 чел.'),
            call.output('    - в статусе "Тяжело болен": 1 чел.'),
            call.input('Введите команду: '),
            call.output('Сеанс завершён.')
        ])

        assert hospital._patients == [1, 2, 0, None, 1]

    def test_invalid_command(self):
        console = MagicMock()
        input_output_manager = InputOutputManager(console)
        hospital = Hospital()
        actions_for_commands = ActionsForCommands(input_output_manager, hospital)
        application = Application(input_output_manager, actions_for_commands)
        console.input.side_effect = [
            'выписать всех пациентов',
            'стоп']

        application.run_application()

        console.assert_has_calls([
            call.input('Введите команду: '),
            call.output('Неизвестная команда! Попробуйте ещё раз'),
            call.input('Введите команду: '),
            call.output('Сеанс завершён.')
        ])
