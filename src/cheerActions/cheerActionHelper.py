import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .cheerActionHelperInterface import CheerActionHelperInterface
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .crowdControl.crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from .itemUse.itemUseCheerActionHelperInterface import ItemUseCheerActionHelperInterface
from .soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from .tts.ttsCheerActionHelperInterface import TtsCheerActionHelperInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class CheerActionHelper(CheerActionHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        crowdControlCheerActionHelper: CrowdControlCheerActionHelperInterface | None,
        itemUseCheerActionHelper: ItemUseCheerActionHelperInterface | None,
        soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None,
        timber: TimberInterface,
        ttsCheerActionHelper: TtsCheerActionHelperInterface | None,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        queueSleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif crowdControlCheerActionHelper is not None and not isinstance(crowdControlCheerActionHelper, CrowdControlCheerActionHelperInterface):
            raise TypeError(f'crowdControlCheerActionHelper argument is malformed: \"{crowdControlCheerActionHelper}\"')
        elif itemUseCheerActionHelper is not None and not isinstance(itemUseCheerActionHelper, ItemUseCheerActionHelperInterface):
            raise TypeError(f'itemUseCheerActionHelper argument is malformed: \"{itemUseCheerActionHelper}\"')
        elif soundAlertCheerActionHelper is not None and not isinstance(soundAlertCheerActionHelper, SoundAlertCheerActionHelperInterface):
            raise TypeError(f'soundAlertCheerActionHelper argument is malformed: \"{soundAlertCheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsCheerActionHelper is not None and not isinstance(ttsCheerActionHelper, TtsCheerActionHelperInterface):
            raise TypeError(f'ttsCheerActionHelper argument is malformed: \"{ttsCheerActionHelper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 0.125 or queueSleepTimeSeconds > 3:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 3:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__crowdControlCheerActionHelper: Final[CrowdControlCheerActionHelperInterface | None] = crowdControlCheerActionHelper
        self.__itemUseCheerActionHelper: Final[ItemUseCheerActionHelperInterface | None] = itemUseCheerActionHelper
        self.__soundAlertCheerActionHelper: Final[SoundAlertCheerActionHelperInterface | None] = soundAlertCheerActionHelper
        self.__timber: Final[TimberInterface] = timber
        self.__ttsCheerActionHelper: Final[TtsCheerActionHelperInterface | None] = ttsCheerActionHelper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__queueSleepTimeSeconds: Final[float] = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__cheerQueue: Final[SimpleQueue[CheerActionHelperInterface.CheerInfo]] = SimpleQueue()

    async def handleCheer(self, cheerInfo: CheerActionHelperInterface.CheerInfo) -> bool:
        if not isinstance(cheerInfo, CheerActionHelperInterface.CheerInfo):
            raise TypeError(f'cheerInfo argument is malformed: \"{cheerInfo}\"')

        if not cheerInfo.twitchUser.areCheerActionsEnabled:
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = cheerInfo.twitchChannelId,
        )

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = userTwitchAccessToken,
        )

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(
            twitchChannelId = moderatorUserId,
        )

        actions = await self.__cheerActionsRepository.getActions(
            twitchChannelId = cheerInfo.twitchChannelId,
        )

        if actions is None or len(actions) == 0:
            return False

        elif self.__crowdControlCheerActionHelper is not None and await self.__crowdControlCheerActionHelper.handleCrowdControlCheerAction(
            actions = actions,
            bits = cheerInfo.bits,
            cheerUserId = cheerInfo.cheerUserId,
            cheerUserName = cheerInfo.cheerUserName,
            message = cheerInfo.message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = cheerInfo.twitchChannelId,
            twitchChatMessageId = cheerInfo.twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = cheerInfo.twitchUser,
        ):
            return True

        elif self.__itemUseCheerActionHelper is not None and await self.__itemUseCheerActionHelper.handleItemUseCheerAction(
            actions = actions,
            bits = cheerInfo.bits,
            cheerUserId = cheerInfo.cheerUserId,
            cheerUserName = cheerInfo.cheerUserName,
            message = cheerInfo.message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = cheerInfo.twitchChannelId,
            twitchChatMessageId = cheerInfo.twitchChatMessageId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = cheerInfo.twitchUser,
        ):
            return True

        elif self.__soundAlertCheerActionHelper is not None and await self.__soundAlertCheerActionHelper.handleSoundAlertCheerAction(
            actions = actions,
            bits = cheerInfo.bits,
            cheerUserId = cheerInfo.cheerUserId,
            cheerUserName = cheerInfo.cheerUserName,
            message = cheerInfo.message,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            twitchChannelId = cheerInfo.twitchChannelId,
            userTwitchAccessToken = userTwitchAccessToken,
            user = cheerInfo.twitchUser,
        ):
            return True

        elif self.__ttsCheerActionHelper is not None and await self.__ttsCheerActionHelper.handleTtsCheerAction(
            actions = actions,
            bits = cheerInfo.bits,
            cheerUserId = cheerInfo.cheerUserId,
            cheerUserName = cheerInfo.cheerUserName,
            message = cheerInfo.message,
            twitchChannelId = cheerInfo.twitchChannelId,
            twitchUser = cheerInfo.twitchUser,
        ):
            return True

        else:
            return False

    def start(self):
        if self.__isStarted:
            self.__timber.log('CheerActionHelper', 'Not starting CheerActionHelper as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CheerActionHelper', 'Starting CheerActionHelper...')
        self.__backgroundTaskHelper.createTask(self.__startLoop())

    async def __startLoop(self):
        while True:
            cheers: FrozenList[CheerActionHelperInterface.CheerInfo] = FrozenList()

            try:
                while not self.__cheerQueue.empty():
                    cheers.append(self.__cheerQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('TriviaGameMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__cheerQueue.qsize()}) ({len(cheers)=}) ({cheers=}): {e}', e, traceback.format_exc())

            cheers.freeze()

            for index, cheerInfo in enumerate(cheers):
                try:
                    await self.handleCheer(
                        cheerInfo = cheerInfo,
                    )
                except Exception as e:
                    self.__timber.log('CheerActionHelper', f'Encountered unknown Exception when looping through events (queue size: {self.__cheerQueue.qsize()}) ({len(cheers)=}) ({index=}) ({cheerInfo=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__queueSleepTimeSeconds)

    def submitCheer(self, cheerInfo: CheerActionHelperInterface.CheerInfo):
        if not isinstance(cheerInfo, CheerActionHelperInterface.CheerInfo):
            raise TypeError(f'cheerInfo argument is malformed: \"{cheerInfo}\"')

        try:
            self.__cheerQueue.put(cheerInfo, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('CheerActionHelper', f'Encountered queue.Full when submitting a new cheer ({cheerInfo}) into the queue (queue size: {self.__cheerQueue.qsize()}): {e}', e, traceback.format_exc())
