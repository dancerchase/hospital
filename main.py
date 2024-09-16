from application import Application
from input_output.input_output_manager import InputOutputManager
from actions_for_commands import ActionsForCommands
from hospital import Hospital
from input_output.console import Console

input_output_manager = InputOutputManager(Console())

hospital = Hospital()

actions_for_commands = ActionsForCommands(input_output_manager, hospital)

application = Application(input_output_manager, actions_for_commands)

application.run_application()
