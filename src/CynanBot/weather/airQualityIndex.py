from enum import Enum, auto

import CynanBot.misc.utils as utils


class AirQualityIndex(Enum):

    FAIR = auto()
    GOOD = auto()
    MODERATE = auto()
    POOR = auto()
    VERY_POOR = auto()

    @classmethod
    def fromInt(cls, airQualityIndex: int):
        if not utils.isValidNum(airQualityIndex):
            raise ValueError(f'airQualityIndex argument is malformed: \"{airQualityIndex}\"')

        if airQualityIndex <= 1:
            return AirQualityIndex.GOOD
        elif airQualityIndex <= 2:
            return AirQualityIndex.FAIR
        elif airQualityIndex <= 3:
            return AirQualityIndex.MODERATE
        elif airQualityIndex <= 4:
            return AirQualityIndex.POOR
        else:
            return AirQualityIndex.VERY_POOR

    def toStr(self) -> str:
        if self is AirQualityIndex.FAIR:
            return 'fair'
        elif self is AirQualityIndex.GOOD:
            return 'good'
        elif self is AirQualityIndex.MODERATE:
            return 'moderate'
        elif self is AirQualityIndex.POOR:
            return 'poor'
        elif self is AirQualityIndex.VERY_POOR:
            return 'very poor'
        else:
            raise RuntimeError(f'unknown AirQualityIndex: \"{self}\"')
