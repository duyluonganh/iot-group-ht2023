from enum import Enum


class IotCommandType(Enum):
    TURN_ON_THE_LIGHT = 'TURN_ON_THE_LIGHT'
    TURN_ON_ALL_THE_LIGHTS = 'TURN_ON_ALL_THE_LIGHTS'
    TURN_OFF_THE_LIGHT = 'TURN_OFF_THE_LIGHT'
    TURN_OFF_ALL_THE_LIGHTS = 'TURN_OFF_ALL_THE_LIGHTS'
