from errors import PatientIDNotIntOrNegativeError


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    @staticmethod
    def request_for_discharge() -> bool:
        return input('Желаете этого клиента выписать? (да/нет): ').lower() == 'да'

    def get_patient_id(self) -> int:
        patient_id_str = input('Введите ID пациента: ')
        patient_id = self._convert_patient_id_from_str_to_positive_int(patient_id_str)
        return patient_id

    @staticmethod
    def _convert_patient_id_from_str_to_positive_int(patient_id: str) -> int:
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise PatientIDNotIntOrNegativeError
        return int(patient_id)

    @staticmethod
    def get_command_type() -> str:
        """Возвращает тип команды"""
        command = input('Введите команду: ').lower()
        command_type = {('узнать статус пациента', 'get status'): 'get_status',
                        ('повысить статус пациента', 'status up'): 'up_status',
                        ('понизить статус пациента', 'status down'): 'down_status',
                        ('выписать пациента', 'discharge'): 'discharge',
                        ('рассчитать статистику', 'calculate statistics'): 'calculate_statistics',
                        ('стоп', 'stop'): 'stop'}

        for k, v in command_type.items():
            if command in k:
                return v
        return 'unknown_command'
