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
            case 'bean': return SoundAlert.BEAN
            case 'cheer': return SoundAlert.CHEER
            case 'click_navigation': return SoundAlert.CLICK_NAVIGATION
            case 'jackpot': return SoundAlert.JACKPOT
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
            case 'tnt_1': return SoundAlert.TNT_1
            case 'tnt_2': return SoundAlert.TNT_2
            case 'tnt_3': return SoundAlert.TNT_3
            case _:
                self.__timber.log('SoundAlertJsonMapper', f'Encountered unknown SoundAlert value: \"{jsonString}\"')
                return None

    def serializeSoundAlert(
        self,
        soundAlert: SoundAlert
    ) -> str:
        if not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        match soundAlert:
            case SoundAlert.BEAN: return 'bean'
            case SoundAlert.CHEER: return 'cheer'
            case SoundAlert.CLICK_NAVIGATION: return 'click_navigation'
            case SoundAlert.JACKPOT: return 'jackpot'
            case SoundAlert.POINT_REDEMPTION_01: return 'point_redemption_01'
            case SoundAlert.POINT_REDEMPTION_02: return 'point_redemption_02'
            case SoundAlert.POINT_REDEMPTION_03: return 'point_redemption_03'
            case SoundAlert.POINT_REDEMPTION_04: return 'point_redemption_04'
            case SoundAlert.POINT_REDEMPTION_05: return 'point_redemption_05'
            case SoundAlert.POINT_REDEMPTION_06: return 'point_redemption_06'
            case SoundAlert.POINT_REDEMPTION_07: return 'point_redemption_07'
            case SoundAlert.POINT_REDEMPTION_08: return 'point_redemption_08'
            case SoundAlert.POINT_REDEMPTION_09: return 'point_redemption_09'
            case SoundAlert.POINT_REDEMPTION_10: return 'point_redemption_10'
            case SoundAlert.POINT_REDEMPTION_11: return 'point_redemption_11'
            case SoundAlert.POINT_REDEMPTION_12: return 'point_redemption_12'
            case SoundAlert.POINT_REDEMPTION_13: return 'point_redemption_13'
            case SoundAlert.POINT_REDEMPTION_14: return 'point_redemption_14'
            case SoundAlert.POINT_REDEMPTION_15: return 'point_redemption_15'
            case SoundAlert.POINT_REDEMPTION_16: return 'point_redemption_16'
            case SoundAlert.RAID: return 'raid'
            case SoundAlert.RANDOM_FROM_DIRECTORY: return 'random_from_directory'
            case SoundAlert.SUBSCRIBE: return 'subscribe'
            case SoundAlert.TNT_1: return 'tnt_1'
            case SoundAlert.TNT_2: return 'tnt_2'
            case SoundAlert.TNT_3: return 'tnt_3'
            case _: raise ValueError(f'Unknown SoundAlert value: \"{soundAlert}\"')
