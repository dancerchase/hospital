class UserOutputCommands:
    """Класс для Вывода информации на экран пользователю"""

    @staticmethod
    def error_patient_id_not_int_or_negative():
        print('Ошибка. ID пациента должно быть числом (целым, положительным)')

    @staticmethod
    def error_patient_id_not_exist():
        print('Ошибка. В больнице нет пациента с таким ID')

    @staticmethod
    def not_approval_discharge():
        print('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')

    @staticmethod
    def error_command_not_exist():
        print('Неизвестная команда! Попробуйте ещё раз')

    @staticmethod
    def new_status(new_status: str):
        print(f'Новый статус пациента: "{new_status}"')

    @staticmethod
    def refusal_of_discharge():
        print('Пациент остался в статусе "Готов к выписке"')

    @staticmethod
    def discharge():
        print('Пациент выписан из больницы')

    @staticmethod
    def stop():
        print('Сеанс завершён.')

    @staticmethod
    def statistic_patients(statistic: dict[str, int]):
        print(f'В больнице на данный момент находится {statistic['Всего']} чел., из них:')
        for key, value in statistic.items():
            if key == 'Всего':
                continue
            elif value != 0:
                print(f'    - в статусе "{key}": {value} чел.')
