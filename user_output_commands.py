class UserOutputCommands:
    """Класс для Вывода информации на экран пользователю"""

    @staticmethod
    def print_command_not_exist_error():
        print('Неизвестная команда! Попробуйте ещё раз')

    @staticmethod
    def print_new_status(new_status: str):
        print(f'Новый статус пациента: "{new_status}"')

    @staticmethod
    def print_out_refusal_of_discharge():
        print('Пациент остался в статусе "Готов к выписке"')

    @staticmethod
    def print_patient_discharge():
        print('Пациент выписан из больницы')

    @staticmethod
    def print_application_stop():
        print('Сеанс завершён.')

    @staticmethod
    def print_hospital_statistics(statistic: dict[str, int], total_patients: int):
        print(f'В больнице на данный момент находится {total_patients} чел., из них:')
        for key, value in statistic.items():
            if value != 0:
                print(f'    - в статусе "{key}": {value} чел.')

    @staticmethod
    def print_patient_status(patient_status: str):
        print(f'Статус пациента: "{patient_status}"')

    @staticmethod
    def print_received_text(text: str):
        print(text)
