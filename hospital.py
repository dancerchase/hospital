from patient_data import PatientData
from user_output_commands import UserOutputCommands
from user_input_commands import UserInputCommands
from actions_for_commands import ActionsForCommands
from errors import InputCommandError, IDNotIntOrNegativeError, IDNotExistError


class Hospital:
    """Класс использует в себе классы PatientData, UserInputCommands, UserOutputCommands и ActionsForCommands. Содержит
    в себе логику обработки команд пользователя и отвечает за запуск программы"""

    def __init__(self):
        self._patient_data = PatientData()
        self._user_input = UserInputCommands()
        self._user_output = UserOutputCommands()
        self._actions = ActionsForCommands()

    def _performing_an_action_based_on_a_command(self, command: str):
        """Выполняет действие в зависимости от команды"""

        if command in ['узнать статус пациента', 'get status']:
            patient_id = self._get_user_id_and_checking()
            self._actions.print_patient_status(patient_id)

        elif command in ['повысить статус пациента', 'status up']:
            patient_id = self._get_user_id_and_checking()
            self._actions.up_status_for_patient(patient_id)

        elif command in ['понизить статус пациента', 'status down']:
            patient_id = self._get_user_id_and_checking()
            self._actions.down_status_for_patient(patient_id)

        elif command in ['выписать пациента', 'discharge']:
            patient_id = self._get_user_id_and_checking()
            self._actions.discharge_patient(patient_id)

        elif command in ['рассчитать статистику', 'calculate statistics']:
            self._actions.print_hospital_statistic()

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
