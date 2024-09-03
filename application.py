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

    def _performing_an_action_based_on_a_command(self, command_type: str):
        """Выполняет действие в зависимости от команды"""

        if command_type == 'get_status':
            self._actions.print_patient_status()

        elif command_type == 'up_status':
            self._actions.up_status_for_patient()

        elif command_type == 'down_status':
            self._actions.down_status_for_patient()

        elif command_type == 'discharge':
            self._actions.discharge_patient()

        elif command_type == 'calculate_statistics':
            self._actions.print_hospital_statistic()

        else:
            UserOutputCommands.error_command_not_exist()

    def run_application(self):
        """Запуск программы"""
        while True:
            #TODO можно ли возбудить исключение, когда приходит команда на стоп, а в этом методе отлавливать
            # исключение и брейкать цикл, или в этом нет смысла?
            command_type = self._user_input.get_command_type()
            if command_type == 'stop':
                self._user_output.stop()
                break
            self._performing_an_action_based_on_a_command(command_type)
