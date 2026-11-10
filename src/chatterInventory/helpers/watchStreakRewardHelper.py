from typing import Final

from .watchStreakRewardHelperInterface import WatchStreakRewardHelperInterface
from ..idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..machine.chatterInventoryMachineInterface import ChatterInventoryMachineInterface
from ..models.requestWatchStreakRewardAction import RequestWatchStreakRewardAction
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class WatchStreakRewardHelper(WatchStreakRewardHelperInterface):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryMachine: ChatterInventoryMachineInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventoryMachine, ChatterInventoryMachineInterface):
            raise TypeError(f'chatterInventoryMachine argument is malformed: \"{chatterInventoryMachine}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryMachine: Final[ChatterInventoryMachineInterface] = chatterInventoryMachine
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber

    async def requestWatchStreakReward(
        self,
        watchStreak: int,
        chatMessage: str | None,
        chatterUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        if not utils.isValidInt(watchStreak):
            raise TypeError(f'watchStreak argument is malformed: \"{watchStreak}\"')
        elif watchStreak < 0 or watchStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'watchStreak argument is malformed: {watchStreak}')
        elif chatMessage is not None and not isinstance(chatMessage, str):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            return False
        elif not await self.__chatterInventorySettings.areWatchStreakRewardsEnabled():
            return False

        actionId = await self.__chatterInventoryIdGenerator.generateActionId()

        self.__chatterInventoryMachine.submitAction(RequestWatchStreakRewardAction(
            watchStreak = watchStreak,
            actionId = actionId,
            chatMessage = chatMessage,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            user = user,
        ))

        self.__timber.log('WatchStreakRewardHelper', f'Submitted request watch streak reward action ({actionId=}) ({watchStreak=}) ({chatterUserId=}) ({twitchChannelId=})')
        return True
