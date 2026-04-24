import json
from typing import Final

import pytest

from src.chatterInventory.mappers.chatterInventoryMapper import ChatterInventoryMapper
from src.chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from src.cheerActions.absCheerAction import AbsCheerAction
from src.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from src.cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from src.cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from src.cheerActions.cheerActionType import CheerActionType
from src.cheerActions.crowdControl.crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from src.cheerActions.crowdControl.crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from src.cheerActions.soundAlert.soundAlertCheerAction import SoundAlertCheerAction


class TestCheerActionJsonMapper:

    chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = ChatterInventoryMapper()

    mapper: Final[CheerActionJsonMapperInterface] = CheerActionJsonMapper(
        chatterInventoryMapper = chatterInventoryMapper,
    )

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.mapper.parseCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withEmptyString(self):
        result = await self.mapper.parseCheerActionStreamStatusRequirement('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withNone(self):
        result = await self.mapper.parseCheerActionStreamStatusRequirement(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.mapper.parseCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.mapper.parseCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withWhitespaceString(self):
        result = await self.mapper.parseCheerActionStreamStatusRequirement(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withCrowdControlString(self):
        result = await self.mapper.parseCheerActionType('crowd_control')
        assert result is CheerActionType.CROWD_CONTROL

        result = await self.mapper.parseCheerActionType('crowd-control')
        assert result is CheerActionType.CROWD_CONTROL

        result = await self.mapper.parseCheerActionType('crowd control')
        assert result is CheerActionType.CROWD_CONTROL

        result = await self.mapper.parseCheerActionType('crowdcontrol')
        assert result is CheerActionType.CROWD_CONTROL

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withEmptyString(self):
        result = await self.mapper.parseCheerActionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withGameShuffleString(self):
        result = await self.mapper.parseCheerActionType('game_shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

        result = await self.mapper.parseCheerActionType('game-shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

        result = await self.mapper.parseCheerActionType('game shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

        result = await self.mapper.parseCheerActionType('gameshuffle')
        assert result is CheerActionType.GAME_SHUFFLE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withItemString(self):
        result = await self.mapper.parseCheerActionType('item')
        assert result is CheerActionType.ITEM_USE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withItemUseString(self):
        result = await self.mapper.parseCheerActionType('item_use')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.parseCheerActionType('item-use')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.parseCheerActionType('item use')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.parseCheerActionType('itemuse')
        assert result is CheerActionType.ITEM_USE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withNone(self):
        result = await self.mapper.parseCheerActionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withSoundAlertString(self):
        result = await self.mapper.parseCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

        result = await self.mapper.parseCheerActionType('sound-alert')
        assert result is CheerActionType.SOUND_ALERT

        result = await self.mapper.parseCheerActionType('sound alert')
        assert result is CheerActionType.SOUND_ALERT

        result = await self.mapper.parseCheerActionType('soundalert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withUseItemString(self):
        result = await self.mapper.parseCheerActionType('use_item')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.parseCheerActionType('use-item')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.parseCheerActionType('use item')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.parseCheerActionType('useitem')
        assert result is CheerActionType.ITEM_USE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withWhitespaceString(self):
        result = await self.mapper.parseCheerActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.mapper.requireCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withEmptyString(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireCheerActionStreamStatusRequirement('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withNone(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireCheerActionStreamStatusRequirement(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.mapper.requireCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.mapper.requireCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withWhitespaceString(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireCheerActionStreamStatusRequirement(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withCrowdControlString(self):
        result = await self.mapper.requireCheerActionType('crowd_control')
        assert result is CheerActionType.CROWD_CONTROL

        result = await self.mapper.requireCheerActionType('crowd-control')
        assert result is CheerActionType.CROWD_CONTROL

        result = await self.mapper.requireCheerActionType('crowd control')
        assert result is CheerActionType.CROWD_CONTROL

        result = await self.mapper.requireCheerActionType('crowdcontrol')
        assert result is CheerActionType.CROWD_CONTROL

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withGameShuffleString(self):
        result = await self.mapper.requireCheerActionType('game_shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

        result = await self.mapper.requireCheerActionType('game-shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

        result = await self.mapper.requireCheerActionType('game shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

        result = await self.mapper.requireCheerActionType('gameshuffle')
        assert result is CheerActionType.GAME_SHUFFLE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withItemString(self):
        result = await self.mapper.requireCheerActionType('item')
        assert result is CheerActionType.ITEM_USE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withItemUseString(self):
        result = await self.mapper.requireCheerActionType('item_use')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.requireCheerActionType('item-use')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.requireCheerActionType('item use')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.requireCheerActionType('itemuse')
        assert result is CheerActionType.ITEM_USE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withSoundAlertString(self):
        result = await self.mapper.requireCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withUseItem(self):
        result = await self.mapper.requireCheerActionType('use_item')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.requireCheerActionType('use-item')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.requireCheerActionType('use item')
        assert result is CheerActionType.ITEM_USE

        result = await self.mapper.requireCheerActionType('useitem')
        assert result is CheerActionType.ITEM_USE

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, CheerActionJsonMapper)
        assert isinstance(self.mapper, CheerActionJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withCrowdControlButtonPressCheerAction(self):
        cheerAction: AbsCheerAction = CrowdControlButtonPressCheerAction(
            enabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            twitchChannelId = 'abc123',
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 0

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withCrowdControlGameShuffleCheerAction1(self):
        cheerAction: AbsCheerAction = CrowdControlGameShuffleCheerAction(
            enabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            gigaShuffleChance = 20,
            twitchChannelId = 'abc123',
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 1

        assert dictionary['gigaShuffleChance'] == 20

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withCrowdControlGameShuffleCheerAction2(self):
        cheerAction: AbsCheerAction = CrowdControlGameShuffleCheerAction(
            enabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            gigaShuffleChance = None,
            twitchChannelId = 'abc123',
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 0

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withSoundAlertCheerAction(self):
        cheerAction: AbsCheerAction = SoundAlertCheerAction(
            enabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            directory = 'soundsDirectory',
            twitchChannelId = 'abc123',
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 1

        assert dictionary['directory'] == 'soundsDirectory'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement(self):
        results: set[str] = set()

        for streamStatusRequirement in CheerActionStreamStatusRequirement:
            results.add(await self.mapper.serializeCheerActionStreamStatusRequirement(streamStatusRequirement))

        assert len(results) == len(CheerActionStreamStatusRequirement)

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withAny(self):
        result = await self.mapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.ANY)
        assert result == 'any'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withOffline(self):
        result = await self.mapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.OFFLINE)
        assert result == 'offline'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withOnline(self):
        result = await self.mapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.ONLINE)
        assert result == 'online'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType(self):
        results: set[str] = set()

        for cheerActionType in CheerActionType:
            results.add(await self.mapper.serializeCheerActionType(cheerActionType))

        assert len(results) == len(CheerActionType)

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withCrowdControl(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.CROWD_CONTROL)
        assert result == 'crowd_control'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withGameShuffle(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.GAME_SHUFFLE)
        assert result == 'game_shuffle'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withItemUse(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.ITEM_USE)
        assert result == 'item_use'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withSoundAlert(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.SOUND_ALERT)
        assert result == 'sound_alert'
