from .soundAlert import SoundAlert
from .soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from ..timber.timberInterface import TimberInterface


class SoundAlertJsonMapper(SoundAlertJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    def parseSoundAlert(
        self,
        jsonString: str | None
    ) -> SoundAlert | None:
        if jsonString is None:
            return None
        elif not isinstance(jsonString, str):
            raise TypeError(f'jsonString argument is malformed: \"{jsonString}\"')

        jsonString = jsonString.lower()

        match jsonString:
            case 'cheer': return SoundAlert.CHEER
            case 'point_redemption_01': return SoundAlert.POINT_REDEMPTION_01
            case 'point_redemption_02': return SoundAlert.POINT_REDEMPTION_02
            case 'point_redemption_03': return SoundAlert.POINT_REDEMPTION_03
            case 'point_redemption_04': return SoundAlert.POINT_REDEMPTION_04
            case 'point_redemption_05': return SoundAlert.POINT_REDEMPTION_05
            case 'point_redemption_06': return SoundAlert.POINT_REDEMPTION_06
            case 'point_redemption_07': return SoundAlert.POINT_REDEMPTION_07
            case 'point_redemption_08': return SoundAlert.POINT_REDEMPTION_08
            case 'point_redemption_09': return SoundAlert.POINT_REDEMPTION_09
            case 'point_redemption_10': return SoundAlert.POINT_REDEMPTION_10
            case 'point_redemption_11': return SoundAlert.POINT_REDEMPTION_11
            case 'point_redemption_12': return SoundAlert.POINT_REDEMPTION_12
            case 'point_redemption_13': return SoundAlert.POINT_REDEMPTION_13
            case 'point_redemption_14': return SoundAlert.POINT_REDEMPTION_14
            case 'point_redemption_15': return SoundAlert.POINT_REDEMPTION_15
            case 'point_redemption_16': return SoundAlert.POINT_REDEMPTION_16
            case 'raid': return SoundAlert.RAID
            case 'random_from_directory': return SoundAlert.RANDOM_FROM_DIRECTORY
            case 'subscribe': return SoundAlert.SUBSCRIBE
            case _:
                self.__timber.log('SoundAlertJsonMapper', f'Encountered unknown SoundAlert value: \"{jsonString}\"')
                return None
