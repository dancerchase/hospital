from errors import IDNotIntOrNegativeError, IDNotExistError, MinStatusError, MaxStatusError


class PatientData:
    """Класс для взаимодействия со списком пациентов"""

    def __init__(self):
        self._patients = [1 for _ in range(200)]
        self._status = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    def _transformation_id(self, input_id: str | int) -> int:
        """Преобразование id пациента в индекс в списке пациентов"""
        return int(input_id) - 1

    def get_patient_status_text(self, patient_id: int) -> str:
        """Возвращает текстовое представление статуса пациента"""
        patient_status_for_number_in_list = self._status[self.get_patient_status_number(patient_id)]
        try:
            assert isinstance(patient_status_for_number_in_list, str)
            return patient_status_for_number_in_list
        except AssertionError:
            raise IDNotExistError

    def get_patient_status_number(self, patient_id: int) -> int:
        """Возвращает статус пациента числовым значением из списка пациентов"""
        patient_status_in_list = self._patients[self._get_patient_index(patient_id)]

        try:
            assert isinstance(patient_status_in_list, int)
            return patient_status_in_list
        except AssertionError:
            raise IDNotExistError

    def _get_patient_index(self, patient_id: int) -> int:
        """Возвращает индекс пациента в списке пациентов"""
        return self._transformation_id(patient_id)

    def up_status_for_patient(self, patient_id: int):
        """Увеличивает статус пациента на единицу"""
        try:
            assert self.get_patient_status_number(patient_id) < 3
            self._patients[self._get_patient_index(patient_id)] += 1

        except AssertionError:
            raise MaxStatusError

    def down_status_for_patient(self, patient_id: int):
        """Уменьшает статус пациента на единицу"""
        try:
            assert self.get_patient_status_number(patient_id) > 0
            self._patients[self._get_patient_index(patient_id)] -= 1

        except AssertionError:
            raise MinStatusError

    def patient_discharge(self, patient_id: int):
        """Выписывает пациента из больницы"""
        try:
            assert self._is_patient_valid_in_list(patient_id)
            self._patients[self._get_patient_index(patient_id)] = None
        except AssertionError:
            raise IDNotExistError

    def get_statistic_patients(self) -> dict[str, int]:
        """Возвращает статистику по пациентам"""
        patient_statistic = {'Всего': 0, 'Болен': 0, 'Слегка болен': 0, 'Тяжело болен': 0, 'Готов к выписке': 0}
        for i in self._patients:
            patient_statistic['Всего'] += 1
            if i == 0:
                patient_statistic['Тяжело болен'] += 1
            elif i == 1:
                patient_statistic['Болен'] += 1
            elif i == 2:
                patient_statistic['Слегка болен'] += 1
            elif i == 3:
                patient_statistic['Готов к выписке'] += 1

        return patient_statistic

    def _is_patient_valid_in_list(self, patient_id: int) -> bool:
        """Проверяет существование ID пациента в списке пациентов - ID не None"""
        return self._patients[self._get_patient_index(patient_id)] is not None

    def _get_len_patients_list(self) -> int:
        """Возвращает длинну списка пациентов"""
        return len(self._patients)

    @staticmethod
    def patient_id_positive_check(patient_id: int):
        """Проверяет правильность ввода ID пациента на целое положительное число"""
        try:
            assert patient_id > 0
        except AssertionError:
            raise IDNotIntOrNegativeError

    def patient_id_exist_check(self, patient_id: int):
        """Проверяет правильность ввода ID пациента на существование"""
        try:
            assert patient_id <= self._get_len_patients_list()
            assert self._is_patient_valid_in_list(patient_id)
        except AssertionError:
            raise IDNotExistError
