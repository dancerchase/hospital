from errors import UserInputIDIntError, UserInputIDNotExistError
from user_output_commands import UserOutputCommands


class PatientData:
    """Класс для взаимодействия со списком пациентов"""

    def __init__(self):
        self._patients = [1 for _ in range(200)]
        self._status = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    def _transformation_id(self, input_id: str | int) -> int:
        """Преобразование id пациента в индекс в списке пациентов"""
        return int(input_id) - 1

    def get_patient_status_text(self, patient_id: int) -> str | bool:
        """Возвращает текстовое представление статуса пациента"""
        patient_status_for_number_in_list = self._status[self.get_patient_status_number(patient_id)]
        return patient_status_for_number_in_list

    def get_patient_status_number(self, patient_id: int) -> int:
        """Возвращает статус пациента числовым значением из списка пациентов"""
        patient_index = self._transformation_id(patient_id)
        patient_status_in_list = self._patients[patient_index]
        if patient_status_in_list is None:
            return False
        return patient_status_in_list

    def up_status_for_patient(self, patient_id: int):
        """Увеличивает статус пациента на единицу"""
        patient_index = self._transformation_id(patient_id)
        self._patients[patient_index] += 1

    def down_status_for_patient(self, patient_id: int):
        """Уменьшает статус пациента на единицу"""
        patient_index = self._transformation_id(patient_id)
        self._patients[patient_index] -= 1

    def extract(self, patient_id: int):
        """Выписывает пациента из больницы"""
        patient_index = self._transformation_id(patient_id)
        self._patients[patient_index] = None

    def get_statistic_patients(self) -> dict[str, int]:
        """Возвращает статистику по пациентам"""
        patient_statistic = {'Всего': 0, 'Болен': 0, 'Слегка болен': 0, 'Тяжело болен': 0, 'Готов к выписке': 0}
        for i in self._patients:
            if i == 0:
                patient_statistic['Тяжело болен'] += 1
                patient_statistic['Всего'] += 1
            elif i == 1:
                patient_statistic['Болен'] += 1
                patient_statistic['Всего'] += 1
            elif i == 2:
                patient_statistic['Слегка болен'] += 1
                patient_statistic['Всего'] += 1
            elif i == 3:
                patient_statistic['Готов к выписке'] += 1
                patient_statistic['Всего'] += 1
        return patient_statistic

    def patient_id_int_check(self, patient_id: str):
        """Проверяет правильность ввода ID пациента на целое положительное число"""
        try:
            dfg = int(patient_id) < 0
            fgh = int(patient_id)
            assert int(patient_id) > 0
        except (ValueError, AssertionError):
            raise UserInputIDIntError

    def patient_id_exist_check(self, patient_id: int):
        """Проверяет правильность ввода ID пациента на существование"""
        patient_index = self._transformation_id(patient_id)
        try:
            assert patient_id < len(self._patients)
            assert self._patients[patient_index] is not None
        except AssertionError:
            raise UserInputIDNotExistError
