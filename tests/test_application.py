from unittest.mock import MagicMock, call
from hospital import Hospital
from actions_for_commands import ActionsForCommands
from input_output.input_output_manager import InputOutputManager
from application import Application
from input_output.mock_console import MockConsole


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
            call.print('Статус пациента: "Болен"'),
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.print('Новый статус пациента: "Слегка болен"'),
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.print('Новый статус пациента: "Тяжело болен"'),
            call.input('Введите команду: '),
            call.input('Введите ID пациента: '),
            call.print('Пациент выписан из больницы'),
            call.input('Введите команду: '),
            call.print('В больнице на данный момент находится 4 чел., из них:' +
                       '\n    - в статусе "Болен": 2 чел.' +
                       '\n    - в статусе "Слегка болен": 1 чел.' +
                       '\n    - в статусе "Тяжело болен": 1 чел.'),
            call.input('Введите команду: '),
            call.print('Сеанс завершён.')
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
            call.print('Неизвестная команда! Попробуйте ещё раз'),
            call.input('Введите команду: '),
            call.print('Сеанс завершён.')
        ])

    def test_ordinary_positive_scenario(self):
        hospital = Hospital([1, 1, 0, 2, 1])
        console = MockConsole()
        actions_for_commands = ActionsForCommands(InputOutputManager(console), hospital)
        application = Application(InputOutputManager(console), actions_for_commands)

        console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '1')
        console.add_expected_output_message('Статус пациента: "Болен"')

        console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '1')
        console.add_expected_output_message('Новый статус пациента: "Слегка болен"')

        console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
        console.add_expected_request_and_response('Введите ID пациента: ', '2')
        console.add_expected_output_message('Новый статус пациента: "Тяжело болен"')

        console.add_expected_request_and_response('Введите команду: ', 'рассчитать статистику')
        console.add_expected_output_message('В больнице на данный момент находится 5 чел., из них:' +
                                            '\n    - в статусе "Слегка болен": 2 чел.' +
                                            '\n    - в статусе "Тяжело болен": 2 чел.' +
                                            '\n    - в статусе "Болен": 1 чел.')

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        application.run_application()

        console.verify_all_calls_have_been_made()
        assert hospital._patients == [2, 0, 0, 2, 1]

    def test_unknown_command(self):
        hospital = Hospital([1, 1, 0, 2, 1])
        console = MockConsole()
        actions_for_commands = ActionsForCommands(InputOutputManager(console), hospital)
        application = Application(InputOutputManager(console), actions_for_commands)

        console.add_expected_request_and_response('Введите команду: ', 'сделай что-нибудь...')
        console.add_expected_output_message('Неизвестная команда! Попробуйте ещё раз')

        console.add_expected_request_and_response('Введите команду: ', 'стоп')
        console.add_expected_output_message('Сеанс завершён.')

        application.run_application()

        console.verify_all_calls_have_been_made()


def test_boundary_cases():
    hospital = Hospital([0, 3, 3, 1])
    console = MockConsole()
    actions_for_commands = ActionsForCommands(InputOutputManager(console), hospital)
    application = Application(InputOutputManager(console), actions_for_commands)

    console.add_expected_request_and_response('Введите команду: ', 'понизить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '1')
    console.add_expected_output_message('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'да')
    console.add_expected_output_message('Пациент выписан из больницы')

    console.add_expected_request_and_response('Введите команду: ', 'повысить статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    console.add_expected_request_and_response('Желаете этого клиента выписать? (да/нет): ', 'нет')
    console.add_expected_output_message('Пациент остался в статусе "Готов к выписке"')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    application.run_application()

    console.verify_all_calls_have_been_made()
    assert hospital._patients == [0, None, 3, 1]


def test_cases_of_invalid_data_entry():
    hospital = Hospital([1, 1])
    console = MockConsole()
    actions_for_commands = ActionsForCommands(InputOutputManager(console), hospital)
    application = Application(InputOutputManager(console), actions_for_commands)

    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', 'два')
    console.add_expected_output_message('Ошибка. ID пациента должно быть числом (целым, положительным)')

    console.add_expected_request_and_response('Введите команду: ', 'узнать статус пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '3')
    console.add_expected_output_message('Ошибка. В больнице нет пациента с таким ID')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    application.run_application()

    console.verify_all_calls_have_been_made()


def test_discharge_patient():
    hospital = Hospital([1, 3, 1])
    console = MockConsole()
    actions_for_commands = ActionsForCommands(InputOutputManager(console), hospital)
    application = Application(InputOutputManager(console), actions_for_commands)

    console.add_expected_request_and_response('Введите команду: ', 'выписать пациента')
    console.add_expected_request_and_response('Введите ID пациента: ', '2')
    console.add_expected_output_message('Пациент выписан из больницы')

    console.add_expected_request_and_response('Введите команду: ', 'стоп')
    console.add_expected_output_message('Сеанс завершён.')

    application.run_application()

    console.verify_all_calls_have_been_made()
    assert hospital._patients == [1, None, 1]
