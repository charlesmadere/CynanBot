import locale
from typing import Final

from frozendict import frozendict

from .itemUseCheerAction import ItemUseCheerAction
from .itemUseCheerActionHelperInterface import ItemUseCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ...chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from ...chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ...chatterInventory.models.useChatterItemRequest import UseChatterItemRequest
from ...chatterInventory.models.useChatterItemResult import UseChatterItemResult
from ...chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...users.userInterface import UserInterface


class ItemUseCheerActionHelper(ItemUseCheerActionHelperInterface):

    def __init__(
        self,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        useChatterItemHelper: UseChatterItemHelperInterface,
    ):
        if not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')

        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__useChatterItemHelper: Final[UseChatterItemHelperInterface] = useChatterItemHelper

    async def __awardItem(
        self,
        action: ItemUseCheerAction,
        cheerUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
    ):
        result = await self.__chatterInventoryHelper.give(
            itemType = action.itemType,
            giveAmount = 1,
            chatterUserId = cheerUserId,
            twitchChannelId = twitchChannelId,
        )

        newAmount = result[action.itemType]
        newAmountString = locale.format_string("%d", newAmount, grouping = True)

        pluralizedName: str

        if newAmount == 1:
            pluralizedName = action.itemType.humanName
        else:
            pluralizedName = action.itemType.pluralHumanName

        hypeEmote = await self.__trollmojiHelper.getHypeEmoteOrBackup()

        self.__twitchChatMessenger.send(
            text = f'{hypeEmote} You got a {action.itemType.humanName}! You now have {newAmountString} {pluralizedName}',
            twitchChannelId = twitchChannelId,
            replyMessageId = twitchChatMessageId,
        )

    async def handleItemUseCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, ItemUseCheerAction) or not action.isEnabled:
            return False

        elif not await self.__chatterInventorySettings.isEnabled():
            return False

        result = await self.__useChatterItemHelper.useItem(UseChatterItemRequest(
            ignoreInventory = True,
            itemType = action.itemType,
            chatMessage = message,
            chatterUserId = cheerUserId,
            requestId = await self.__chatterInventoryIdGenerator.generateRequestId(),
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            user = user,
        ))

        return result is UseChatterItemResult.OK
