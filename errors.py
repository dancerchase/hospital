class PatientIDNotIntOrNegativeError(Exception):
    def __init__(self):
        super().__init__('Ошибка. ID пациента должно быть числом (целым, положительным)')


class PatientIDNotExistsError(Exception):
    def __init__(self):
        super().__init__('Ошибка. В больнице нет пациента с таким ID')


class AttemptLowerMinimumStatusError(Exception):
    def __init__(self):
        super().__init__('Ошибка. Нельзя понизить самый низкий статус (наши пациенты не умирают)')


class AttemptUpperMaximumStatusError(Exception):
    def __init__(self):
        super().__init__('Ошибка. Нельзя повысить самый высокий статус')
