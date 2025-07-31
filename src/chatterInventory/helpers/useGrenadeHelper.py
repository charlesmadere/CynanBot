import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from frozenlist import FrozenList

from .useGrenadeHelperInterface import UseGrenadeHelperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.useGrenadeItemAction import UseGrenadeItemAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class UseGrenadeHelper(UseGrenadeHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        sleepTimeSeconds: float = 1,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 0.5 or sleepTimeSeconds > 8:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__sleepTimeSeconds: Final[float] = sleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__actionQueue: Final[SimpleQueue[UseGrenadeItemAction]] = SimpleQueue()

    async def __handleAction(self, action: UseGrenadeItemAction):
        if not isinstance(action, UseGrenadeItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__isEnabled():
            return

        chatterInventory = await self.__chatterInventoryRepository.get(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        if chatterInventory[ChatterItemType.GRENADE] < 1:
            return

        # We're intentionally not decrementing the chatter's grenade count here.
        # Instead, that happens within the TimeoutActionMachine class.

        # TODO
        pass

        # self.__timeoutActionHelper.submitTimeout(TimeoutActionData(
        #     isRandomChanceEnabled = False,
        #     bits = None,
        #     durationSeconds = durationSeconds,
        #     remainingGrenades = chatterInventory[ChatterItemType.GRENADE],
        #     chatMessage = None,
        #     instigatorUserId = action.chatterUserId,
        #     instigatorUserName = instigatorUserName,
        #     moderatorTwitchAccessToken = moderatorTwitchAccessToken,
        #     moderatorUserId = moderatorUserId,
        #     pointRedemptionEventId = None,
        #     pointRedemptionMessage = None,
        #     pointRedemptionRewardId = None,
        #     timeoutTargetUserId = timeoutTargetUserId,
        #     timeoutTargetUserName = timeoutTargetUserName,
        #     twitchChannelId = action.twitchChannelId,
        #     twitchChatMessageId = None,
        #     userTwitchAccessToken = userTwitchAccessToken,
        #     actionType = TimeoutActionType.GRENADE,
        #     streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
        #     user = user,
        # ))

        # TODO
        pass

    async def __isEnabled(self) -> bool:
        if not await self.__chatterInventorySettings.isEnabled():
            return False

        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()
        return ChatterItemType.GRENADE in enabledItemTypes

    def start(self):
        if self.__isStarted:
            self.__timber.log('UseGrenadeHelper', 'Not starting UseGrenadeHelper as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('UseGrenadeHelper', 'Starting UseGrenadeHelper...')
        self.__backgroundTaskHelper.createTask(self.__startActionLoop())

    async def __startActionLoop(self):
        while True:
            actions: FrozenList[UseGrenadeItemAction] = FrozenList()

            try:
                while not self.__actionQueue.empty():
                    action = self.__actionQueue.get_nowait()
                    actions.append(action)
            except queue.Empty as e:
                self.__timber.log('UseGrenadeHelper', f'Encountered queue.Empty when building up actions list (queue size: {self.__actionQueue.qsize()}) (actions size: {len(actions)}): {e}', e, traceback.format_exc())

            actions.freeze()

            for index, action in enumerate(actions):
                try:
                    await self.__handleAction(action)
                except Exception as e:
                    self.__timber.log('UseGrenadeHelper', f'Encountered unknown Exception when looping through actions (queue size: {self.__actionQueue.qsize()}) ({len(actions)=}) ({index=}) ({action=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

    def submitAction(self, action: UseGrenadeItemAction):
        if not isinstance(action, UseGrenadeItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        try:
            self.__actionQueue.put(action, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('UseGrenadeHelper', f'Encountered queue.Full when submitting a new action ({action}) into the action queue (queue size: {self.__actionQueue.qsize()}): {e}', e, traceback.format_exc())
