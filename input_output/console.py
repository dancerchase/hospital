class Console:
    @staticmethod
    def input(message: str) -> str:
        return input(message).lower()

    @staticmethod
    def print(message: str):
        print(message)
