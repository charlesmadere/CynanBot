import pytest

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.chatterInventory.models.chatterItemType import ChatterItemType


class TestChatterInventoryMapper:

    mapper: ChatterInventoryMapperInterface = ChatterInventoryMapper()

    @pytest.mark.asyncio
    async def test_parseItemType_withAirStrike(self):
        result = await self.mapper.parseItemType('air_strike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('air_strikes')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('air strike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('air strikes')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('air-strike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('air-strikes')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('airstrike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('airstrikes')
        assert result is ChatterItemType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_parseItemType_withEmptyString(self):
        result = await self.mapper.parseItemType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseItemType_withGrenade(self):
        result = await self.mapper.parseItemType('grenade')
        assert result is ChatterItemType.GRENADE

        result = await self.mapper.parseItemType('grenades')
        assert result is ChatterItemType.GRENADE

    @pytest.mark.asyncio
    async def test_parseItemType_withNone(self):
        result = await self.mapper.parseItemType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseItemType_withWhitespaceString(self):
        result = await self.mapper.parseItemType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireItemType_withAirStrike(self):
        result = await self.mapper.requireItemType('air_strike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('air_strikes')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('air strike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('air strikes')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('air-strike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('air-strikes')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('airstrike')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('airstrikes')
        assert result is ChatterItemType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_requireItemType_withEmptyString(self):
        result: ChatterItemType | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireItemType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireItemType_withGrenade(self):
        result = await self.mapper.requireItemType('grenade')
        assert result is ChatterItemType.GRENADE

        result = await self.mapper.requireItemType('grenades')
        assert result is ChatterItemType.GRENADE

    @pytest.mark.asyncio
    async def test_requireItemType_withNone(self):
        result: ChatterItemType | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireItemType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireItemType_withWhitespaceString(self):
        result: ChatterItemType | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireItemType(' ')

        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, ChatterInventoryMapper)
        assert isinstance(self.mapper, ChatterInventoryMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeItemType_withAll(self):
        results: set[str] = set()

        for itemType in ChatterItemType:
            results.add(await self.mapper.serializeItemType(itemType))

        assert len(results) == len(ChatterItemType)

    @pytest.mark.asyncio
    async def test_serializeItemType_withAirStrike(self):
        result = await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)
        assert result == 'air_strike'

    @pytest.mark.asyncio
    async def test_serializeItemType_withGrenade(self):
        result = await self.mapper.serializeItemType(ChatterItemType.GRENADE)
        assert result == 'grenade'
