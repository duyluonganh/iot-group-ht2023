import predict
from iotcommand import IotCommand
from iotcommandtype import IotCommandType


def get_iot_command(command):
    if 'turn on all' in command.lower():
        iot_command = IotCommand(other_command_type=IotCommandType.TURN_ON_ALL_THE_LIGHTS, other_properties=[])
    if 'turn off all' in command.lower():
        iot_command = IotCommand(other_command_type=IotCommandType.TURN_OFF_ALL_THE_LIGHTS, other_properties=[])
    if 'turn on' in command.lower():
        iot_command = IotCommand(other_command_type=IotCommandType.TURN_ON_THE_LIGHT, other_properties=[])
        return iot_command
    if 'turn off' in command.lower():
        iot_command = IotCommand(other_command_type=IotCommandType.TURN_OFF_THE_LIGHT, other_properties=[])
    return {}

def get_voice_command(file):
    return predict.predict_for_ws(file)