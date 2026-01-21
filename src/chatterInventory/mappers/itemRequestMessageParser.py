import re
from dataclasses import dataclass
from typing import Any, Final, Match, Pattern

from .chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.chatterItemType import ChatterItemType
from ...misc import utils as utils


class ItemRequestMessageParser:

    @dataclass(frozen = True, slots = True)
    class Result:
        itemType: ChatterItemType
        argument: str | None
        originalChatMessage: str

    def __init__(
        self,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
    ):
        if not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')

        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper

        # meant to match: !use grenade, !use airstrike, etc
        self.__useCommandRegEx: Final[Pattern] = re.compile(r'^\s*(?:!\s*use\s+)?((?:[\w_-])+)\s*(.*)$', re.IGNORECASE)

        # meant to match various item type style commands: !airstrike, !grenade, etc
        self.__itemTypeCommandRegEx: Final[Pattern] = re.compile(r'^\s*!\s*([\w_-]+)\s*(.*)$', re.IGNORECASE)

    async def parse(
        self,
        chatMessage: str | Any | None,
    ) -> Result | None:
        if not utils.isValidStr(chatMessage):
            return None

        chatMessage = utils.cleanStr(chatMessage)

        match = self.__useCommandRegEx.fullmatch(chatMessage)
        result = await self.__parseMatch(match = match, chatMessage = chatMessage)
        if result is not None:
            return result

        match = self.__itemTypeCommandRegEx.fullmatch(chatMessage)
        result = await self.__parseMatch(match = match, chatMessage = chatMessage)
        if result is not None:
            return result

        return None

    async def __parseMatch(
        self,
        match: Match[str] | None,
        chatMessage: str,
    ) -> Result | None:
        if match is None:
            return None

        itemType = await self.__chatterInventoryMapper.parseItemType(match.group(1))
        if itemType is None:
            return None

        argument: str | None = None
        if utils.isValidStr(utils.cleanStr(match.group(2))):
            argument = utils.cleanStr(match.group(2))

        return ItemRequestMessageParser.Result(
            itemType = itemType,
            argument = argument,
            originalChatMessage = chatMessage,
        )
