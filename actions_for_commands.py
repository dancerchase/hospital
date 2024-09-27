from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError, PatientIDNotIntOrNegativeError


class ActionsForCommands:
    """Содержит методы для работы с командами"""

    def __init__(self, input_output_manager, hospital):
        self._input_output_manager = input_output_manager
        self._hospital = hospital

    def get_patient_status(self):
        try:
            patient_id = self._input_output_manager.get_patient_id()
            patient_status = self._hospital.get_patient_status(patient_id)
            self._input_output_manager.send_message_patient_status(patient_status)

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError) as error:
            self._input_output_manager.send_message_with_received_text(str(error))

    def up_patient_status(self):
        try:
            patient_id = self._input_output_manager.get_patient_id()

            if self._hospital.is_possible_to_up_patient_status(patient_id):
                self._hospital.up_status_for_patient(patient_id)
                new_status = self._hospital.get_patient_status(patient_id)
                self._input_output_manager.send_message_new_status(new_status)

            else:
                if self._input_output_manager.request_for_discharge():
                    self._hospital.patient_discharge(patient_id)
                    self._input_output_manager.send_message_patient_discharge()
                else:
                    self._input_output_manager.send_message_out_refusal_of_discharge()

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError) as error:
            self._input_output_manager.send_message_with_received_text(str(error))

    def down_patient_status(self):
        try:
            patient_id = self._input_output_manager.get_patient_id()
            self._hospital.down_status_for_patient(patient_id)
            new_status = self._hospital.get_patient_status(patient_id)
            self._input_output_manager.send_message_new_status(new_status)

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError, AttemptLowerMinimumStatusError) as error:
            self._input_output_manager.send_message_with_received_text(str(error))

    def discharge_patient(self):
        try:
            patient_id = self._input_output_manager.get_patient_id()
            self._hospital.patient_discharge(patient_id)
            self._input_output_manager.send_message_patient_discharge()

        except (PatientIDNotIntOrNegativeError, PatientIDNotExistsError) as error:
            self._input_output_manager.send_message_with_received_text(str(error))

    def get_hospital_statistics(self):
        statistic = self._hospital.get_statistics_patients_statuses()
        total_patients = self._hospital.get_total_number_patients()
        self._input_output_manager.send_message_hospital_statistics_text(statistic, total_patients)

    def add_new_patient(self):
        status = self._input_output_manager.get_new_patient_status()
        patient_id = self._hospital.add_new_patient(status)
        self._input_output_manager.send_message_patient_added(patient_id)
