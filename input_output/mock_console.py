class MockConsole:
    def __init__(self):
        self._expected_requests_and_response = []
        self._expected_output_messages = []

    def add_expected_request_and_response(self, request: str, response: str):
        self._expected_requests_and_response.append((request, response))

    def input(self, request: str) -> str:
        if not self._expected_requests_and_response:
            raise AssertionError

        expected_request, expected_response = self._expected_requests_and_response.pop(0)

        if request != expected_request:
            raise AssertionError

        return expected_response

    def print(self, message: str):
        if not self._expected_output_messages or message != self._expected_output_messages[0]:
            raise AssertionError

        self._expected_output_messages.pop(0)

    def add_expected_output_message(self, message: str):
        self._expected_output_messages.append(message)

    def verify_all_calls_have_been_made(self):
        if self._expected_requests_and_response or self._expected_output_messages:
            raise AssertionError
