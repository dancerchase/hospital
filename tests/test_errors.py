import pytest
from errors import PatientIDNotExistsError, PatientIDNotIntOrNegativeError, AttemptLowerMinimumStatusError, \
    AttemptUpperMaximumStatusError


class TestErrors:
    def test_patient_id_not_exists_error(self):
        with pytest.raises(PatientIDNotExistsError):
            raise PatientIDNotExistsError

        assert str(PatientIDNotExistsError()) == 'Ошибка. В больнице нет пациента с таким ID'

    def test_patient_id_not_int_or_negative_error(self):
        with pytest.raises(PatientIDNotIntOrNegativeError):
            raise PatientIDNotIntOrNegativeError

        assert str(PatientIDNotIntOrNegativeError()) == 'Ошибка. ID пациента должно быть числом (целым, положительным)'

    def test_attempt_lower_minimum_status_error(self):
        with pytest.raises(AttemptLowerMinimumStatusError):
            raise AttemptLowerMinimumStatusError

        assert str(AttemptLowerMinimumStatusError()) == ('Ошибка. Нельзя понизить самый низкий статус '
                                                         '(наши пациенты не умирают)')

    def test_attempt_upper_maximum_status_error(self):
        with pytest.raises(AttemptUpperMaximumStatusError):
            raise AttemptUpperMaximumStatusError

        assert str(AttemptUpperMaximumStatusError()) == 'Ошибка. Нельзя повысить самый высокий статус'
