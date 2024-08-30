from user_output_commands import UserOutputCommands
from errors import UserInputIDIntError, UserInputCommandError


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    @staticmethod
    def get_input_command() -> str:
        """Получает команду от пользователя"""
        return input('Введите команду: ')

    @staticmethod
    def get_patient_id() -> str:
        """Получает ID пациента от пользователя"""
        return input('Введите ID пациента: ')

    @staticmethod
    def offer_extract() -> str:
        answer = input('Желаете этого клиента выписать? (да/нет): ')
        return answer
