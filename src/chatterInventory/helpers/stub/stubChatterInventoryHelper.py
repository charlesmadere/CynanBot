from typing import Final

from frozendict import frozendict

from ..chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ...models.chatterInventoryData import ChatterInventoryData
from ...models.chatterItemGiveResult import ChatterItemGiveResult
from ...models.chatterItemType import ChatterItemType
from ...models.preparedChatterInventoryData import PreparedChatterInventoryData
from ....misc import utils as utils
from ....twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ....twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class StubChatterInventoryHelper(ChatterInventoryHelperInterface):

    def __init__(
        self,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

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

        chatterUserData = await self.__twitchUserIdsHelper.requireById(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

        twitchChannelData = await self.__twitchUserIdsHelper.requireById(
            userId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        inventory: dict[ChatterItemType, int] = dict()

        for itemType in ChatterItemType:
            inventory[itemType] = 0

        return PreparedChatterInventoryData(
            chatterInventory = ChatterInventoryData(
                inventory = frozendict(inventory),
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            ),
            twitchChannel = twitchChannelData.userLogin,
            chatterUserData = chatterUserData,
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

        chatterUserData = await self.__twitchUserIdsHelper.requireById(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
        )

        twitchChannelData = await self.__twitchUserIdsHelper.requireById(
            userId = twitchChannelId,
            twitchAccessToken = twitchAccessToken,
        )

        inventory: dict[ChatterItemType, int] = dict()

        for itemType in ChatterItemType:
            inventory[itemType] = 0

        return ChatterItemGiveResult(
            chatterInventory = ChatterInventoryData(
                inventory = frozendict(inventory),
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            ),
            givenItem = itemType,
            givenAmount = giveAmount,
            twitchChannel = twitchChannelData.userLogin,
            chatterUserData = chatterUserData,
        )
