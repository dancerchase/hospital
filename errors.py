class InputCommandError(Exception):
    """Класс для ошибки ввода команды """
    pass


class IDNotIntOrNegativeError(Exception):
    """Класс для ошибки ввода ID пациента - если не целое положительное число"""
    pass


class IDNotExistError(Exception):
    """Класс для ошибки ввода ID пациента - если ID не существует"""
    pass


class MinStatusError(Exception):
    """Класс для ошибки минимизации ID пациента - если попытка уменьшить ID пациента меньше 0"""
    pass


class MaxStatusError(Exception):
    """Класс для ошибки максимизации ID пациента - если попытка увеличить ID пациента больше 3"""
    pass
