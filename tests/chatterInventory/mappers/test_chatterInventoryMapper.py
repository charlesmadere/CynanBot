import random

import pytest
from frozendict import frozendict

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.chatterInventory.models.chatterItemType import ChatterItemType


class TestChatterInventoryMapper:

    mapper: ChatterInventoryMapperInterface = ChatterInventoryMapper()

    @pytest.mark.asyncio
    async def test_parseInventory1(self):
        airStrikes = round(random.uniform(0.01, 1.00) * 100)
        bananas = round(random.uniform(0.01, 1.00) * 100)
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
            await self.mapper.serializeItemType(ChatterItemType.BANANA): bananas,
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == airStrikes
        assert result[ChatterItemType.BANANA] == bananas
        assert result[ChatterItemType.GRENADE] == grenades

    @pytest.mark.asyncio
    async def test_parseInventory2(self):
        airStrikes = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == airStrikes
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.GRENADE] == 0

    @pytest.mark.asyncio
    async def test_parseInventory3(self):
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == 0
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.GRENADE] == grenades

    @pytest.mark.asyncio
    async def test_parseInventory_withEmptyDictionary(self):
        result = await self.mapper.parseInventory(dict())
        assert len(result) == len(ChatterItemType)

        for itemType in ChatterItemType:
            assert result[itemType] == 0

    @pytest.mark.asyncio
    async def test_parseInventory_withEmptyFrozenDictionary(self):
        result = await self.mapper.parseInventory(frozendict())
        assert len(result) == len(ChatterItemType)

        for itemType in ChatterItemType:
            assert result[itemType] == 0

    @pytest.mark.asyncio
    async def test_parseInventory_withNegativeNumbers(self):
        airStrikes = round(random.uniform(-1.00, -0.01) * 100)
        bananas = round(random.uniform(-1.00, -0.01) * 100)
        grenades = round(random.uniform(-1.00, -0.01) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
            await self.mapper.serializeItemType(ChatterItemType.BANANA): bananas,
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        # negative numbers should be normalized to 0
        assert result[ChatterItemType.AIR_STRIKE] == 0
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.GRENADE] == 0

    @pytest.mark.asyncio
    async def test_parseInventory_withNone(self):
        result = await self.mapper.parseInventory(None)
        assert len(result) == len(ChatterItemType)

        for itemType in ChatterItemType:
            assert result[itemType] == 0

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
    async def test_parseItemType_withBanana(self):
        result = await self.mapper.parseItemType('banana')
        assert result is ChatterItemType.BANANA

        result = await self.mapper.parseItemType('bananas')
        assert result is ChatterItemType.BANANA

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
    async def test_parseItemType_withTnt(self):
        result = await self.mapper.parseItemType('tnt')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('tnts')
        assert result is ChatterItemType.AIR_STRIKE

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
    async def test_requireItemType_withBanana(self):
        result = await self.mapper.requireItemType('banana')
        assert result is ChatterItemType.BANANA

        result = await self.mapper.requireItemType('banana')
        assert result is ChatterItemType.BANANA

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
    async def test_requireItemType_withTnt(self):
        result = await self.mapper.requireItemType('tnt')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('tnts')
        assert result is ChatterItemType.AIR_STRIKE

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
    async def test_serializeInventory1(self):
        airStrikes = round(random.uniform(0.01, 1.00)  * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == len(ChatterItemType)

        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == airStrikes
        assert result[await self.mapper.serializeItemType(ChatterItemType.BANANA)] == 0
        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == 0

    @pytest.mark.asyncio
    async def test_serializeInventory2(self):
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.GRENADE: grenades,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == len(ChatterItemType)

        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == 0
        assert result[await self.mapper.serializeItemType(ChatterItemType.BANANA)] == 0
        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == grenades

    @pytest.mark.asyncio
    async def test_serializeInventory3(self):
        airStrikes = round(random.uniform(0.01, 1.00) * 100)
        bananas = round(random.uniform(0.01, 1.00) * 100)
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
            ChatterItemType.BANANA: bananas,
            ChatterItemType.GRENADE: grenades,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == len(ChatterItemType)

        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == airStrikes
        assert result[await self.mapper.serializeItemType(ChatterItemType.BANANA)] == bananas
        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == grenades

    @pytest.mark.asyncio
    async def test_serializeInventory_withEmptyDictionary(self):
        result = await self.mapper.serializeInventory(dict())
        assert len(result) == len(ChatterItemType)

        for itemType in ChatterItemType:
            itemTypeString = await self.mapper.serializeItemType(itemType)
            assert result[itemTypeString] == 0

    @pytest.mark.asyncio
    async def test_serializeInventory_withEmptyFrozenDictionary(self):
        result = await self.mapper.serializeInventory(frozendict())
        assert len(result) == len(ChatterItemType)

        for itemType in ChatterItemType:
            itemTypeString = await self.mapper.serializeItemType(itemType)
            assert result[itemTypeString] == 0

    @pytest.mark.asyncio
    async def test_serializeInventory_withNegativeNumbers(self):
        airStrikes = round(random.uniform(-1.00, -0.01) * 100)
        bananas = round(random.uniform(-1.00, -0.01) * 100)
        grenades = round(random.uniform(-1.00, -0.01) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
            ChatterItemType.BANANA: bananas,
            ChatterItemType.GRENADE: grenades,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == len(ChatterItemType)

        # negative numbers should be normalized to 0
        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == 0
        assert result[await self.mapper.serializeItemType(ChatterItemType.BANANA)] == 0
        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == 0

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
    async def test_serializeItemType_withBanana(self):
        result = await self.mapper.serializeItemType(ChatterItemType.BANANA)
        assert result == 'banana'

    @pytest.mark.asyncio
    async def test_serializeItemType_withGrenade(self):
        result = await self.mapper.serializeItemType(ChatterItemType.GRENADE)
        assert result == 'grenade'
