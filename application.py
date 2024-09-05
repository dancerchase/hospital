class Application:
    """Класс использует в себе классы UserInputCommands, UserOutputCommands и ActionsForCommands. Содержит
    в себе логику обработки команд пользователя и отвечает за запуск программы"""

    def __init__(self, user_input_commands, user_output_commands, actions_for_commands):
        self._user_input_commands = user_input_commands
        self._user_output_commands = user_output_commands
        self._actions_for_commands = actions_for_commands
        self._is_command_not_stop = True

    def _performing_an_action_based_on_a_command(self, command_type: str):

        if command_type == 'get_status':
            self._actions_for_commands.print_patient_status()

        elif command_type == 'up_status':
            self._actions_for_commands.up_patient_status()

        elif command_type == 'down_status':
            self._actions_for_commands.down_patient_status()

        elif command_type == 'discharge':
            self._actions_for_commands.discharge_patient()

        elif command_type == 'calculate_statistics':
            self._actions_for_commands.print_hospital_statistic()

        elif command_type == 'stop':
            self._is_command_not_stop = False
            self._user_output_commands.print_application_stop()

        else:
            self._user_output_commands.print_command_not_exist_error()

    def run_application(self):
        while self._is_command_not_stop:
            command_type = self._user_input_commands.get_command_type()
            self._performing_an_action_based_on_a_command(command_type)
