from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface


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

        if jsonString == 'cheer':
            return SoundAlert.CHEER
        elif jsonString == 'point_redemption_01':
            return SoundAlert.POINT_REDEMPTION_01
        elif jsonString == 'point_redemption_02':
            return SoundAlert.POINT_REDEMPTION_02
        elif jsonString == 'point_redemption_03':
            return SoundAlert.POINT_REDEMPTION_03
        elif jsonString == 'point_redemption_04':
            return SoundAlert.POINT_REDEMPTION_04
        elif jsonString == 'point_redemption_05':
            return SoundAlert.POINT_REDEMPTION_05
        elif jsonString == 'point_redemption_06':
            return SoundAlert.POINT_REDEMPTION_06
        elif jsonString == 'point_redemption_07':
            return SoundAlert.POINT_REDEMPTION_07
        elif jsonString == 'point_redemption_08':
            return SoundAlert.POINT_REDEMPTION_08
        elif jsonString == 'point_redemption_09':
            return SoundAlert.POINT_REDEMPTION_09
        elif jsonString == 'point_redemption_10':
            return SoundAlert.POINT_REDEMPTION_10
        elif jsonString == 'point_redemption_11':
            return SoundAlert.POINT_REDEMPTION_11
        elif jsonString == 'point_redemption_12':
            return SoundAlert.POINT_REDEMPTION_12
        elif jsonString == 'point_redemption_13':
            return SoundAlert.POINT_REDEMPTION_13
        elif jsonString == 'point_redemption_14':
            return SoundAlert.POINT_REDEMPTION_14
        elif jsonString == 'point_redemption_15':
            return SoundAlert.POINT_REDEMPTION_15
        elif jsonString == 'point_redemption_16':
            return SoundAlert.POINT_REDEMPTION_16
        elif jsonString == 'raid':
            return SoundAlert.RAID
        elif jsonString == 'subscribe':
            return SoundAlert.SUBSCRIBE
        else:
            self.__timber.log('SoundAlertJsonMapper', f'Encountered unknown SoundAlert value: \"{jsonString}\"')
            return None
