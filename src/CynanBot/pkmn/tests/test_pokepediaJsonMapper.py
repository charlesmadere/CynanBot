import pytest

from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from CynanBot.pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from CynanBot.pkmn.pokepediaJsonMapperInterface import \
    PokepediaJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestPokepediaJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: PokepediaJsonMapperInterface = PokepediaJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_withNegative1(self):
        result = await self.jsonMapper.parseBerryFlavor(-1)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_withNone(self):
        result = await self.jsonMapper.parseBerryFlavor(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with1(self):
        result = await self.jsonMapper.parseBerryFlavor(1)
        assert result is PokepediaBerryFlavor.SPICY

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with2(self):
        result = await self.jsonMapper.parseBerryFlavor(2)
        assert result is PokepediaBerryFlavor.DRY

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with3(self):
        result = await self.jsonMapper.parseBerryFlavor(3)
        assert result is PokepediaBerryFlavor.SWEET

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with4(self):
        result = await self.jsonMapper.parseBerryFlavor(4)
        assert result is PokepediaBerryFlavor.BITTER

    @pytest.mark.asyncio
    async def test_parseBerryFlavor_with5(self):
        result = await self.jsonMapper.parseBerryFlavor(5)
        assert result is PokepediaBerryFlavor.SOUR
