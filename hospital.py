from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError


class Hospital:
    """Основная бизнес-логика работы приложения"""

    def __init__(self):
        self._patients = [1 for _ in range(200)]
        self._status = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    def get_patient_status_text(self, patient_id: int) -> str:
        patient_status_text = self._status[self._get_patient_status_number(patient_id)]
        return patient_status_text

    def _get_patient_status_number(self, patient_id: int) -> int:
        self._check_patient_exists(patient_id)
        patient_status_number = self._patients[self._convert_patient_id_to_index(patient_id)]
        return patient_status_number

    @staticmethod
    def _convert_patient_id_to_index(patient_id: int) -> int:
        return patient_id - 1

    def up_status_for_patient(self, patient_id: int):
        self._check_patient_exists(patient_id)
        self._patients[self._convert_patient_id_to_index(patient_id)] += 1

    def is_possible_to_up_patient_status(self, patient_id: int) -> bool:
        return self._get_patient_status_number(patient_id) != 3

    def is_patient_status_already_max(self, patient_id: int) -> bool:
        return self._get_patient_status_number(patient_id) == 3

    def down_status_for_patient(self, patient_id: int):
        if self._get_patient_status_number(patient_id) == 0:
            raise AttemptLowerMinimumStatusError
        self._patients[self._convert_patient_id_to_index(patient_id)] -= 1

    def patient_discharge(self, patient_id: int):
        self._check_patient_exists(patient_id)
        self._patients[self._convert_patient_id_to_index(patient_id)] = None

    def get_statistics_patients_statuses(self) -> dict[str, int]:
        patient_statistic = {'Болен': 0, 'Слегка болен': 0, 'Тяжело болен': 0, 'Готов к выписке': 0}
        for i in self._patients:
            if i == 0:
                patient_statistic['Тяжело болен'] += 1
            elif i == 1:
                patient_statistic['Болен'] += 1
            elif i == 2:
                patient_statistic['Слегка болен'] += 1
            elif i == 3:
                patient_statistic['Готов к выписке'] += 1

        return patient_statistic

    def get_total_number_patients(self):
        return len(list(filter(lambda x: x is not None, self._patients)))

    def _check_patient_exists(self, patient_id: int):
        try:
            patient_status = self._patients[self._convert_patient_id_to_index(patient_id)]
            if patient_status is None:
                raise PatientIDNotExistsError
        except IndexError:
            raise PatientIDNotExistsError
