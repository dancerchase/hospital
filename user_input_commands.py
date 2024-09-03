from errors import IDNotIntOrNegativeError, IDNotExistError
from user_output_commands import UserOutputCommands
from hospital import Hospital


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    @staticmethod
    def get_input_command_from_user() -> str:
        """Получает команду от пользователя"""
        return input('Введите команду: '.lower())

    @staticmethod
    def get_patient_id_from_user() -> str:
        """Получает ID пациента от пользователя"""
        return input('Введите ID пациента: ')

    @staticmethod
    def hospital_discharge_offer() -> str:
        return input('Желаете этого клиента выписать? (да/нет): '.lower())

    def get_patient_id(self) -> int:
        """Возвращает ID пациента"""
        patient_id_str = self.get_patient_id_from_user()
        patient_id_int = self._patient_id_from_str_to_int(patient_id_str)
        return patient_id_int

    def _patient_id_from_str_to_int(self, patient_id: str) -> int:
        """Получает ID пациента и преобразует его в положительный целочисленный тип"""
        try:
            patient_id_int = int(patient_id)

            if patient_id_int <= 0:
                raise IDNotIntOrNegativeError
            return patient_id_int

        except ValueError:
            raise IDNotIntOrNegativeError
