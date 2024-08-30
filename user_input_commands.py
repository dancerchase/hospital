from user_output_commands import UserOutputCommands
from errors import UserInputIDIntError, UserInputCommandError


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    def _patient_id_analysis(self, patient_id: str) -> int:
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

    def check_command_in_list_available(self, command: str):
        """Проверяет правильность ввода команды"""
        if command not in (
                'узнать статус пациента', 'get status', 'повысить статус пациента', 'status up',
                'понизить статус пациента', 'status down', 'выписать пациента', 'discharge', 'рассчитать статистику',
                'calculate statistics', 'стоп', 'stop'):
            raise UserInputCommandError

    def get_input_command(self) -> str:
        """Получает команду от пользователя"""
        return input('Введите команду: ')

    def get_patient_id(self) -> str:
        """Получает ID пациента от пользователя"""
        return input('Введите ID пациента: ')

    def offer_extract(self) -> str:
        answer = input('Желаете этого клиента выписать? (да/нет): ')
        return answer
