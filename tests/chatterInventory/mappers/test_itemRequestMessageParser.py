from typing import Final

import pytest

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.chatterInventory.mappers.itemRequestMessageParser import ItemRequestMessageParser
from src.chatterInventory.models.chatterItemType import ChatterItemType


class TestItemRequestMessageParser:

    chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = ChatterInventoryMapper()

    parser: Final[ItemRequestMessageParser] = ItemRequestMessageParser(
        chatterInventoryMapper = chatterInventoryMapper,
    )

    @pytest.mark.asyncio
    async def test_parse_withAirStrikeCommand(self):
        result = await self.parser.parse('!air_strike')
        assert result is not None
        assert result.itemType is ChatterItemType.AIR_STRIKE
        assert result.argument is None
        assert result.originalChatMessage == '!air_strike'

        result = await self.parser.parse('!air-strike')
        assert result is not None
        assert result.itemType is ChatterItemType.AIR_STRIKE
        assert result.argument is None
        assert result.originalChatMessage == '!air-strike'

    @pytest.mark.asyncio
    async def test_parse_withBananaCommand(self):
        result = await self.parser.parse('!banana')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument is None
        assert result.originalChatMessage == '!banana'

        result = await self.parser.parse('!bananas')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument is None
        assert result.originalChatMessage == '!bananas'

    @pytest.mark.asyncio
    async def test_parse_withBananaCommandAndArgument(self):
        result = await self.parser.parse('!banana @stashiocat')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument == '@stashiocat'
        assert result.originalChatMessage == '!banana @stashiocat'

        result = await self.parser.parse('!bananas   @the_purple_falcon    \n')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument == '@the_purple_falcon'
        assert result.originalChatMessage == '!bananas @the_purple_falcon'

        result = await self.parser.parse('!bananas   the_purple_falcon  ')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument == 'the_purple_falcon'
        assert result.originalChatMessage == '!bananas the_purple_falcon'

    @pytest.mark.asyncio
    async def test_parse_withCassetteCommand(self):
        result = await self.parser.parse('!cassette')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!cassette'

    @pytest.mark.asyncio
    async def test_parse_withCassetteTapeCommand(self):
        result = await self.parser.parse('!cassette-tape')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!cassette-tape'

        result = await self.parser.parse('!cassette_tape')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!cassette_tape'

        result = await self.parser.parse('!cassettetape')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!cassettetape'

    @pytest.mark.asyncio
    async def test_parse_withEmptyString(self):
        result = await self.parser.parse('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withGrenadeCommand(self):
        result = await self.parser.parse('!grenade')
        assert result is not None
        assert result.itemType is ChatterItemType.GRENADE
        assert result.argument is None
        assert result.originalChatMessage == '!grenade'

        result = await self.parser.parse('!grenades')
        assert result is not None
        assert result.itemType is ChatterItemType.GRENADE
        assert result.argument is None
        assert result.originalChatMessage == '!grenades'

        result = await self.parser.parse('!nade')
        assert result is not None
        assert result.itemType is ChatterItemType.GRENADE
        assert result.argument is None
        assert result.originalChatMessage == '!nade'

        result = await self.parser.parse('!nades')
        assert result is not None
        assert result.itemType is ChatterItemType.GRENADE
        assert result.argument is None
        assert result.originalChatMessage == '!nades'

    @pytest.mark.asyncio
    async def test_parse_withNone(self):
        result = await self.parser.parse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withUseCommandAndAirStrikeItemType(self):
        result = await self.parser.parse('!use air_strike')
        assert result is not None
        assert result.itemType is ChatterItemType.AIR_STRIKE
        assert result.argument is None
        assert result.originalChatMessage == '!use air_strike'

        result = await self.parser.parse('!use air-strike')
        assert result is not None
        assert result.itemType is ChatterItemType.AIR_STRIKE
        assert result.argument is None
        assert result.originalChatMessage == '!use air-strike'

        result = await self.parser.parse('!use airstrike')
        assert result is not None
        assert result.itemType is ChatterItemType.AIR_STRIKE
        assert result.argument is None
        assert result.originalChatMessage == '!use airstrike'

    @pytest.mark.asyncio
    async def test_parse_withUseCommandAndBananaItemType(self):
        result = await self.parser.parse('!use banana')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument is None
        assert result.originalChatMessage == '!use banana'

    @pytest.mark.asyncio
    async def test_parse_withUseCommandAndBananaItemTypeAndArgument(self):
        result = await self.parser.parse('!use banana @eddie')
        assert result is not None
        assert result.itemType is ChatterItemType.BANANA
        assert result.argument == '@eddie'
        assert result.originalChatMessage == '!use banana @eddie'

    @pytest.mark.asyncio
    async def test_parse_withUseCommandAndCassetteTapeItemType(self):
        result = await self.parser.parse('!use cassette_tape')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!use cassette_tape'

        result = await self.parser.parse('!use cassette-tape')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!use cassette-tape'

        result = await self.parser.parse('!use cassettetape')
        assert result is not None
        assert result.itemType is ChatterItemType.CASSETTE_TAPE
        assert result.argument is None
        assert result.originalChatMessage == '!use cassettetape'

    @pytest.mark.asyncio
    async def test_parse_withUseCommandAndGrenadeItemType(self):
        result = await self.parser.parse('!use grenade')
        assert result is not None
        assert result.itemType is ChatterItemType.GRENADE
        assert result.argument is None
        assert result.originalChatMessage == '!use grenade'

    @pytest.mark.asyncio
    async def test_parse_withUseCommandButNoItemType(self):
        result = await self.parser.parse('!use')
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withWhitespaceString(self):
        result = await self.parser.parse(' ')
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, ItemRequestMessageParser)
