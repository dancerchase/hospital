from errors import IDNotExistError, MaxStatusError, MinStatusError, IDNotIntOrNegativeError
from hospital import Hospital
from user_input_commands import UserInputCommands
from user_output_commands import UserOutputCommands


class ActionsForCommands:
    """Класс содержащий методы для действий в зависимости от команды"""

    def __init__(self):
        self._hospital = Hospital()
        self._user_input = UserInputCommands()
        self._user_output = UserOutputCommands()

    def print_patient_status(self):
        """Печать статуса пациента"""
        try:
            patient_id = self._user_input.get_patient_id()
            self._hospital.check_patient_id_exist(patient_id)
            patient_status = self._hospital.get_patient_status_text(patient_id)
            self._user_output.print_patient_status(patient_status)

        except IDNotIntOrNegativeError:
            UserOutputCommands.error_patient_id_not_int_or_negative()

        except IDNotExistError:
            UserOutputCommands.error_patient_id_not_exist()

    def up_status_for_patient(self):
        """Повышение статуса пациента"""
        try:
            patient_id = self._user_input.get_patient_id()
            self._hospital.check_patient_id_exist(patient_id)
            self._hospital.up_status_for_patient(patient_id)
            new_status = self._hospital.get_patient_status_text(patient_id)
            self._user_output.new_status(new_status)

        except MaxStatusError:
            if self._user_input.hospital_discharge_offer() == 'да':
                self._hospital.patient_discharge(patient_id)
                self._user_output.discharge()
            else:
                self._user_output.refusal_of_discharge()

        except IDNotIntOrNegativeError:
            UserOutputCommands.error_patient_id_not_int_or_negative()

        except IDNotExistError:
            UserOutputCommands.error_patient_id_not_exist()

    def down_status_for_patient(self):
        """Понижение статуса пациента"""
        try:
            patient_id = self._user_input.get_patient_id()
            self._hospital.check_patient_id_exist(patient_id)
            self._hospital.down_status_for_patient(patient_id)
            new_status = self._hospital.get_patient_status_text(patient_id)
            self._user_output.new_status(new_status)

        except MinStatusError:
            self._user_output.not_approval_discharge()

        except IDNotIntOrNegativeError:
            UserOutputCommands.error_patient_id_not_int_or_negative()

        except IDNotExistError:
            UserOutputCommands.error_patient_id_not_exist()

    def discharge_patient(self):
        """Выписка пациента"""
        try:
            patient_id = self._user_input.get_patient_id()
            self._hospital.check_patient_id_exist(patient_id)
            self._hospital.patient_discharge(patient_id)
            self._user_output.discharge()

        except IDNotIntOrNegativeError:
            UserOutputCommands.error_patient_id_not_int_or_negative()

        except IDNotExistError:
            UserOutputCommands.error_patient_id_not_exist()

    def print_hospital_statistic(self):
        """Печать статистики больницы"""
        statistic = self._hospital.get_statistic_patients()
        self._user_output.statistic_patients(statistic)
