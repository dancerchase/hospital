from user_output_commands import UserOutputCommands
from user_input_commands import UserInputCommands
from actions_for_commands import ActionsForCommands


class Application:
    """Класс использует в себе классы UserInputCommands, UserOutputCommands и ActionsForCommands. Содержит
    в себе логику обработки команд пользователя и отвечает за запуск программы"""

    def __init__(self):
        self._user_input = UserInputCommands()
        self._user_output = UserOutputCommands()
        self._actions = ActionsForCommands()

    def _performing_an_action_based_on_a_command(self, command: str):
        """Выполняет действие в зависимости от команды"""

        if command in ['узнать статус пациента', 'get status']:
            self._actions.print_patient_status()

        elif command in ['повысить статус пациента', 'status up']:
            self._actions.up_status_for_patient()

        elif command in ['понизить статус пациента', 'status down']:
            self._actions.down_status_for_patient()

        elif command in ['выписать пациента', 'discharge']:
            self._actions.discharge_patient()

        elif command in ['рассчитать статистику', 'calculate statistics']:
            self._actions.print_hospital_statistic()

        else:
            UserOutputCommands.error_command_not_exist()

    def run_application(self):
        """Запуск программы"""
        while True:
            command = self._user_input.get_input_command_from_user()
            if command in ['стоп', 'stop']:
                self._user_output.stop()
                break
            self._performing_an_action_based_on_a_command(command)
