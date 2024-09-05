from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError, PatientIDNotIntOrNegativeError
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
        try:
            patient_id = self._user_input.get_patient_id()
            patient_status = self._hospital.get_patient_status_text(patient_id)
            self._user_output.print_patient_status(patient_status)

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError) as error:
            self._user_output.print_received_text(error)

    def up_patient_status(self):
        try:
            patient_id = self._user_input.get_patient_id()

            if self._hospital.is_possible_to_up_patient_status(patient_id):
                self._hospital.up_status_for_patient(patient_id)
                new_status = self._hospital.get_patient_status_text(patient_id)
                self._user_output.print_new_status(new_status)

            elif self._hospital.is_patient_status_already_max(patient_id):
                if self._user_input.request_for_discharge():
                    self._hospital.patient_discharge(patient_id)
                    self._user_output.print_patient_discharge()
                else:
                    self._user_output.print_out_refusal_of_discharge()

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError) as error:
            self._user_output.print_received_text(error)

    def down_patient_status(self):
        try:
            patient_id = self._user_input.get_patient_id()
            self._hospital.down_status_for_patient(patient_id)
            new_status = self._hospital.get_patient_status_text(patient_id)
            self._user_output.print_new_status(new_status)

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError, AttemptLowerMinimumStatusError) as error:
            self._user_output.print_received_text(error)

    def discharge_patient(self):
        try:
            patient_id = self._user_input.get_patient_id()
            self._hospital.patient_discharge(patient_id)
            self._user_output.print_patient_discharge()

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError) as error:
            self._user_output.print_received_text(error)

    def print_hospital_statistic(self):
        statistic = self._hospital.get_statistics_patients_statuses()
        total_patients = self._hospital.get_total_number_patients()
        self._user_output.print_hospital_statistics(statistic, total_patients)
