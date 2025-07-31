from typing import Final

from frozendict import frozendict

from .chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemGiveResult import ChatterItemGiveResult
from ..models.chatterItemType import ChatterItemType
from ..models.preparedChatterInventoryData import PreparedChatterInventoryData
from ..repositories.chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class ChatterInventoryHelper(ChatterInventoryHelperInterface):

    def __init__(
        self,
        chatterInventoryRepository: ChatterInventoryRepositoryInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(chatterInventoryRepository, ChatterInventoryRepositoryInterface):
            raise TypeError(f'chatterInventoryRepository argument is malformed: \"{chatterInventoryRepository}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__chatterInventoryRepository: Final[ChatterInventoryRepositoryInterface] = chatterInventoryRepository
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> PreparedChatterInventoryData:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        chatterUserName = await self.__userIdsRepository.requireUserName(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

        twitchChannel = await self.__userIdsRepository.requireUserName(
            userId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        if not await self.__chatterInventorySettings.isEnabled():
            return PreparedChatterInventoryData(
                chatterInventory = ChatterInventoryData(
                    inventory = frozendict(),
                    chatterUserId = chatterUserId,
                    twitchChannelId = twitchChannelId,
                ),
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
            )

        chatterInventory = await self.__chatterInventoryRepository.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        return PreparedChatterInventoryData(
            chatterInventory = chatterInventory,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
        )

    async def give(
        self,
        itemType: ChatterItemType,
        giveAmount: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterItemGiveResult:
        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')
        elif not utils.isValidInt(giveAmount):
            raise TypeError(f'giveAmount argument is malformed: \"{giveAmount}\"')
        elif giveAmount < utils.getIntMinSafeSize() or giveAmount > utils.getIntMaxSafeSize():
            raise ValueError(f'giveAmount argument is out of bounds: {giveAmount}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
            twitchChannelId = twitchChannelId,
        )

        chatterUserName = await self.__userIdsRepository.requireUserName(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

        twitchChannel = await self.__userIdsRepository.requireUserName(
            userId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        if not await self.__chatterInventorySettings.isEnabled():
            return ChatterItemGiveResult(
                chatterInventory = ChatterInventoryData(
                    inventory = frozendict(),
                    chatterUserId = chatterUserId,
                    twitchChannelId = twitchChannelId,
                ),
                givenItem = itemType,
                givenAmount = giveAmount,
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
            )

        chatterInventory = await self.__chatterInventoryRepository.update(
            itemType = itemType,
            changeAmount = giveAmount,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        return ChatterItemGiveResult(
            chatterInventory = chatterInventory,
            givenItem = itemType,
            givenAmount = giveAmount,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
        )
