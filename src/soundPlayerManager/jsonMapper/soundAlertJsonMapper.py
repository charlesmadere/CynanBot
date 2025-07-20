from typing import Any

from .soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from ..soundAlert import SoundAlert
from ...misc import utils as utils


class SoundAlertJsonMapper(SoundAlertJsonMapperInterface):

    def parseSoundAlert(
        self,
        jsonString: str | Any | None
    ) -> SoundAlert | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'air_strike': return SoundAlert.AIR_STRIKE
            case 'bean': return SoundAlert.BEAN
            case 'cheer': return SoundAlert.CHEER
            case 'click_navigation': return SoundAlert.CLICK_NAVIGATION
            case 'follow': return SoundAlert.FOLLOW
            case 'grenade_1': return SoundAlert.GRENADE_1
            case 'grenade_2': return SoundAlert.GRENADE_2
            case 'grenade_3': return SoundAlert.GRENADE_3
            case 'jackpot': return SoundAlert.JACKPOT
            case 'launch_air_strike': return SoundAlert.LAUNCH_AIR_STRIKE
            case 'mega_grenade_1': return SoundAlert.MEGA_GRENADE_1
            case 'mega_grenade_2': return SoundAlert.MEGA_GRENADE_2
            case 'mega_grenade_3': return SoundAlert.MEGA_GRENADE_3
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
            case 'splat': return SoundAlert.SPLAT
            case 'subscribe': return SoundAlert.SUBSCRIBE
            case 'tnt': return SoundAlert.AIR_STRIKE
            case _: return None

    def requireSoundAlert(
        self,
        jsonString: str | Any | None
    ) -> SoundAlert:
        result = self.parseSoundAlert(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into SoundAlert value!')

        return result

    def serializeSoundAlert(
        self,
        soundAlert: SoundAlert
    ) -> str:
        if not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        match soundAlert:
            case SoundAlert.AIR_STRIKE: return 'air_strike'
            case SoundAlert.BEAN: return 'bean'
            case SoundAlert.CHEER: return 'cheer'
            case SoundAlert.CLICK_NAVIGATION: return 'click_navigation'
            case SoundAlert.FOLLOW: return 'follow'
            case SoundAlert.GRENADE_1: return 'grenade_1'
            case SoundAlert.GRENADE_2: return 'grenade_2'
            case SoundAlert.GRENADE_3: return 'grenade_3'
            case SoundAlert.JACKPOT: return 'jackpot'
            case SoundAlert.LAUNCH_AIR_STRIKE: return 'launch_air_strike'
            case SoundAlert.MEGA_GRENADE_1: return 'mega_grenade_1'
            case SoundAlert.MEGA_GRENADE_2: return 'mega_grenade_2'
            case SoundAlert.MEGA_GRENADE_3: return 'mega_grenade_3'
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
            case SoundAlert.SPLAT: return 'splat'
            case SoundAlert.SUBSCRIBE: return 'subscribe'
            case _: raise ValueError(f'Unknown SoundAlert value: \"{soundAlert}\"')
