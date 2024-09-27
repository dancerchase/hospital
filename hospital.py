from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError, AttemptUpperMaximumStatusError


class Hospital:
    """Основная бизнес-логика работы приложения"""

    def __init__(self, statuses, patients=None, ):
        self._statuses = statuses

        if patients:
            self._patients = patients
        else:
            self._patients = [1 for _ in range(200)]

    def get_patient_status(self, patient_id: int) -> str:
        self._check_patient_exists(patient_id)
        patient_status_text = self._statuses[self._get_patient_status_number(patient_id)]
        return patient_status_text

    def _get_patient_status_number(self, patient_id: int) -> int:
        patient_status_number = self._patients[self._convert_patient_id_to_index(patient_id)]
        return patient_status_number

    @staticmethod
    def _convert_patient_id_to_index(patient_id: int) -> int:
        return patient_id - 1

    def up_status_for_patient(self, patient_id: int):
        self._check_patient_exists(patient_id)
        if not self.is_possible_to_up_patient_status(patient_id):
            raise AttemptUpperMaximumStatusError
        self._patients[self._convert_patient_id_to_index(patient_id)] += 1

    def is_possible_to_up_patient_status(self, patient_id: int) -> bool:
        self._check_patient_exists(patient_id)
        return self._get_patient_status_number(patient_id) < self._get_maximum_status_number()

    def is_possible_to_down_patient_status(self, patient_id: int) -> bool:
        self._check_patient_exists(patient_id)
        return self._get_patient_status_number(patient_id) > self._get_minimum_status_number()

    def down_status_for_patient(self, patient_id: int):
        self._check_patient_exists(patient_id)
        if not self.is_possible_to_down_patient_status(patient_id):
            raise AttemptLowerMinimumStatusError
        self._patients[self._convert_patient_id_to_index(patient_id)] -= 1

    def _get_maximum_status_number(self) -> int:
        return max(self._statuses.keys())

    def _get_minimum_status_number(self) -> int:
        return min(self._statuses.keys())

    def patient_discharge(self, patient_id: int):
        self._check_patient_exists(patient_id)
        self._patients[self._convert_patient_id_to_index(patient_id)] = None

    def get_statistics_patients_statuses(self) -> dict[str, int]:
        patient_statistic = dict()
        for i in self._patients:
            if i == 0:
                patient_statistic['Тяжело болен'] = patient_statistic.get('Тяжело болен', 0) + 1
            elif i == 1:
                patient_statistic['Болен'] = patient_statistic.get('Болен', 0) + 1
            elif i == 2:
                patient_statistic['Слегка болен'] = patient_statistic.get('Слегка болен', 0) + 1
            elif i == 3:
                patient_statistic['Готов к выписке'] = patient_statistic.get('Готов к выписке', 0) + 1

        return patient_statistic

    def get_total_number_patients(self) -> int:
        return len(list(filter(lambda x: x is not None, self._patients)))

    def _check_patient_exists(self, patient_id: int):
        if patient_id > len(self._patients) or self._patients[self._convert_patient_id_to_index(patient_id)] is None:
            raise PatientIDNotExistsError
