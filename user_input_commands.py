from errors import IDNotIntOrNegativeError, IDNotExistError
from user_output_commands import UserOutputCommands
from hospital import Hospital


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    def __init__(self):
        self._hospital = Hospital()

    @staticmethod
    def get_input_command_from_user() -> str:
        """Получает команду от пользователя"""
        return input('Введите команду: ')

    @staticmethod
    def get_patient_id_from_user() -> str:
        """Получает ID пациента от пользователя"""
        return input('Введите ID пациента: ')

    @staticmethod
    def hospital_discharge_offer() -> str:
        return input('Желаете этого клиента выписать? (да/нет): ')

    def get_patient_id(self) -> int:
        """Возвращает валидный ID пациента"""
        try:
            patient_id = self.get_patient_id_from_user()
            patient_id = self._is_valid_user_id(patient_id)
            return patient_id

        except IDNotIntOrNegativeError:
            UserOutputCommands.error_patient_id_not_int_or_negative()

        except IDNotExistError:
            UserOutputCommands.error_patient_id_not_exist()

    def _is_patient_id_positive(self, patient_id: int) -> bool:
        """Проверяет правильность ввода ID пациента на целое положительное число"""
        return patient_id > 0

    def _is_patient_id_int(self, patient_id: str):
        """Проверяет правильность ввода ID пациента на целое число"""
        try:
            return int(patient_id)
        except ValueError:
            raise IDNotIntOrNegativeError

    def _is_valid_user_id(self, patient_id: str):
        """Получает ID пациента и проверяет его на правильность, если ID не валидный выводит ошибку"""

        if not self._is_patient_id_int(patient_id):
            raise IDNotIntOrNegativeError
        patient_id = int(patient_id)

        if not self._is_patient_id_positive(patient_id):
            raise IDNotIntOrNegativeError

        if not self._hospital.is_patient_id_exist(patient_id):
            raise IDNotExistError

        return patient_id
