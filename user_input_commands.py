from user_output_commands import UserOutputCommands


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    def _patient_id_analysis(self, patient_id: str) -> int | bool:
        """Проверяет правильность ввода ID пациента"""
        try:
            patient_id = int(patient_id)

        except ValueError:
            UserOutputCommands.error_patient_id_not_int_or_negative()
            return False

        if patient_id < 0:
            UserOutputCommands.error_patient_id_not_int_or_negative()
            return False
        elif 0 >= patient_id or patient_id > 200:
            UserOutputCommands.error_patient_id_not_exist()
            return False
        else:
            return patient_id

    def _user_input_command_analysis(self, command: str) -> bool:
        """Проверяет правильность ввода команды"""
        if command not in (
                'узнать статус пациента', 'get status', 'повысить статус пациента', 'status up',
                'понизить статус пациента', 'status down', 'выписать пациента', 'discharge', 'рассчитать статистику',
                'calculate statistics', 'стоп', 'stop'):
            UserOutputCommands.error_command_not_exist()
            return False
        return True

    def get_input_command(self) -> bool | str:
        """Получает команду от пользователя"""
        command = input('Введите команду: ')
        if self._user_input_command_analysis(command) is False:
            return False
        return command

    def get_patient_id(self) -> int | bool:
        """Получает ID пациента от пользователя"""
        patient_id = input('Введите ID пациента: ')
        if self._patient_id_analysis(patient_id) is False:
            return False
        return int(patient_id)

    def offer_extract(self) -> str:
        answer = input('Желаете этого клиента выписать? (да/нет): ')
        return answer
