from errors import PatientIDNotExistsError, PatientIDNotIntOrNegativeError, AttemptLowerMinimumStatusError, \
    AttemptUpperMaximumStatusError


class TestErrors:
    def test_patient_id_not_exists_error(self):
       assert str(PatientIDNotExistsError()) == 'Ошибка. В больнице нет пациента с таким ID'

    def test_patient_id_not_int_or_negative_error(self):
        assert str(PatientIDNotIntOrNegativeError()) == 'Ошибка. ID пациента должно быть числом (целым, положительным)'

    def test_attempt_lower_minimum_status_error(self):
        assert str(AttemptLowerMinimumStatusError()) == ('Ошибка. Нельзя понизить самый низкий статус '
                                                         '(наши пациенты не умирают)')

    def test_attempt_upper_maximum_status_error(self):
       assert str(AttemptUpperMaximumStatusError()) == 'Ошибка. Нельзя повысить самый высокий статус'
