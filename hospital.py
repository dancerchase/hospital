from patient_data import PatientData
from user_output_commands import UserOutputCommands
from user_input_commands import UserInputCommands


class Hospital:
    """Класс использует в себе классы PatientData, UserInputCommands и UserOutputCommands. Содержит в себе логику
    обработки команд пользователя и отвечает за запуск программы"""
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

