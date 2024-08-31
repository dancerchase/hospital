from errors import IDNotExistError, MaxStatusError, MinStatusError
from patient_data import PatientData
from user_input_commands import UserInputCommands
from user_output_commands import UserOutputCommands


class ActionsForCommands:
    """Класс содержащий методы для действий в зависимости от команды"""

    def __init__(self):
        self._patient_data = PatientData()
        self._user_input = UserInputCommands()
        self._user_output = UserOutputCommands()

    def print_patient_status(self, patient_id: int):
        """Печать статуса пациента"""
        try:
            print(f'Статус пациента: "{self._patient_data.get_patient_status_text(patient_id)}"')
        except IDNotExistError:
            self._user_output.error_patient_id_not_exist()

        except TypeError:
            pass

    def up_status_for_patient(self, patient_id: int):
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

    def down_status_for_patient(self, patient_id: int):
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

    def discharge_patient(self, patient_id: int):
        """Выписка пациента"""
        try:
            self._patient_data.patient_discharge(patient_id)
            self._user_output.discharge()
        except IDNotExistError:
            self._user_output.error_patient_id_not_exist()

        except TypeError:
            pass

    def print_hospital_statistic(self):
        """Печать статистики больницы"""
        statistic = self._patient_data.get_statistic_patients()
        self._user_output.statistic_patients(statistic)
