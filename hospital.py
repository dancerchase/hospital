from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError, AttemptUpperMaximumStatusError


class Hospital:
    """Основная бизнес-логика работы приложения"""

    def __init__(self, patients=None, statuses=None):
        if patients:
            self._patients = patients
        else:
            self._patients = [1 for _ in range(200)]

        if statuses:
            self._statuses = statuses
        else:
            self._statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

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
        if self._get_patient_status_number(patient_id) == self._max_status_number():
            raise AttemptUpperMaximumStatusError
        self._patients[self._convert_patient_id_to_index(patient_id)] += 1

    def is_possible_to_up_patient_status(self, patient_id: int) -> bool:
        self._check_patient_exists(patient_id)
        return self._get_patient_status_number(patient_id) < self._max_status_number()

    def down_status_for_patient(self, patient_id: int):
        self._check_patient_exists(patient_id)
        if self._get_patient_status_number(patient_id) == self._min_status_number():
            raise AttemptLowerMinimumStatusError
        self._patients[self._convert_patient_id_to_index(patient_id)] -= 1

    def patient_discharge(self, patient_id: int):
        self._check_patient_exists(patient_id)
        self._patients[self._convert_patient_id_to_index(patient_id)] = None

    def get_statistics_patients_statuses(self) -> dict[str, int]:
        patient_statistic = dict()
        for i in self._patients:
            if i is not None:
                status = self._statuses[i]
                patient_statistic[status] = patient_statistic.get(status, 0) + 1

        return patient_statistic

    def get_total_number_patients(self) -> int:
        return len(list(filter(lambda x: x is not None, self._patients)))

    def _check_patient_exists(self, patient_id: int):
        if patient_id > len(self._patients) or self._patients[self._convert_patient_id_to_index(patient_id)] is None:
            raise PatientIDNotExistsError

    def _max_status_number(self) -> int:
        return max(self._statuses.keys())

    def _min_status_number(self) -> int:
        return min(self._statuses.keys())

    def add_new_patient(self, status: str):
        self._check_status(status)
        status_number = self._get_number_status(status)
        self._patients.append(status_number)
        return self._patients.index(status_number, -1) + 1

    def _get_number_status(self, status: str) -> int:
        for key, value in self._statuses.items():
            if value == status:
                return key

    def _check_status(self, status: str):
        if status not in self._statuses.values():
            raise PatientIDNotExistsError
