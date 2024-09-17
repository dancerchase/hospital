class Console:
    @staticmethod
    def input(message: str) -> str:
        return input(message).lower()

    @staticmethod
    def output(message: str):
        print(message)
