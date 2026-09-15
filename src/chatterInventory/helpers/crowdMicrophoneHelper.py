from datetime import timedelta
from typing import Final

from .crowdMicrophoneHelperInterface import CrowdMicrophoneHelperInterface
from ..exceptions import CrowdMicrophoneAlreadyStartedException
from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class CrowdMicrophoneHelper(CrowdMicrophoneHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        extraTimeBuffer: timedelta = timedelta(seconds = 3),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(extraTimeBuffer, timedelta):
            raise TypeError(f'extraTimeBuffer argument is malformed: \"{extraTimeBuffer}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__extraTimeBuffer: Final[timedelta] = extraTimeBuffer

        self.__crowdMicrophones: Final[dict[str, CrowdMicrophoneStatus | None]] = dict()

    async def get(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentCrowdMicrophone = self.__crowdMicrophones.get(twitchChannelId, None)
        if currentCrowdMicrophone is None:
            return None

        now = self.__timeZoneRepository.getNow()
        if now < currentCrowdMicrophone.endTime:
            return currentCrowdMicrophone

        self.__crowdMicrophones.pop(twitchChannelId, None)
        return None

    async def start(
        self,
        durationSeconds: int,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getShortMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentCrowdMicrophone = await self.get(
            twitchChannelId = twitchChannelId,
        )

        if currentCrowdMicrophone is not None:
            raise CrowdMicrophoneAlreadyStartedException(
                currentCrowdMicrophone = currentCrowdMicrophone,
            )

        now = self.__timeZoneRepository.getNow()
        endTime = now + timedelta(seconds = durationSeconds) + self.__extraTimeBuffer

        newCrowdMicrophone = CrowdMicrophoneStatus(
            endTime = endTime,
            totalDurationSeconds = durationSeconds,
            twitchChannelId = twitchChannelId,
        )

        self.__timber.log('CrowdMicrophoneHelper', f'Starting new crowd microphone ({newCrowdMicrophone=})')
        self.__crowdMicrophones[twitchChannelId] = newCrowdMicrophone
        return newCrowdMicrophone
