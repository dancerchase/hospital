import pytest
from hospital import Hospital
from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError, AttemptUpperMaximumStatusError, \
    PatientStatusNotExistsError


class TestHospital:
    class TestGetPatientStatus:

        def test_get_patient_status(self):
            hospital = Hospital(patients=[2, 0], statuses={0: "Стабильное состояние", 2: "Готов к выписке"})

            assert hospital.get_patient_status(1) == "Готов к выписке"

        def test_get_status_patient_id_not_exists(self):
            hospital = Hospital([1, 1, 1])

            with pytest.raises(PatientIDNotExistsError):
                hospital.get_patient_status(4)

        def test_get_patient_status_patient_already_discharged(self):
            hospital = Hospital([1, None, 0])

            with pytest.raises(PatientIDNotExistsError):
                hospital.get_patient_status(2)

        def test_patient_base_statuses(self):
            assert Hospital()._statuses == {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

        def test_patient_other_statuses(self):
            hospital = Hospital(
                statuses={0: "Состояние средней тяжести",
                          1: "Слабое состояние",
                          2: "Стабильное состояние",
                          3: "Готов к выписке"})

            assert hospital._statuses == {0: "Состояние средней тяжести",
                                          1: "Слабое состояние",
                                          2: "Стабильное состояние",
                                          3: "Готов к выписке"}

    class TestDownStatusForPatient:

        def test_down_status_for_patient(self):
            hospital = Hospital(patients=[5, 0],
                                statuses={0: "Состояние средней тяжести", 4: "Слегка болен", 5: "Готов к выписке"})

            hospital.down_status_for_patient(1)

            assert hospital._patients == [4, 0]

        def test_down_status_for_patient_minimum_status(self):
            hospital = Hospital(patients=[3, 4],
                                statuses={4: "Готов к выписке", 3: "Состояние средней тяжести"})

            with pytest.raises(AttemptLowerMinimumStatusError):
                hospital.down_status_for_patient(1)

            assert hospital._patients == [3, 4]

        def test_down_status_for_patient_id_not_exists(self):
            hospital = Hospital([1, 1, 1])

            with pytest.raises(PatientIDNotExistsError):
                hospital.down_status_for_patient(4)

        def test_down_status_for_patient_already_discharged(self):
            hospital = Hospital([1, None, 0])

            with pytest.raises(PatientIDNotExistsError):
                hospital.down_status_for_patient(2)

    class TestUpStatusForPatient:

        def test_up_status_for_patient(self):
            hospital = Hospital(patients=[3, 0],
                                statuses={0: "Состояние средней тяжести", 1: "Слабое состояние", 3: "Готов к выписке"})

            hospital.up_status_for_patient(2)

            assert hospital._patients == [3, 1]

        def test_up_status_for_patient_maximum_status(self):
            hospital = Hospital(patients=[5, 0], statuses={0: "Состояние средней тяжести", 5: "Готов к выписке"})

            with pytest.raises(AttemptUpperMaximumStatusError):
                hospital.up_status_for_patient(1)

            assert hospital._patients == [5, 0]

        def test_up_status_for_patient_id_not_exists(self):
            hospital = Hospital([1, 2])

            with pytest.raises(PatientIDNotExistsError):
                hospital.up_status_for_patient(4)

        def test_up_status_for_patient_already_discharged(self):
            hospital = Hospital([1, None, 0])

            with pytest.raises(PatientIDNotExistsError):
                hospital.up_status_for_patient(2)

    class TestIsPossibleToUpPatientStatus:

        def test_is_possible_to_up_patient_status(self):
            hospital = Hospital(patients=[5, 1],
                                statuses={1: "Слабое состояние", 2: "Стабильное состояние", 5: "Готов к выписке"})

            assert hospital.is_possible_to_up_patient_status(2)

        def test_is_not_possible_to_up_patient_status(self):
            hospital = Hospital(patients=[5, 1],
                                statuses={1: "Слабое состояние", 2: "Стабильное состояние", 5: "Готов к выписке"})

            assert not hospital.is_possible_to_up_patient_status(1)

    class TestPatientDischarge:

        def test_patient_discharge(self):
            hospital = Hospital([3, 1])

            hospital.patient_discharge(2)

            assert hospital._patients == [3, None]

        def test_patient_discharge_id_not_exists(self):
            hospital = Hospital([1, 2, 3])

            with pytest.raises(PatientIDNotExistsError):
                hospital.patient_discharge(6)

        def test_patient_discharge_already_discharged(self):
            hospital = Hospital([2, None, None])

            with pytest.raises(PatientIDNotExistsError):
                hospital.patient_discharge(3)

    class TestGetTotalNumberPatients:

        def test_get_total_number_patients(self):
            hospital = Hospital([2, None, 1, 3, 0, None])

            assert hospital.get_total_number_patients() == 4

    class TestGetStatisticsPatientsStatuses:

        def test_get_statistics_patients_statuses_all(self):
            hospital = Hospital(patients=[1, 2, None, 3, 0, None, 1],
                                statuses={0: "Состояние средней тяжести",
                                          1: "Слабое состояние",
                                          2: "Стабильное состояние",
                                          3: "Готов к выписке"})

            assert hospital.get_statistics_patients_statuses() == {'Состояние средней тяжести': 1,
                                                                   'Слабое состояние': 2,
                                                                   'Стабильное состояние': 1,
                                                                   'Готов к выписке': 1}

        def test_get_statistics_patients_statuses(self):
            hospital = Hospital(patients=[1, 2, 3, None],
                                statuses={0: "Состояние средней тяжести",
                                          1: "Слабое состояние",
                                          2: "Стабильное состояние",
                                          3: "Готов к выписке"})

            assert hospital.get_statistics_patients_statuses() == {'Слабое состояние': 1,
                                                                   'Стабильное состояние': 1,
                                                                   'Готов к выписке': 1}

    class TestCheckPatientExists:

        def test_patient_id_not_in_patient_list(self):
            hospital = Hospital([1, 2, 3])

            with pytest.raises(PatientIDNotExistsError):
                hospital._check_patient_exists(4)

        def test_patient_status_in_patient_list_is_none(self):
            hospital = Hospital([None, 2, 3])

            with pytest.raises(PatientIDNotExistsError):
                hospital._check_patient_exists(1)

        def test_if_patient_exists_error_not_raised(self):
            hospital = Hospital([0, 2])

            hospital._check_patient_exists(1)

    class TestAddNewPatient:

        def test_add_new_patient(self):
            hospital = Hospital([1, 2])

            hospital.add_new_patient('Болен')

            assert hospital._patients == [1, 2, 1]

        def test_add_new_patient_invalid_status(self):
            hospital = Hospital([1, 2])

            with pytest.raises(PatientStatusNotExistsError):
                hospital.add_new_patient('Инвалидный статус')

            assert hospital._patients == [1, 2]

    class TestCheckStatusExists:

        def test_check_status_exists(self):
            hospital = Hospital(statuses={0: "Состояние средней тяжести"})
            hospital._check_status_exist('Состояние средней тяжести')

        def test_check_status_not_exists(self):
            hospital = Hospital(statuses={0: "Состояние средней тяжести"})

            with pytest.raises(PatientStatusNotExistsError):
                hospital._check_status_exist('несуществующий статус')
