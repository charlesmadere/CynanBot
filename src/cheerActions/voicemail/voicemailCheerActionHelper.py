from typing import Final

from frozendict import frozendict

from .voicemailCheerAction import VoicemailCheerAction
from .voicemailCheerActionHelperInterface import VoicemailCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from ...chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ...chatterInventory.models.chatterItemType import ChatterItemType
from ...chatterInventory.models.useChatterItemRequest import UseChatterItemRequest
from ...chatterInventory.models.useChatterItemResult import UseChatterItemResult
from ...twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from ...users.userInterface import UserInterface


class VoicemailCheerActionHelper(VoicemailCheerActionHelperInterface):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        useChatterItemHelper: UseChatterItemHelperInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__useChatterItemHelper: Final[UseChatterItemHelperInterface] = useChatterItemHelper

    async def handleVoicemailCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        action = actions.get(bits, None)

        if not isinstance(action, VoicemailCheerAction) or not action.isEnabled:
            return False

        result = await self.__useChatterItemHelper.useItem(UseChatterItemRequest(
            ignoreInventory = True,
            itemType = ChatterItemType.CASSETTE_TAPE,
            chatMessage = await self.__twitchMessageStringUtils.removeCheerStrings(message),
            chatterUserId = cheerUserId,
            requestId = await self.__chatterInventoryIdGenerator.generateRequestId(),
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            user = user,
        ))

        return result is UseChatterItemResult.OK
