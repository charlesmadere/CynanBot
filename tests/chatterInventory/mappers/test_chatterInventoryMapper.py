import random

import pytest
from frozendict import frozendict

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.chatterInventory.models.chatterItemType import ChatterItemType
from src.chatterInventory.models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from src.chatterInventory.models.itemDetails.bananaItemDetails import BananaItemDetails
from src.chatterInventory.models.itemDetails.grenadeItemDetails import GrenadeItemDetails


class TestChatterInventoryMapper:

    mapper: ChatterInventoryMapperInterface = ChatterInventoryMapper()

    @pytest.mark.asyncio
    async def test_parseAirStrikeItemDetails(self):
        details = AirStrikeItemDetails(
            maxDurationSeconds = 75,
            minDurationSeconds = 55,
            maxTargets = 13,
            minTargets = 8,
        )

        result = await self.mapper.parseAirStrikeItemDetails({
            'maxDurationSeconds': details.maxDurationSeconds,
            'minDurationSeconds': details.minDurationSeconds,
            'maxTargets': details.maxTargets,
            'minTargets': details.minTargets,
        })

        assert isinstance(result, AirStrikeItemDetails)
        assert result == details
        assert result.maxDurationSeconds == details.maxDurationSeconds
        assert result.minDurationSeconds == details.minDurationSeconds
        assert result.maxTargets == details.maxTargets
        assert result.minTargets == details.minTargets

    @pytest.mark.asyncio
    async def test_parseAirStrikeItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseAirStrikeItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseAirStrikeItemDetails_withNone(self):
        result = await self.mapper.parseAirStrikeItemDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBananaItemDetails(self):
        details = BananaItemDetails(
            randomChanceEnabled = True,
            durationSeconds = 60,
        )

        result = await self.mapper.parseBananaItemDetails({
            'randomChanceEnabled': details.randomChanceEnabled,
            'durationSeconds': details.durationSeconds,
        })

        assert isinstance(result, BananaItemDetails)
        assert result == details
        assert result.randomChanceEnabled == details.randomChanceEnabled
        assert result.durationSeconds == details.durationSeconds

    @pytest.mark.asyncio
    async def test_parseBananaItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseBananaItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBananaItemDetails_withNone(self):
        result = await self.mapper.parseBananaItemDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseGrenadeItemDetails(self):
        details = GrenadeItemDetails(
            maxDurationSeconds = 60,
            minDurationSeconds = 30,
        )

        result = await self.mapper.parseGrenadeItemDetails({
            'maxDurationSeconds': details.maxDurationSeconds,
            'minDurationSeconds': details.minDurationSeconds,
        })

        assert isinstance(result, GrenadeItemDetails)
        assert result == details
        assert result.maxDurationSeconds == details.maxDurationSeconds
        assert result.minDurationSeconds == details.minDurationSeconds

    @pytest.mark.asyncio
    async def test_parseGrenadeItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseGrenadeItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseGrenadeItemDetails_withNone(self):
        result = await self.mapper.parseGrenadeItemDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseInventory1(self):
        airStrikes = round(random.uniform(0.01, 1.00) * 100)
        bananas = round(random.uniform(0.01, 1.00) * 100)
        cassetteTapes = round(random.uniform(0.01, 1.00) * 100)
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
            await self.mapper.serializeItemType(ChatterItemType.BANANA): bananas,
            await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE): cassetteTapes,
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == airStrikes
        assert result[ChatterItemType.BANANA] == bananas
        assert result[ChatterItemType.CASSETTE_TAPE] == cassetteTapes
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
        assert result[ChatterItemType.CASSETTE_TAPE] == 0
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
        assert result[ChatterItemType.CASSETTE_TAPE] == 0
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
        cassetteTapes = round(random.uniform(-1.00, -0.01) * 100)
        grenades = round(random.uniform(-1.00, -0.01) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
            await self.mapper.serializeItemType(ChatterItemType.BANANA): bananas,
            await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE): cassetteTapes,
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        # negative numbers should always be normalized to 0
        assert result[ChatterItemType.AIR_STRIKE] == 0
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.CASSETTE_TAPE] == 0
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
    async def test_parseItemType_withCassetteStrings(self):
        result = await self.mapper.parseItemType('casete')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassete')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('casette')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassette')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassettes')
        assert result is ChatterItemType.CASSETTE_TAPE

    @pytest.mark.asyncio
    async def test_parseItemType_withCassetteTapeStrings(self):
        result = await self.mapper.parseItemType('cassette_tape')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassette-tape')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassette tape')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassette_tapes')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassette-tapes')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.parseItemType('cassette tapes')
        assert result is ChatterItemType.CASSETTE_TAPE

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
    async def test_parseItemType_withNade(self):
        result = await self.mapper.parseItemType('nade')
        assert result is ChatterItemType.GRENADE

        result = await self.mapper.parseItemType('nades')
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

        result = await self.mapper.parseItemType('tnt\'s')
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

        result = await self.mapper.requireItemType('bananas')
        assert result is ChatterItemType.BANANA

    @pytest.mark.asyncio
    async def test_requireItemType_withCassetteStrings(self):
        result = await self.mapper.requireItemType('casete')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassete')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('casette')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassette')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassettes')
        assert result is ChatterItemType.CASSETTE_TAPE

    @pytest.mark.asyncio
    async def test_requireItemType_withCassetteTapeStrings(self):
        result = await self.mapper.requireItemType('cassette_tape')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassette-tape')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassette tape')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassette_tapes')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassette-tapes')
        assert result is ChatterItemType.CASSETTE_TAPE

        result = await self.mapper.requireItemType('cassette tapes')
        assert result is ChatterItemType.CASSETTE_TAPE

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

        result = await self.mapper.requireItemType('tnt\'s')
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
        assert len(result) == 1

        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == airStrikes

    @pytest.mark.asyncio
    async def test_serializeInventory2(self):
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.GRENADE: grenades,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == 1

        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == grenades

    @pytest.mark.asyncio
    async def test_serializeInventory3(self):
        airStrikes = round(random.uniform(0.01, 1.00) * 100)
        bananas = round(random.uniform(0.01, 1.00) * 100)
        cassetteTapes = round(random.uniform(0.01, 1.00) * 100)
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
            ChatterItemType.BANANA: bananas,
            ChatterItemType.CASSETTE_TAPE: cassetteTapes,
            ChatterItemType.GRENADE: grenades,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == len(ChatterItemType)

        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == airStrikes
        assert result[await self.mapper.serializeItemType(ChatterItemType.BANANA)] == bananas
        assert result[await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE)] == cassetteTapes
        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == grenades

    @pytest.mark.asyncio
    async def test_serializeInventory_withEmptyDictionary(self):
        result = await self.mapper.serializeInventory(dict())
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializeInventory_withEmptyFrozenDictionary(self):
        result = await self.mapper.serializeInventory(frozendict())
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_serializeInventory_withNegativeNumbers(self):
        airStrikes = round(random.uniform(-1.00, -0.01) * 100)
        bananas = round(random.uniform(-1.00, -0.01) * 100)
        cassetteTapes = round(random.uniform(-1.00, -0.01) * 100)
        grenades = round(random.uniform(-1.00, -0.01) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
            ChatterItemType.BANANA: bananas,
            ChatterItemType.CASSETTE_TAPE: cassetteTapes,
            ChatterItemType.GRENADE: grenades,
        }

        result = await self.mapper.serializeInventory(inventory)

        # negative numbers should always be normalized to 0
        assert len(result) == 0

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
    async def test_serializeItemType_withCassetteTape(self):
        result = await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE)
        assert result == 'cassette_tape'

    @pytest.mark.asyncio
    async def test_serializeItemType_withGrenade(self):
        result = await self.mapper.serializeItemType(ChatterItemType.GRENADE)
        assert result == 'grenade'
