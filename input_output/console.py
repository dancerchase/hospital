class Console:

    @staticmethod
    def request_for_discharge() -> str:
        return input('Желаете этого клиента выписать? (да/нет): ').lower()

    @staticmethod
    def get_patient_id() -> str:
        return input('Введите ID пациента: ')

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
