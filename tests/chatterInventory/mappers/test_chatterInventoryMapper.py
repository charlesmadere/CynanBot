import random
from typing import Final

import pytest
from frozendict import frozendict

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.chatterInventory.models.chatterItemType import ChatterItemType
from src.chatterInventory.models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from src.chatterInventory.models.itemDetails.animalPetItemDetails import AnimalPetItemDetails
from src.chatterInventory.models.itemDetails.bananaItemDetails import BananaItemDetails
from src.chatterInventory.models.itemDetails.gashaponItemDetails import GashaponItemDetails
from src.chatterInventory.models.itemDetails.gashaponItemPullRate import GashaponItemPullRate
from src.chatterInventory.models.itemDetails.grenadeItemDetails import GrenadeItemDetails
from src.chatterInventory.models.itemDetails.tm36ItemDetails import Tm36ItemDetails
from src.chatterInventory.models.itemDetails.voreItemDetails import VoreItemDetails


class TestChatterInventoryMapper:

    mapper: Final[ChatterInventoryMapperInterface] = ChatterInventoryMapper()

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
    async def test_parseAnimalPetItemDetails(self):
        details = AnimalPetItemDetails(
            soundDirectory = 'sounds/animalPets',
        )

        result = await self.mapper.parseAnimalPetItemDetails({
            'soundDirectory': details.soundDirectory,
        })

        assert isinstance(result, AnimalPetItemDetails)
        assert result == details
        assert result.soundDirectory == details.soundDirectory

    @pytest.mark.asyncio
    async def test_parseAnimalPetItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseAnimalPetItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseAnimalPetItemDetails_withNone(self):
        result = await self.mapper.parseAnimalPetItemDetails(None)
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
    async def test_parseGashaponItemDetails(self):
        airStrikePullRate = GashaponItemPullRate(
            pullRate = 0.25,
            iterations = 2,
            maximumPullAmount = 2,
            minimumPullAmount = 0,
        )

        animalPetPullRate = GashaponItemPullRate(
            pullRate = 0.6,
            iterations = 2,
            maximumPullAmount = 2,
            minimumPullAmount = 1,
        )

        bananaPullRate = GashaponItemPullRate(
            pullRate = 0.5,
            iterations = 2,
            maximumPullAmount = 2,
            minimumPullAmount = 0,
        )

        cassetteTapePullRate = GashaponItemPullRate(
            pullRate = 0.2,
            iterations = 1,
            maximumPullAmount = 1,
            minimumPullAmount = 0,
        )

        gashaponPullRate = GashaponItemPullRate(
            pullRate = 0.01,
            iterations = 1,
            maximumPullAmount = 1,
            minimumPullAmount = 1,
        )

        grenadePullRate = GashaponItemPullRate(
            pullRate = 0.75,
            iterations = 2,
            maximumPullAmount = 2,
            minimumPullAmount = 1,
        )

        tm36PullRate = GashaponItemPullRate(
            pullRate = 0.2,
            iterations = 1,
            maximumPullAmount = 1,
            minimumPullAmount = 0,
        )

        vorePullRate = GashaponItemPullRate(
            pullRate = 0.0,
            iterations = 0,
            maximumPullAmount = 0,
            minimumPullAmount = 0,
        )

        gashaponItemDetails = GashaponItemDetails(
            pullRates = frozendict({
                ChatterItemType.AIR_STRIKE: airStrikePullRate,
                ChatterItemType.ANIMAL_PET: animalPetPullRate,
                ChatterItemType.BANANA: bananaPullRate,
                ChatterItemType.CASSETTE_TAPE: cassetteTapePullRate,
                ChatterItemType.GASHAPON: gashaponPullRate,
                ChatterItemType.GRENADE: grenadePullRate,
                ChatterItemType.TM_36: tm36PullRate,
                ChatterItemType.VORE: vorePullRate,
            }),
        )

        result = await self.mapper.parseGashaponItemDetails({
            'pullRates': {
                await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): {
                    'pullRate': airStrikePullRate.pullRate,
                    'iterations': airStrikePullRate.iterations,
                    'maximumPullAmount': airStrikePullRate.maximumPullAmount,
                    'minimumPullAmount': airStrikePullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.ANIMAL_PET): {
                    'pullRate': animalPetPullRate.pullRate,
                    'iterations': animalPetPullRate.iterations,
                    'maximumPullAmount': animalPetPullRate.maximumPullAmount,
                    'minimumPullAmount': animalPetPullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.BANANA): {
                    'pullRate': bananaPullRate.pullRate,
                    'iterations': bananaPullRate.iterations,
                    'maximumPullAmount': bananaPullRate.maximumPullAmount,
                    'minimumPullAmount': bananaPullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE): {
                    'pullRate': cassetteTapePullRate.pullRate,
                    'iterations': cassetteTapePullRate.iterations,
                    'maximumPullAmount': cassetteTapePullRate.maximumPullAmount,
                    'minimumPullAmount': cassetteTapePullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.GASHAPON): {
                    'pullRate': gashaponPullRate.pullRate,
                    'iterations': gashaponPullRate.iterations,
                    'maximumPullAmount': gashaponPullRate.maximumPullAmount,
                    'minimumPullAmount': gashaponPullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.GRENADE): {
                    'pullRate': grenadePullRate.pullRate,
                    'iterations': grenadePullRate.iterations,
                    'maximumPullAmount': grenadePullRate.maximumPullAmount,
                    'minimumPullAmount': grenadePullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.TM_36): {
                    'pullRate': tm36PullRate.pullRate,
                    'iterations': tm36PullRate.iterations,
                    'maximumPullAmount': tm36PullRate.maximumPullAmount,
                    'minimumPullAmount': tm36PullRate.minimumPullAmount,
                },
                await self.mapper.serializeItemType(ChatterItemType.VORE): {
                    'pullRate': vorePullRate.pullRate,
                    'iterations': vorePullRate.iterations,
                    'maximumPullAmount': vorePullRate.maximumPullAmount,
                    'minimumPullAmount': vorePullRate.minimumPullAmount,
                },
            },
        })

        assert isinstance(result, GashaponItemDetails)
        assert result == gashaponItemDetails

        assert len(result.pullRates) == len(ChatterItemType)
        assert result[ChatterItemType.AIR_STRIKE] == airStrikePullRate
        assert result[ChatterItemType.ANIMAL_PET] == animalPetPullRate
        assert result[ChatterItemType.BANANA] == bananaPullRate
        assert result[ChatterItemType.CASSETTE_TAPE] == cassetteTapePullRate
        assert result[ChatterItemType.GASHAPON] == gashaponPullRate
        assert result[ChatterItemType.GRENADE] == grenadePullRate
        assert result[ChatterItemType.TM_36] == tm36PullRate
        assert result[ChatterItemType.VORE] == vorePullRate

    @pytest.mark.asyncio
    async def test_parseGashaponItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseGashaponItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseGashaponItemDetails_withNone(self):
        result = await self.mapper.parseGashaponItemDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseGashaponItemPullRate(self):
        itemPullRate = GashaponItemPullRate(
            pullRate = 0.5,
            iterations = 2,
            maximumPullAmount = 3,
            minimumPullAmount = 1,
        )

        result = await self.mapper.parseGashaponItemPullRate({
            'pullRate': itemPullRate.pullRate,
            'iterations': itemPullRate.iterations,
            'maximumPullAmount': itemPullRate.maximumPullAmount,
            'minimumPullAmount': itemPullRate.minimumPullAmount,
        })

        assert isinstance(result, GashaponItemPullRate)
        assert result == itemPullRate
        assert result.pullRate == itemPullRate.pullRate
        assert result.iterations == itemPullRate.iterations
        assert result.maximumPullAmount == itemPullRate.maximumPullAmount
        assert result.minimumPullAmount == itemPullRate.minimumPullAmount

    @pytest.mark.asyncio
    async def test_parseGashaponItemPullRate2(self):
        itemPullRate = GashaponItemPullRate(
            pullRate = 0.125,
            iterations = 1,
            maximumPullAmount = 1,
            minimumPullAmount = 0,
        )

        result = await self.mapper.parseGashaponItemPullRate({
            'pullRate': itemPullRate.pullRate,
        })

        assert isinstance(result, GashaponItemPullRate)
        assert result == itemPullRate
        assert result.pullRate == itemPullRate.pullRate
        assert result.iterations == itemPullRate.iterations
        assert result.maximumPullAmount == itemPullRate.maximumPullAmount
        assert result.minimumPullAmount == itemPullRate.minimumPullAmount

    @pytest.mark.asyncio
    async def test_parseGashaponItemPullRate_withEmptyDictionary(self):
        result = await self.mapper.parseGashaponItemPullRate(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseGashaponItemPullRate_withMinimalJson(self):
        itemPullRate = GashaponItemPullRate(
            pullRate = 0.5,
            iterations = 1,
            maximumPullAmount = 1,
            minimumPullAmount = 0,
        )

        result = await self.mapper.parseGashaponItemPullRate({
            'pullRate': itemPullRate.pullRate,
        })

        assert isinstance(result, GashaponItemPullRate)
        assert result == itemPullRate
        assert result.pullRate == itemPullRate.pullRate
        assert result.iterations == itemPullRate.iterations
        assert result.maximumPullAmount == itemPullRate.maximumPullAmount
        assert result.minimumPullAmount == itemPullRate.minimumPullAmount

    @pytest.mark.asyncio
    async def test_parseGashaponItemPullRate_withNone(self):
        result = await self.mapper.parseGashaponItemPullRate(None)
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
        animalPets = round(random.uniform(0.01, 1.00) * 100)
        bananas = round(random.uniform(0.01, 1.00) * 100)
        cassetteTapes = round(random.uniform(0.01, 1.00) * 100)
        gashapons = round(random.uniform(0.01, 1.00) * 100)
        grenades = round(random.uniform(0.01, 1.00) * 100)
        tm36s = round(random.uniform(0.01, 1.00) * 100)
        vores = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
            await self.mapper.serializeItemType(ChatterItemType.ANIMAL_PET): animalPets,
            await self.mapper.serializeItemType(ChatterItemType.BANANA): bananas,
            await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE): cassetteTapes,
            await self.mapper.serializeItemType(ChatterItemType.GASHAPON): gashapons,
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
            await self.mapper.serializeItemType(ChatterItemType.TM_36): tm36s,
            await self.mapper.serializeItemType(ChatterItemType.VORE): vores,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == airStrikes
        assert result[ChatterItemType.ANIMAL_PET] == animalPets
        assert result[ChatterItemType.BANANA] == bananas
        assert result[ChatterItemType.CASSETTE_TAPE] == cassetteTapes
        assert result[ChatterItemType.GASHAPON] == gashapons
        assert result[ChatterItemType.GRENADE] == grenades
        assert result[ChatterItemType.TM_36] == tm36s
        assert result[ChatterItemType.VORE] == vores

    @pytest.mark.asyncio
    async def test_parseInventory2(self):
        airStrikes = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == airStrikes
        assert result[ChatterItemType.ANIMAL_PET] == 0
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.CASSETTE_TAPE] == 0
        assert result[ChatterItemType.GASHAPON] == 0
        assert result[ChatterItemType.GRENADE] == 0
        assert result[ChatterItemType.TM_36] == 0
        assert result[ChatterItemType.VORE] == 0

    @pytest.mark.asyncio
    async def test_parseInventory3(self):
        grenades = round(random.uniform(0.01, 1.00) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        assert result[ChatterItemType.AIR_STRIKE] == 0
        assert result[ChatterItemType.ANIMAL_PET] == 0
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.CASSETTE_TAPE] == 0
        assert result[ChatterItemType.GASHAPON] == 0
        assert result[ChatterItemType.GRENADE] == grenades
        assert result[ChatterItemType.TM_36] == 0
        assert result[ChatterItemType.VORE] == 0

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
        animalPets = round(random.uniform(-1.00, -0.01) * 100)
        bananas = round(random.uniform(-1.00, -0.01) * 100)
        cassetteTapes = round(random.uniform(-1.00, -0.01) * 100)
        gashapons = round(random.uniform(-1.00, -0.01) * 100)
        grenades = round(random.uniform(-1.00, -0.01) * 100)
        tm36s = round(random.uniform(-1.00, -0.01) * 100)
        vores = round(random.uniform(-1.00, -0.01) * 100)

        inventoryJson: dict[str, int] = {
            await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE): airStrikes,
            await self.mapper.serializeItemType(ChatterItemType.ANIMAL_PET): animalPets,
            await self.mapper.serializeItemType(ChatterItemType.BANANA): bananas,
            await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE): cassetteTapes,
            await self.mapper.serializeItemType(ChatterItemType.GASHAPON): gashapons,
            await self.mapper.serializeItemType(ChatterItemType.GRENADE): grenades,
            await self.mapper.serializeItemType(ChatterItemType.TM_36): tm36s,
            await self.mapper.serializeItemType(ChatterItemType.VORE): vores,
        }

        result = await self.mapper.parseInventory(inventoryJson)
        assert len(result) == len(ChatterItemType)

        # negative numbers should always be normalized to 0
        assert result[ChatterItemType.AIR_STRIKE] == 0
        assert result[ChatterItemType.ANIMAL_PET] == 0
        assert result[ChatterItemType.BANANA] == 0
        assert result[ChatterItemType.CASSETTE_TAPE] == 0
        assert result[ChatterItemType.GASHAPON] == 0
        assert result[ChatterItemType.GRENADE] == 0
        assert result[ChatterItemType.TM_36] == 0
        assert result[ChatterItemType.VORE] == 0

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
    async def test_parseItemType_withAnimalPet(self):
        result = await self.mapper.parseItemType('animal_pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animal_pets')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animal pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animal pets')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animal-pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animal-pets')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animalpet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('animalpets')
        assert result is ChatterItemType.ANIMAL_PET

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
    async def test_parseItemType_withGashapon(self):
        result = await self.mapper.parseItemType('gacha')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gachas')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gachapon')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gachapons')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gasha')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gashas')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gashapon')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.parseItemType('gashapons')
        assert result is ChatterItemType.GASHAPON

    @pytest.mark.asyncio
    async def test_parseItemType_withGrenade(self):
        result = await self.mapper.parseItemType('grenade')
        assert result is ChatterItemType.GRENADE

        result = await self.mapper.parseItemType('grenades')
        assert result is ChatterItemType.GRENADE

    @pytest.mark.asyncio
    async def test_parseItemType_withLootbox(self):
        result = await self.mapper.parseItemType('lootbox')
        assert result is ChatterItemType.GASHAPON

    @pytest.mark.asyncio
    async def test_parseItemType_withLootcrate(self):
        result = await self.mapper.parseItemType('lootcrate')
        assert result is ChatterItemType.GASHAPON

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
    async def test_parseItemType_withPet(self):
        result = await self.mapper.parseItemType('pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.parseItemType('pets')
        assert result is ChatterItemType.ANIMAL_PET

    @pytest.mark.asyncio
    async def test_parseItemType_withTm36(self):
        result = await self.mapper.parseItemType('tm_36')
        assert result is ChatterItemType.TM_36

        result = await self.mapper.parseItemType('tm-36')
        assert result is ChatterItemType.TM_36

        result = await self.mapper.parseItemType('tm 36')
        assert result is ChatterItemType.TM_36

        result = await self.mapper.parseItemType('tm36')
        assert result is ChatterItemType.TM_36

    @pytest.mark.asyncio
    async def test_parseItemType_withTnt(self):
        result = await self.mapper.parseItemType('tnt')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('tnts')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.parseItemType('tnt\'s')
        assert result is ChatterItemType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_parseItemType_withVore(self):
        result = await self.mapper.parseItemType('vore')
        assert result is ChatterItemType.VORE

        result = await self.mapper.parseItemType('vores')
        assert result is ChatterItemType.VORE

        result = await self.mapper.parseItemType('voar')
        assert result is ChatterItemType.VORE

        result = await self.mapper.parseItemType('voars')
        assert result is ChatterItemType.VORE

    @pytest.mark.asyncio
    async def test_parseItemType_withWhitespaceString(self):
        result = await self.mapper.parseItemType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTm36ItemDetails(self):
        details = Tm36ItemDetails(
            maxDurationSeconds = 600,
            minDurationSeconds = 300,
        )

        result = await self.mapper.parseTm36ItemDetails({
            'maxDurationSeconds': details.maxDurationSeconds,
            'minDurationSeconds': details.minDurationSeconds,
        })

        assert isinstance(result, Tm36ItemDetails)
        assert result == details
        assert result.maxDurationSeconds == details.maxDurationSeconds
        assert result.minDurationSeconds == details.minDurationSeconds

    @pytest.mark.asyncio
    async def test_parseTm36ItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseTm36ItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTm36ItemDetails_withNone(self):
        result = await self.mapper.parseTm36ItemDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoreItemDetails(self):
        details = VoreItemDetails(
            timeoutDurationSeconds = 86400,
        )

        result = await self.mapper.parseVoreItemDetails({
            'timeoutDurationSeconds': details.timeoutDurationSeconds,
        })

        assert isinstance(result, VoreItemDetails)
        assert result == details
        assert result.timeoutDurationSeconds == details.timeoutDurationSeconds

    @pytest.mark.asyncio
    async def test_parseVoreItemDetails_withEmptyDictionary(self):
        result = await self.mapper.parseVoreItemDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoreItemDetails_withNone(self):
        result = await self.mapper.parseVoreItemDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireGashaponItemPullRate(self):
        itemPullRate = GashaponItemPullRate(
            pullRate = 0.75,
            iterations = 1,
            maximumPullAmount = 2,
            minimumPullAmount = 0,
        )

        result = await self.mapper.requireGashaponItemPullRate({
            'pullRate': itemPullRate.pullRate,
            'iterations': itemPullRate.iterations,
            'maximumPullAmount': itemPullRate.maximumPullAmount,
            'minimumPullAmount': itemPullRate.minimumPullAmount,
        })

        assert isinstance(result, GashaponItemPullRate)
        assert result == itemPullRate
        assert result.pullRate == itemPullRate.pullRate
        assert result.iterations == itemPullRate.iterations
        assert result.maximumPullAmount == itemPullRate.maximumPullAmount
        assert result.minimumPullAmount == itemPullRate.minimumPullAmount

    @pytest.mark.asyncio
    async def test_requireGashaponItemPullRate2(self):
        itemPullRate = GashaponItemPullRate(
            pullRate = 0.9,
            iterations = 1,
            maximumPullAmount = 1,
            minimumPullAmount = 0,
        )

        result = await self.mapper.requireGashaponItemPullRate({
            'pullRate': itemPullRate.pullRate,
        })

        assert isinstance(result, GashaponItemPullRate)
        assert result == itemPullRate
        assert result.pullRate == itemPullRate.pullRate
        assert result.iterations == itemPullRate.iterations
        assert result.maximumPullAmount == itemPullRate.maximumPullAmount
        assert result.minimumPullAmount == itemPullRate.minimumPullAmount

    @pytest.mark.asyncio
    async def test_requireGashaponItemPullRate_withEmptyDictionary(self):
        result: GashaponItemPullRate | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireGashaponItemPullRate(dict())

        assert result is None

    @pytest.mark.asyncio
    async def test_requireGashaponItemPullRate_withNone(self):
        result: GashaponItemPullRate | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireGashaponItemPullRate(None)

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
    async def test_requireItemType_withAnimalPet(self):
        result = await self.mapper.requireItemType('animal_pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animal_pets')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animal pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animal pets')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animal-pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animal-pets')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animalpet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('animalpets')
        assert result is ChatterItemType.ANIMAL_PET

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
    async def test_requireItemType_withGashapon(self):
        result = await self.mapper.requireItemType('gacha')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gachas')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gachapon')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gachapons')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gasha')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gashas')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gashapon')
        assert result is ChatterItemType.GASHAPON

        result = await self.mapper.requireItemType('gashapons')
        assert result is ChatterItemType.GASHAPON

    @pytest.mark.asyncio
    async def test_requireItemType_withGrenade(self):
        result = await self.mapper.requireItemType('grenade')
        assert result is ChatterItemType.GRENADE

        result = await self.mapper.requireItemType('grenades')
        assert result is ChatterItemType.GRENADE

    @pytest.mark.asyncio
    async def test_requireItemType_withLootbox(self):
        result = await self.mapper.requireItemType('lootbox')
        assert result is ChatterItemType.GASHAPON

    @pytest.mark.asyncio
    async def test_requireItemType_withLootcrate(self):
        result = await self.mapper.requireItemType('lootcrate')
        assert result is ChatterItemType.GASHAPON

    @pytest.mark.asyncio
    async def test_requireItemType_withNade(self):
        result = await self.mapper.requireItemType('nade')
        assert result is ChatterItemType.GRENADE

        result = await self.mapper.requireItemType('nades')
        assert result is ChatterItemType.GRENADE

    @pytest.mark.asyncio
    async def test_requireItemType_withNone(self):
        result: ChatterItemType | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireItemType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireItemType_withPet(self):
        result = await self.mapper.requireItemType('pet')
        assert result is ChatterItemType.ANIMAL_PET

        result = await self.mapper.requireItemType('pets')
        assert result is ChatterItemType.ANIMAL_PET

    @pytest.mark.asyncio
    async def test_requireItemType_withTm36(self):
        result = await self.mapper.requireItemType('tm_36')
        assert result is ChatterItemType.TM_36

        result = await self.mapper.requireItemType('tm-36')
        assert result is ChatterItemType.TM_36

        result = await self.mapper.requireItemType('tm 36')
        assert result is ChatterItemType.TM_36

        result = await self.mapper.requireItemType('tm36')
        assert result is ChatterItemType.TM_36

    @pytest.mark.asyncio
    async def test_requireItemType_withTnt(self):
        result = await self.mapper.requireItemType('tnt')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('tnts')
        assert result is ChatterItemType.AIR_STRIKE

        result = await self.mapper.requireItemType('tnt\'s')
        assert result is ChatterItemType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_requireItemType_withVore(self):
        result = await self.mapper.requireItemType('voar')
        assert result is ChatterItemType.VORE

        result = await self.mapper.requireItemType('voars')
        assert result is ChatterItemType.VORE

        result = await self.mapper.requireItemType('vore')
        assert result is ChatterItemType.VORE

        result = await self.mapper.requireItemType('vores')
        assert result is ChatterItemType.VORE

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
        animalPets = round(random.uniform(0.01, 1.00) * 100)
        bananas = round(random.uniform(0.01, 1.00) * 100)
        cassetteTapes = round(random.uniform(0.01, 1.00) * 100)
        gashapons = round(random.uniform(0.01, 1.00) * 100)
        grenades = round(random.uniform(0.01, 1.00) * 100)
        tm36s = round(random.uniform(0.01, 1.00) * 100)
        vores = round(random.uniform(0.01, 1.00) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
            ChatterItemType.ANIMAL_PET: animalPets,
            ChatterItemType.BANANA: bananas,
            ChatterItemType.CASSETTE_TAPE: cassetteTapes,
            ChatterItemType.GASHAPON: gashapons,
            ChatterItemType.GRENADE: grenades,
            ChatterItemType.TM_36: tm36s,
            ChatterItemType.VORE: vores,
        }

        result = await self.mapper.serializeInventory(inventory)
        assert len(result) == len(ChatterItemType)

        assert result[await self.mapper.serializeItemType(ChatterItemType.AIR_STRIKE)] == airStrikes
        assert result[await self.mapper.serializeItemType(ChatterItemType.ANIMAL_PET)] == animalPets
        assert result[await self.mapper.serializeItemType(ChatterItemType.BANANA)] == bananas
        assert result[await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE)] == cassetteTapes
        assert result[await self.mapper.serializeItemType(ChatterItemType.GASHAPON)] == gashapons
        assert result[await self.mapper.serializeItemType(ChatterItemType.GRENADE)] == grenades
        assert result[await self.mapper.serializeItemType(ChatterItemType.TM_36)] == tm36s
        assert result[await self.mapper.serializeItemType(ChatterItemType.VORE)] == vores

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
        animalPets = round(random.uniform(-1.00, -0.01) * 100)
        bananas = round(random.uniform(-1.00, -0.01) * 100)
        cassetteTapes = round(random.uniform(-1.00, -0.01) * 100)
        gashapons = round(random.uniform(-1.00, -0.01) * 100)
        grenades = round(random.uniform(-1.00, -0.01) * 100)
        tm36s = round(random.uniform(-1.00, -0.01) * 100)
        vores = round(random.uniform(-1.00, -0.01) * 100)

        inventory: dict[ChatterItemType, int] = {
            ChatterItemType.AIR_STRIKE: airStrikes,
            ChatterItemType.ANIMAL_PET: animalPets,
            ChatterItemType.BANANA: bananas,
            ChatterItemType.CASSETTE_TAPE: cassetteTapes,
            ChatterItemType.GASHAPON: gashapons,
            ChatterItemType.GRENADE: grenades,
            ChatterItemType.TM_36: tm36s,
            ChatterItemType.VORE: vores,
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
    async def test_serializeItemType_withAnimalPet(self):
        result = await self.mapper.serializeItemType(ChatterItemType.ANIMAL_PET)
        assert result == 'animal_pet'

    @pytest.mark.asyncio
    async def test_serializeItemType_withBanana(self):
        result = await self.mapper.serializeItemType(ChatterItemType.BANANA)
        assert result == 'banana'

    @pytest.mark.asyncio
    async def test_serializeItemType_withCassetteTape(self):
        result = await self.mapper.serializeItemType(ChatterItemType.CASSETTE_TAPE)
        assert result == 'cassette_tape'

    @pytest.mark.asyncio
    async def test_serializeItemType_withGashapon(self):
        result = await self.mapper.serializeItemType(ChatterItemType.GASHAPON)
        assert result == 'gashapon'

    @pytest.mark.asyncio
    async def test_serializeItemType_withGrenade(self):
        result = await self.mapper.serializeItemType(ChatterItemType.GRENADE)
        assert result == 'grenade'

    @pytest.mark.asyncio
    async def test_serializeItemType_withTm36(self):
        result = await self.mapper.serializeItemType(ChatterItemType.TM_36)
        assert result == 'tm36'

    @pytest.mark.asyncio
    async def test_serializeItemType_withVore(self):
        result = await self.mapper.serializeItemType(ChatterItemType.VORE)
        assert result == 'vore'
