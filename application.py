class Application:
    """Обрабатывает команд пользователя и отвечает за запуск программы"""

    def __init__(self, input_output_manager, actions_for_commands):
        self._input_output_manager = input_output_manager
        self._actions_for_commands = actions_for_commands
        self._is_command_not_stop = True

    def _performing_an_action_based_on_a_command(self, command: str):

        if command in ['узнать статус пациента', 'get status']:
            self._actions_for_commands.get_patient_status()

        elif command in ['повысить статус пациента', 'status up']:
            self._actions_for_commands.up_patient_status()

        elif command in ['понизить статус пациента', 'status down']:
            self._actions_for_commands.down_patient_status()

        elif command in ['выписать пациента', 'discharge']:
            self._actions_for_commands.discharge_patient()

        elif command in ['рассчитать статистику', 'calculate statistics']:
            self._actions_for_commands.get_hospital_statistics()

        elif command in ['стоп', 'stop']:
            self._is_command_not_stop = False
            self._input_output_manager.send_message_application_stop()

        else:
            self._input_output_manager.send_message_command_not_exist_error()

    def run_application(self):
        while self._is_command_not_stop:
            command = self._input_output_manager.get_command_from_user()
            self._performing_an_action_based_on_a_command(command)
