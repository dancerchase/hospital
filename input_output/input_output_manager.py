from errors import PatientIDNotIntOrNegativeError


class InputOutputManager:
    """Объединяет методы для получения ввода от пользователя и вывода информации на экран."""

    def __init__(self, console):
        self._console = console

    def request_for_discharge(self) -> bool:
        return self._console.input('Желаете этого клиента выписать? (да/нет): ') == 'да'

    def get_patient_id(self) -> int:
        patient_id_as_str = self._console.input('Введите ID пациента: ')
        patient_id = self._convert_patient_id_from_str_to_positive_int(patient_id_as_str)
        return patient_id

    @staticmethod
    def _convert_patient_id_from_str_to_positive_int(patient_id: str) -> int:
        if not patient_id.isdigit() or int(patient_id) <= 0:
            raise PatientIDNotIntOrNegativeError
        return int(patient_id)

    def get_command_from_user(self) -> str:
        return self._console.input('Введите команду: ')

    def send_message_command_not_exist_error(self):
        self._console.output('Неизвестная команда! Попробуйте ещё раз')

    def send_message_new_status(self, new_status: str):
        self._console.output(f'Новый статус пациента: "{new_status}"')

    def send_message_out_refusal_of_discharge(self):
        self._console.output('Пациент остался в статусе "Готов к выписке"')

    def send_message_patient_discharge(self):
        self._console.output('Пациент выписан из больницы')

    def send_message_application_stop(self):
        self._console.output('Сеанс завершён.')

    def send_message_hospital_statistics_text(self, statistics: dict[str, int], total_patients: int):
        self._console.output(f'В больнице на данный момент находится {total_patients} чел., из них:')
        for key, value in statistics.items():
            if value != 0:
                self._console.output(f'    - в статусе "{key}": {value} чел.')

    def send_message_patient_status(self, patient_status: str):
        self._console.output(f'Статус пациента: "{patient_status}"')

    def send_message_with_received_text(self, text: str):
        self._console.output(text)
