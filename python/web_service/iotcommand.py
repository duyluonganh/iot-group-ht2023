from iotcommandtype import IotCommandType


class IotCommand:
    command_type = IotCommandType.TURN_ON_THE_LIGHT
    properties = []

    def __init__(self, other_command_type, other_properties):
        self.command_type = other_command_type
        self.properties.append(other_properties)
