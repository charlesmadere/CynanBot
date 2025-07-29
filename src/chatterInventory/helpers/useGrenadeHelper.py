from typing import Final

from .useGrenadeHelperInterface import UseGrenadeHelperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.useGrenadeItemAction import UseGrenadeItemAction
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class UseGrenadeHelper(UseGrenadeHelperInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timeoutActionHelper: TimeoutActionHelperInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timeoutActionHelper, TimeoutActionHelperInterface):
            raise TypeError(f'timeoutActionHelper argument is malformed: \"{timeoutActionHelper}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timeoutActionHelper: Final[TimeoutActionHelperInterface] = timeoutActionHelper
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __isEnabled(self) -> bool:
        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()
        return ChatterItemType.GRENADE in enabledItemTypes

    async def use(self, action: UseGrenadeItemAction):
        if not isinstance(action, UseGrenadeItemAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not await self.__isEnabled():
            return

        chatterInventory = await self.__chatterInventoryRepository.get(
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        if chatterInventory.inventory[ChatterItemType.GRENADE] < 1:
            return

        chatterInventory = await self.__chatterInventoryRepository.update(
            itemType = ChatterItemType.GRENADE,
            changeAmount = -1,
            chatterUserId = action.chatterUserId,
            twitchChannelId = action.twitchChannelId,
        )

        # TODO
        #
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
