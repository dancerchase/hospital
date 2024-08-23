class PatientData:
    """Класс для взаимодействия со списком пациентов"""

    def __init__(self):
        self._patients = [1 for _ in range(200)]
        self._status = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    def _transformation_id(self, input_id: str | int) -> int:
        """Преобразование id пациента в индекс в списке пациентов"""
        return int(input_id) - 1

    def get_patient_status_text(self, patient_id: int) -> str | bool:
        """Возвращает текстовое представление статуса пациента"""
        patient_status_for_number_in_list = self._status[self.get_patient_status_number(patient_id)]
        return patient_status_for_number_in_list

    def get_patient_status_number(self, patient_id: int) -> int:
        """Возвращает статус пациента числовым значением из списка пациентов"""
        patient_index = self._transformation_id(patient_id)
        patient_status_in_list = self._patients[patient_index]
        if patient_status_in_list is None:
            return False
        return patient_status_in_list

    def up_status_for_patient(self, patient_id: int):
        """Увеличивает статус пациента на единицу"""
        patient_index = self._transformation_id(patient_id)
        self._patients[patient_index] += 1

    def down_status_for_patient(self, patient_id: int):
        """Уменьшает статус пациента на единицу"""
        patient_index = self._transformation_id(patient_id)
        self._patients[patient_index] -= 1

    def extract(self, patient_id: int):
        """Выписывает пациента из больницы"""
        patient_index = self._transformation_id(patient_id)
        self._patients[patient_index] = None

    def get_statistic_patients(self) -> dict[str, int]:
        """Возвращает статистику по пациентам"""
        patient_statistic = {'Всего': 0, 'Болен': 0, 'Слегка болен': 0, 'Тяжело болен': 0, 'Готов к выписке': 0}
        for i in self._patients:
            if i == 0:
                patient_statistic['Тяжело болен'] += 1
                patient_statistic['Всего'] += 1
            elif i == 1:
                patient_statistic['Болен'] += 1
                patient_statistic['Всего'] += 1
            elif i == 2:
                patient_statistic['Слегка болен'] += 1
                patient_statistic['Всего'] += 1
            elif i == 3:
                patient_statistic['Готов к выписке'] += 1
                patient_statistic['Всего'] += 1
        return patient_statistic


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


class UserInputCommands:
    """Класс для работы с командами которые вводит пользователь"""

    def _patient_id_analysis(self, patient_id: str) -> int | bool:
        """Проверяет правильность ввода ID пациента"""
        try:
            patient_id = int(patient_id)

        except ValueError:
            UserOutputCommands.error_patient_id_not_int_or_negative()
            return False

        if patient_id < 0:
            UserOutputCommands.error_patient_id_not_int_or_negative()
            return False
        elif 0 >= patient_id or patient_id > 200:
            UserOutputCommands.error_patient_id_not_exist()
            return False
        else:
            return patient_id

    def _user_input_command_analysis(self, command: str) -> bool:
        """Проверяет правильность ввода команды"""
        if command not in (
                'узнать статус пациента', 'get status', 'повысить статус пациента', 'status up',
                'понизить статус пациента', 'status down', 'выписать пациента', 'discharge', 'рассчитать статистику',
                'calculate statistics', 'стоп', 'stop'):
            UserOutputCommands.error_command_not_exist()
            return False
        return True

    def get_input_command(self) -> bool | str:
        """Получает команду от пользователя"""
        command = input('Введите команду: ')
        if self._user_input_command_analysis(command) is False:
            return False
        return command

    def get_patient_id(self) -> int | bool:
        """Получает ID пациента от пользователя"""
        patient_id = input('Введите ID пациента: ')
        if self._patient_id_analysis(patient_id) is False:
            return False
        return int(patient_id)

    def offer_extract(self) -> str:
        answer = input('Желаете этого клиента выписать? (да/нет): ')
        return answer


class Hospital:
    def __init__(self):
        self.hospital = PatientData()
        self.user_input = UserInputCommands()
        self.user_output = UserOutputCommands()

    def action_with_command(self, command: str, patient_id: int | None):
        if command in ['узнать статус пациента', 'get status']:
            status = self.hospital.get_patient_status_number(patient_id)
            if status is False:
                self.user_output.error_patient_id_not_exist()
            else:
                print(f'Статус пациента: "{self.hospital.get_patient_status_text(patient_id)}"')

        elif command in ['повысить статус пациента', 'status up']:
            status = self.hospital.get_patient_status_number(patient_id)
            if status is False:
                self.user_output.error_patient_id_not_exist()
            else:
                if self.hospital.get_patient_status_number(patient_id) == 3:
                    if self.user_input.offer_extract() == 'да':
                        self.hospital.extract(patient_id)
                        self.user_output.patient_extraction()
                    else:
                        self.user_output.refusal_of_discharge()

                else:
                    self.hospital.up_status_for_patient(patient_id)
                    new_status = self.hospital.get_patient_status_text(patient_id)
                    self.user_output.up_status(new_status)

        elif command in ['понизить статус пациента', 'status down']:
            status = self.hospital.get_patient_status_number(patient_id)
            if status is False:
                self.user_output.error_patient_id_not_exist()
            else:
                if self.hospital.get_patient_status_number(patient_id) == 0:
                    self.user_output.not_approval_discharge()

                else:
                    self.hospital.down_status_for_patient(patient_id)
                    new_status = self.hospital.get_patient_status_text(patient_id)
                    self.user_output.up_status(new_status)

        elif command in ['выписать пациента', 'discharge']:
            status = self.hospital.get_patient_status_number(patient_id)
            if status is False:
                self.user_output.error_patient_id_not_exist()
            else:
                self.hospital.extract(patient_id)
                self.user_output.patient_extraction()

        elif command in ['рассчитать статистику', 'calculate statistics']:
            statistic = self.hospital.get_statistic_patients()
            self.user_output.print_statistic_patients(statistic)

    def run_hospital(self):
        while True:

            command = self.user_input.get_input_command()
            if command is False:
                continue
            elif command in ['стоп', 'stop']:
                print('Сеанс завершён.')
                break
            elif command in ['рассчитать статистику', 'calculate statistics']:
                self.action_with_command(command, patient_id=None)
                continue

            patient_id = self.user_input.get_patient_id()
            if patient_id is False:
                continue

            else:
                self.action_with_command(command, patient_id)


hospital = Hospital()
hospital.run_hospital()
