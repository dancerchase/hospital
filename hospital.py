from patient_data import PatientData
from user_output_commands import UserOutputCommands
from user_input_commands import UserInputCommands
from errors import InputCommandError, IDNotIntOrNegativeError, IDNotExistError, MinStatusError, MaxStatusError


class Hospital:
    """Класс использует в себе классы PatientData, UserInputCommands и UserOutputCommands. Содержит в себе логику
    обработки команд пользователя и отвечает за запуск программы"""

    def __init__(self):
        self._patient_data = PatientData()
        self._user_input = UserInputCommands()
        self._user_output = UserOutputCommands()

    def _performing_an_action_based_on_a_command(self, command: str):
        """Выполняет действие в зависимости от команды"""

        if command in ['узнать статус пациента', 'get status']:
            patient_id = self._get_user_id_and_checking()
            self._print_patient_status(patient_id)

        elif command in ['повысить статус пациента', 'status up']:
            patient_id = self._get_user_id_and_checking()
            self._up_status_for_patient(patient_id)

        elif command in ['понизить статус пациента', 'status down']:
            patient_id = self._get_user_id_and_checking()
            self._down_status_for_patient(patient_id)

        elif command in ['выписать пациента', 'discharge']:
            patient_id = self._get_user_id_and_checking()
            self._discharge_patient(patient_id)

        elif command in ['рассчитать статистику', 'calculate statistics']:
            self._print_hospital_statistic()

    def _print_patient_status(self, patient_id: int):
        """Печать статуса пациента"""
        try:
            print(f'Статус пациента: "{self._patient_data.get_patient_status_text(patient_id)}"')
        except IDNotExistError:
            self._user_output.error_patient_id_not_exist()

        except TypeError:
            pass

    def _up_status_for_patient(self, patient_id: int):
        """Повышение статуса пациента"""
        try:
            self._patient_data.up_status_for_patient(patient_id)
            new_status = self._patient_data.get_patient_status_text(patient_id)
            self._user_output.new_status(new_status)

        except IDNotExistError:
            self._user_output.error_patient_id_not_exist()

        except MaxStatusError:
            if self._user_input.hospital_discharge_offer() == 'да':
                self._patient_data.patient_discharge(patient_id)
                self._user_output.discharge()
            else:
                self._user_output.refusal_of_discharge()

        except TypeError:
            pass

    def _down_status_for_patient(self, patient_id: int):
        """Понижение статуса пациента"""
        try:
            self._patient_data.down_status_for_patient(patient_id)
            new_status = self._patient_data.get_patient_status_text(patient_id)
            self._user_output.new_status(new_status)

        except IDNotExistError:
            self._user_output.error_patient_id_not_exist()

        except MinStatusError:
            self._user_output.not_approval_discharge()

        except TypeError:
            pass

    def _discharge_patient(self, patient_id: int):
        """Выписка пациента"""
        try:
            self._patient_data.patient_discharge(patient_id)
            self._user_output.discharge()
        except IDNotExistError:
            self._user_output.error_patient_id_not_exist()

        except TypeError:
            pass

    def _print_hospital_statistic(self):
        """Печать статистики больницы"""
        statistic = self._patient_data.get_statistic_patients()
        self._user_output.statistic_patients(statistic)

    def _check_command_in_list_available(self, command: str):
        """Проверяет правильность ввода команды"""
        if command not in (
                'узнать статус пациента', 'get status', 'повысить статус пациента', 'status up',
                'понизить статус пациента', 'status down', 'выписать пациента', 'discharge', 'рассчитать статистику',
                'calculate statistics', 'стоп', 'stop'):
            raise InputCommandError

    def _get_user_command_and_checking(self):
        """Получает команду пользователя и проверяет ее на правильность, если команда не валидная выводит ошибку"""
        command = self._user_input.get_input_command()
        try:
            self._check_command_in_list_available(command)
            return command
        except InputCommandError:
            UserOutputCommands.error_command_not_exist()

    def _get_user_id_and_checking(self):
        """Получает ID пациента и проверяет его на правильность, если ID не валидный выводит ошибку"""
        patient_id = self._user_input.get_patient_id()
        try:
            patient_id = int(patient_id)
            self._patient_data.patient_id_positive_check(patient_id)
            self._patient_data.patient_id_exist_check(patient_id)
            return patient_id

        except (ValueError, IDNotIntOrNegativeError):
            UserOutputCommands.error_patient_id_not_int_or_negative()

        except IDNotExistError:
            UserOutputCommands.error_patient_id_not_exist()

    def run_hospital(self):
        """Запуск программы"""
        while True:
            command = self._get_user_command_and_checking()
            if command in ['стоп', 'stop']:
                self._user_output.stop()
                break
            self._performing_an_action_based_on_a_command(command)
