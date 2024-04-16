import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert


class SoundAlertRedemption():

    def __init__(
        self,
        soundAlert: SoundAlert,
        rewardId: str
    ):
        if not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')
        elif not utils.isValidStr(rewardId):
            raise TypeError(f'rewardId argument is malformed: \"{rewardId}\"')

        self.__soundAlert: SoundAlert = soundAlert
        self.__rewardId: str = rewardId

    def getRewardId(self) -> str:
        return self.__rewardId

    def getSoundAlert(self) -> SoundAlert:
        return self.__soundAlert
