from application import Application
from user_input_commands import UserInputCommands
from user_output_commands import UserOutputCommands
from actions_for_commands import ActionsForCommands

application = Application(user_input_commands=UserInputCommands(), user_output_commands=UserOutputCommands(),
                          actions_for_commands=ActionsForCommands())
application.run_application()
