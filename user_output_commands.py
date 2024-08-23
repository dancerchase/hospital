class UserOutputCommands:
    """Класс для Вывода информации на экран пользователю"""

    @staticmethod
    def error_patient_id_not_int_or_negative():
        print('Ошибка. ID пациента должно быть числом (целым, положительным)')

    @staticmethod
    def error_patient_id_not_exist():
        print('Ошибка. В больнице нет пациента с таким ID')

    @staticmethod
    def error_command_not_exist():
        print('Команда не распознана. Попробуйте ещё раз')

    def up_status(self, new_status: str):
        print(f'Новый статус пациента: "{new_status}"')

    def refusal_of_discharge(self):
        print('Пациент остался в статусе "Готов к выписке"')

    def patient_extraction(self):
        print('Пациент выписан из больницы')

    def not_approval_discharge(self):
        print('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    def print_statistic_patients(self, statistic: dict[str, int]):
        print(f'В больнице на данный момент находится {statistic['Всего']} чел., из них:')
        for key, value in statistic.items():
            if key == 'Всего':
                continue
            elif value != 0:
                print(f'    - в статусе "{key}": {value} чел.')