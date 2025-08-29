import pytest

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.chatterInventory.mappers.itemRequestMessageParser import ItemRequestMessageParser
from src.chatterInventory.models.chatterItemType import ChatterItemType


class TestItemRequestMessageParser:

    chatterInventoryMapper: ChatterInventoryMapperInterface = ChatterInventoryMapper()

    parser = ItemRequestMessageParser(
        chatterInventoryMapper = chatterInventoryMapper,
    )

    @pytest.mark.asyncio
    async def test_parse_withEmptyString(self):
        result = await self.parser.parse('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withNone(self):
        result = await self.parser.parse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withUseCommandAndAirStrikeItemType(self):
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
