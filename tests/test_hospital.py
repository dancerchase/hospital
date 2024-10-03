import pytest
from hospital import Hospital
from errors import PatientIDNotExistsError, AttemptLowerMinimumStatusError, AttemptUpperMaximumStatusError, \
    PatientStatusNotExistsError

base_statuses = {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}


class TestHospital:
    class TestGetPatientStatus:

        def test_get_patient_status(self):
            hospital = Hospital(patients=[2, 0], statuses=base_statuses)

            assert hospital.get_patient_status(1) == "Слегка болен"

        def test_get_status_patient_id_not_exists(self):
            hospital = Hospital(patients=[1, 1, 1], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.get_patient_status(4)

        def test_get_patient_status_patient_already_discharged(self):
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.get_patient_status(2)

        def test_patient_statuses(self):
            hospital = Hospital(patients=[], statuses=base_statuses)
            assert hospital._statuses == {0: "Тяжело болен", 1: "Болен", 2: "Слегка болен", 3: "Готов к выписке"}

    class TestDownStatusForPatient:

        def test_down_status_for_patient(self):
            hospital = Hospital(patients=[3, 0], statuses=base_statuses)

            hospital.down_status_for_patient(1)

            assert hospital._patients == [2, 0]

        def test_down_status_for_patient_minimum_status(self):
            hospital = Hospital(patients=[3, 0], statuses=base_statuses)

            with pytest.raises(AttemptLowerMinimumStatusError):
                hospital.down_status_for_patient(2)

            assert hospital._patients == [3, 0]

        def test_down_status_for_patient_id_not_exists(self):
            hospital = Hospital(patients=[1, 1, 1], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.down_status_for_patient(4)

        def test_down_status_for_patient_already_discharged(self):
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.down_status_for_patient(2)

        def test_down_status_for_patient_with_other_statuses(self):
            statuses = {-1: 'Критическое состояние', 0: "Тяжело болен", 1: 'Среднее состояние'}
            hospital = Hospital(patients=[-1, 0, 1], statuses=statuses)

            hospital.down_status_for_patient(2)

            assert hospital._patients == [-1, -1, 1]

        def test_down_status_for_patient_minimum_status_with_other_statuses(self):
            statuses = {-1: 'Критическое состояние', 0: "Тяжело болен", 1: 'Среднее состояние'}
            hospital = Hospital(patients=[-1, 0], statuses=statuses)

            with pytest.raises(AttemptLowerMinimumStatusError):
                hospital.down_status_for_patient(1)

            assert hospital._patients == [-1, 0]

        def test_down_status_for_patient_to_next_status(self):
            statuses = {10: 'Критическое состояние',
                        20: 'Среднее состояние',
                        30: "Хорошее состояние",
                        40: "Может быть выписан"}
            hospital = Hospital(patients=[20, 40], statuses=statuses)

            hospital.down_status_for_patient(1)

            assert hospital._patients == [10, 40]

    class TestUpStatusForPatient:

        def test_up_status_for_patient(self):
            hospital = Hospital(patients=[3, 0], statuses=base_statuses)

            hospital.up_status_for_patient(2)

            assert hospital._patients == [3, 1]

        def test_up_status_for_patient_maximum_status(self):
            hospital = Hospital(patients=[3, 0], statuses=base_statuses)

            with pytest.raises(AttemptUpperMaximumStatusError):
                hospital.up_status_for_patient(1)

            assert hospital._patients == [3, 0]

        def test_up_status_for_patient_id_not_exists(self):
            hospital = Hospital(patients=[1, 2], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.up_status_for_patient(4)

        def test_up_status_for_patient_already_discharged(self):
            hospital = Hospital(patients=[1, None, 0], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.up_status_for_patient(2)

        def test_up_status_for_patient_with_other_statuses(self):
            statuses = {1: 'Критическое состояние', 2: "Тяжело болен", 3: 'Среднее состояние', 4: "Хорошее состояние",
                        5: "Может быть выписан"}
            hospital = Hospital(patients=[3, 5], statuses=statuses)

            hospital.up_status_for_patient(1)

            assert hospital._patients == [4, 5]

        def test_up_status_for_patient_maximum_status_with_other_statuses(self):
            statuses = {1: 'Критическое состояние', 2: "Тяжело болен", 3: 'Среднее состояние', 4: "Хорошее состояние",
                        5: "Может быть выписан"}
            hospital = Hospital(patients=[4, 5], statuses=statuses)

            with pytest.raises(AttemptUpperMaximumStatusError):
                hospital.up_status_for_patient(2)

            assert hospital._patients == [4, 5]

        def test_up_status_for_patient_to_next_status(self):
            statuses = {10: 'Критическое состояние',
                        20: 'Среднее состояние',
                        30: "Хорошее состояние",
                        40: "Может быть выписан"}
            hospital = Hospital(patients=[20, 40], statuses=statuses)

            hospital.up_status_for_patient(1)

            assert hospital._patients == [30, 40]

    class TestIsPossibleToUpPatientStatus:

        def test_is_possible_to_up_patient_status(self):
            hospital = Hospital(patients=[3, 1], statuses=base_statuses)

            assert hospital.is_possible_to_up_patient_status(2)

        def test_is_not_possible_to_up_patient_status(self):
            hospital = Hospital(patients=[3, 1], statuses=base_statuses)

            assert not hospital.is_possible_to_up_patient_status(1)

        def test_is_possible_to_up_patient_status_with_other_statuses_model(self):
            statuses = {1: 'Критическое состояние', 2: "Тяжело болен", 3: 'Среднее состояние', 4: "Хорошее состояние",
                        5: "Может быть выписан"}
            hospital = Hospital(patients=[4, 5], statuses=statuses)

            assert hospital.is_possible_to_up_patient_status(1)

        def test_is_not_possible_to_up_patient_status_with_other_statuses_model(self):
            statuses = {1: 'Критическое состояние', 2: "Тяжело болен", 3: 'Среднее состояние', 4: "Хорошее состояние",
                        5: "Может быть выписан"}
            hospital = Hospital(patients=[4, 5], statuses=statuses)

            assert not hospital.is_possible_to_up_patient_status(2)

    class TestIsPossibleToDownPatientStatus:
        def test_is_possible_to_down_patient_status(self):
            hospital = Hospital(patients=[3, 2], statuses=base_statuses)

            assert hospital._is_possible_to_down_patient_status(2)

        def test_is_not_possible_to_down_patient_status(self):
            hospital = Hospital(patients=[0, 2], statuses=base_statuses)

            assert not hospital._is_possible_to_down_patient_status(1)

        def test_is_possible_to_down_patient_status_with_other_statuses(self):
            statuses = {-1: 'Критическое состояние', 0: "Тяжело болен", 1: 'Среднее состояние', 2: "Хорошее состояние"}
            hospital = Hospital(patients=[0, -1], statuses=statuses)

            assert hospital._is_possible_to_down_patient_status(1)

        def test_is_not_possible_to_down_patient_status_with_other_statuses(self):
            statuses = {-1: 'Критическое состояние', 0: "Тяжело болен", 1: 'Среднее состояние', 2: "Хорошее состояние"}
            hospital = Hospital(patients=[0, -1], statuses=statuses)

            assert not hospital._is_possible_to_down_patient_status(2)

    class TestPatientDischarge:

        def test_patient_discharge(self):
            hospital = Hospital(patients=[3, 1], statuses=base_statuses)

            hospital.patient_discharge(2)

            assert hospital._patients == [3, None]

        def test_patient_discharge_id_not_exists(self):
            hospital = Hospital(patients=[1, 2, 3], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.patient_discharge(6)

        def test_patient_discharge_already_discharged(self):
            hospital = Hospital(patients=[2, None, None], statuses=base_statuses)

            with pytest.raises(PatientIDNotExistsError):
                hospital.patient_discharge(3)

    class TestGetTotalNumberPatients:

        def test_get_total_number_patients(self):
            hospital = Hospital(patients=[2, None, 1, 3, 0, None], statuses=base_statuses)

            assert hospital.get_total_number_patients() == 4

    class TestGetStatisticsPatientsStatuses:

        def test_get_statistics_patients_statuses_all(self):
            hospital = Hospital(patients=[1, 2, None, 3, 0, None, 1], statuses=base_statuses)

            assert hospital.get_statistics_patients_statuses() == {'Болен': 2,
                                                                   'Слегка болен': 1,
                                                                   'Тяжело болен': 1,
                                                                   'Готов к выписке': 1}

        def test_get_statistics_patients_statuses(self):
            hospital = Hospital(patients=[1, 2, 3, None], statuses=base_statuses)

            assert hospital.get_statistics_patients_statuses() == {'Болен': 1,
                                                                   'Слегка болен': 1,
                                                                   'Готов к выписке': 1}

        def test_get_statistics_patients_statuses_with_other_statuses(self):
            statuses = {-1: "Критическое состояние",
                        0: "Плохое состояние",
                        1: "Хорошее состояние",
                        2: "Может быть выписан",
                        3: "В стадии оформления на выписку"}
            hospital = Hospital(patients=[3, -1, 2, None, 1, 0, None, 1], statuses=statuses)

            assert hospital.get_statistics_patients_statuses() == {"В стадии оформления на выписку": 1,
                                                                   'Критическое состояние': 1,
                                                                   'Плохое состояние': 1,
                                                                   'Хорошее состояние': 2,
                                                                   'Может быть выписан': 1}

        class TestCheckPatientExists:

            def test_patient_id_not_in_patient_list(self):
                hospital = Hospital(patients=[1, 2, 3], statuses=base_statuses)

                with pytest.raises(PatientIDNotExistsError):
                    hospital._check_patient_exists(4)

            def test_patient_status_in_patient_list_is_none(self):
                hospital = Hospital(patients=[None, 2, 3], statuses=base_statuses)

                with pytest.raises(PatientIDNotExistsError):
                    hospital._check_patient_exists(1)

            def test_if_patient_exists_error_not_raised(self):
                hospital = Hospital(patients=[1, 2, 3], statuses=base_statuses)

                hospital._check_patient_exists(1)

        class TestAddNewPatient:
            def test_add_new_patient(self):
                hospital = Hospital(patients=[1, 2, None], statuses=base_statuses)

                patient_id = hospital.add_new_patient('Готов к выписке')

                assert patient_id == 4
                assert hospital._patients == [1, 2, None, 3]

            def test_add_new_patient_status_not_exists(self):
                hospital = Hospital(patients=[1, 2, None], statuses=base_statuses)

                with pytest.raises(PatientStatusNotExistsError):
                    hospital.add_new_patient('несуществующий статус')

    class TestGetNewStatusNumber:

        def test_get_new_status_number(self):
            statuses = {10: 'Критическое состояние',
                        20: 'Среднее состояние',
                        30: "Хорошее состояние",
                        40: "Может быть выписан"}
            hospital = Hospital(patients=[10, 40], statuses=statuses)

            assert hospital._get_new_status_number(1) == 20
