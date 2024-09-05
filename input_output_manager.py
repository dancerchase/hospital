from errors import PatientIDNotIntOrNegativeError


class InputOutputManager:
    """Объединяет методы для получения ввода от пользователя и вывода информации на экран."""

    @staticmethod
    def request_for_discharge() -> bool:
        return input('Желаете этого клиента выписать? (да/нет): ').lower() == 'да'

    def get_patient_id(self) -> int:
        patient_id_as_str = input('Введите ID пациента: ')
        patient_id = self._convert_patient_id_from_str_to_positive_int(patient_id_as_str)
        return patient_id

    @staticmethod
    def _convert_patient_id_from_str_to_positive_int(patient_id: str) -> int:
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise PatientIDNotIntOrNegativeError
        return int(patient_id)

    @staticmethod
    def get_command_from_user() -> str:
        return input('Введите команду: ').lower()

    @staticmethod
    def send_message_command_not_exist_error():
        print('Неизвестная команда! Попробуйте ещё раз')

    @staticmethod
    def send_message_new_status(new_status: str):
        print(f'Новый статус пациента: "{new_status}"')

    @staticmethod
    def send_message_out_refusal_of_discharge():
        print('Пациент остался в статусе "Готов к выписке"')

    @staticmethod
    def send_message_patient_discharge():
        print('Пациент выписан из больницы')

    @staticmethod
    def send_message_application_stop():
        print('Сеанс завершён.')

    @staticmethod
    def send_message_hospital_statistics_text(statistic: dict[str, int], total_patients: int):
        print(f'В больнице на данный момент находится {total_patients} чел., из них:')
        for key, value in statistic.items():
            if value != 0:
                print(f'    - в статусе "{key}": {value} чел.')

    @staticmethod
    def send_message_patient_status_text(patient_status: str):
        print(f'Статус пациента: "{patient_status}"')

    @staticmethod
    def send_message_with_received_text(text: str):
        print(text)
