import traceback
from datetime import timedelta
from typing import Final

from .crowdMicrophoneHelperInterface import CrowdMicrophoneHelperInterface
from ..exceptions import CrowdMicrophoneAlreadyStartedException
from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus
from ..models.useChatterItemAction import UseChatterItemAction
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.compositeTtsManagerInterface import CompositeTtsManagerInterface


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
        self.__associatedTtsManagers: Final[dict[str, list[CompositeTtsManagerInterface] | None]] = dict()

    async def addAssociatedTtsManager(
        self,
        compositeTtsManager: CompositeTtsManagerInterface,
        twitchChannelId: str,
    ):
        if not isinstance(compositeTtsManager, CompositeTtsManagerInterface):
            raise TypeError(f'compositeTtsManager argument is malformed: \"{compositeTtsManager}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        associatedTtsManagers = self.__associatedTtsManagers.get(twitchChannelId, None)

        if associatedTtsManagers is None:
            associatedTtsManagers = list()
            self.__associatedTtsManagers[twitchChannelId] = associatedTtsManagers

        associatedTtsManagers.append(compositeTtsManager)

    async def getAllDeadMicrophones(self) -> frozenset[CrowdMicrophoneStatus]:
        allDeadMicrophones: set[CrowdMicrophoneStatus] = set()
        now = self.__timeZoneRepository.getNow()

        for microphone in self.__crowdMicrophones.values():
            if microphone is None:
                continue
            elif now > microphone.endTime:
                allDeadMicrophones.add(microphone)

        return frozenset(allDeadMicrophones)

    async def getMicrophone(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return self.__crowdMicrophones.get(twitchChannelId, None)

    async def startMicrophone(
        self,
        durationSeconds: int,
        originatingAction: UseChatterItemAction,
    ) -> CrowdMicrophoneStatus:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getShortMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not isinstance(originatingAction, UseChatterItemAction):
            raise TypeError(f'originatingAction argument is malformed: \"{originatingAction}\"')

        currentMicrophone = await self.getMicrophone(
            twitchChannelId = originatingAction.twitchChannelId,
        )

        if currentMicrophone is not None:
            raise CrowdMicrophoneAlreadyStartedException(
                currentMicrophone= currentMicrophone,
            )

        now = self.__timeZoneRepository.getNow()
        endTime = now + timedelta(seconds = durationSeconds) + self.__extraTimeBuffer

        newCrowdMicrophone = CrowdMicrophoneStatus(
            endTime = endTime,
            totalDurationSeconds = durationSeconds,
            twitchChannelId = originatingAction.twitchChannelId,
            originatingAction = originatingAction,
        )

        self.__crowdMicrophones[newCrowdMicrophone.twitchChannelId] = newCrowdMicrophone
        self.__timber.log('CrowdMicrophoneHelper', f'Starting new crowd microphone ({newCrowdMicrophone=})')
        return newCrowdMicrophone

    async def __stopAllAssociatedTtsManagers(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        associatedTtsManagers = self.__associatedTtsManagers.pop(twitchChannelId, None)

        if associatedTtsManagers is None or len(associatedTtsManagers) == 0:
            self.__timber.log('CrowdMicrophoneHelper', f'No TTS Manager is available to be stopped ({associatedTtsManagers=}) ({twitchChannelId=})')
            return

        stopped = 0
        errors = 0

        for index, ttsManager in enumerate(associatedTtsManagers):
            if not ttsManager.isLoadingOrPlaying:
                continue

            try:
                await ttsManager.stopTtsEvent()
                stopped += 1
            except Exception as e:
                self.__timber.log('CrowdMicrophoneHelper', f'Encountered exception when trying to stop TTS Manager ({index=}) ({ttsManager=}) ({twitchChannelId=})', e, traceback.format_exc())
                errors += 1

        associatedTtsManagers.clear()
        self.__timber.log('CrowdMicrophoneHelper', f'Finished stopping all TTS Managers ({errors=}) ({stopped=}) ({twitchChannelId=})')

    async def stopMicrophone(
        self,
        twitchChannelId: str,
    ) -> CrowdMicrophoneStatus | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        removedMicrophone = self.__crowdMicrophones.pop(twitchChannelId, None)
        await self.__stopAllAssociatedTtsManagers(twitchChannelId = twitchChannelId)
        self.__timber.log('CrowdMicrophoneHelper', f'Removed crowd microphone ({removedMicrophone=}) ({twitchChannelId=})')
        return removedMicrophone
