import json

import pytest

from src.cheerActions.absCheerAction import AbsCheerAction
from src.cheerActions.beanChanceCheerAction import BeanChanceCheerAction
from src.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from src.cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from src.cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from src.cheerActions.cheerActionType import CheerActionType
from src.cheerActions.crowdControl.crowdControlCheerAction import CrowdControlCheerAction
from src.cheerActions.crowdControl.crowdControlCheerActionType import CrowdControlCheerActionType
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestCheerActionJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withNone(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withBeanChanceString(self):
        result = await self.jsonMapper.parseCheerActionType('bean_chance')
        assert result is CheerActionType.BEAN_CHANCE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withCrowdControlString(self):
        result = await self.jsonMapper.parseCheerActionType('crowd_control')
        assert result is CheerActionType.CROWD_CONTROL

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withEmptyString(self):
        result = await self.jsonMapper.parseCheerActionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withNone(self):
        result = await self.jsonMapper.parseCheerActionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withSoundAlertString(self):
        result = await self.jsonMapper.parseCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withTimeoutString(self):
        result = await self.jsonMapper.parseCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCrowdControlCheerActionType_withButtonPressString(self):
        result = await self.jsonMapper.parseCrowdControlCheerActionType('button_press')
        assert result is CrowdControlCheerActionType.BUTTON_PRESS

    @pytest.mark.asyncio
    async def test_parseCrowdControlCheerActionType_withEmptyString(self):
        result = await self.jsonMapper.parseCrowdControlCheerActionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCrowdControlCheerActionType_withGameShuffleString(self):
        result = await self.jsonMapper.parseCrowdControlCheerActionType('game_shuffle')
        assert result is CrowdControlCheerActionType.GAME_SHUFFLE

    @pytest.mark.asyncio
    async def test_parseCrowdControlCheerActionType_withNone(self):
        result = await self.jsonMapper.parseCrowdControlCheerActionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCrowdControlCheerActionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseCrowdControlCheerActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withBeanChanceString(self):
        result = await self.jsonMapper.requireCheerActionType('bean_chance')
        assert result is CheerActionType.BEAN_CHANCE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withCrowdControlString(self):
        result = await self.jsonMapper.requireCheerActionType('crowd_control')
        assert result is CheerActionType.CROWD_CONTROL

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withSoundAlertString(self):
        result = await self.jsonMapper.requireCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withTimeoutString(self):
        result = await self.jsonMapper.requireCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_requireCrowdControlCheerActionType_withButtonPressString(self):
        result = await self.jsonMapper.requireCrowdControlCheerActionType('button_press')
        assert result is CrowdControlCheerActionType.BUTTON_PRESS

    @pytest.mark.asyncio
    async def test_requireCrowdControlCheerActionType_withEmptyString(self):
        result: CrowdControlCheerActionType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireCrowdControlCheerActionType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCrowdControlCheerActionType_withGameShuffleString(self):
        result = await self.jsonMapper.requireCrowdControlCheerActionType('game_shuffle')
        assert result is CrowdControlCheerActionType.GAME_SHUFFLE

    @pytest.mark.asyncio
    async def test_requireCrowdControlCheerActionType_withNone(self):
        result: CrowdControlCheerActionType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireCrowdControlCheerActionType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCrowdControlCheerActionType_withWhitespaceString(self):
        result: CrowdControlCheerActionType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireCrowdControlCheerActionType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withBeanChanceCheerAction(self):
        cheerAction: AbsCheerAction = BeanChanceCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            randomChance = 70,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 1

        assert dictionary['randomChance'] == 70

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withCrowdControlCheerAction(self):
        cheerAction: AbsCheerAction = CrowdControlCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            crowdControlCheerActionType = CrowdControlCheerActionType.GAME_SHUFFLE,
            bits = 50,
            gigaShuffleChance = 20,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 2

        assert dictionary['crowdControlCheerActionType'] == 'game_shuffle'
        assert dictionary['gigaShuffleChance'] == 20

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withAny(self):
        result = await self.jsonMapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.ANY)
        assert result == 'any'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withOffline(self):
        result = await self.jsonMapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.OFFLINE)
        assert result == 'offline'

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement_withOnline(self):
        result = await self.jsonMapper.serializeCheerActionStreamStatusRequirement(CheerActionStreamStatusRequirement.ONLINE)
        assert result == 'online'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withBeanChance(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.BEAN_CHANCE)
        assert result == 'bean_chance'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withCrowdControl(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.CROWD_CONTROL)
        assert result == 'crowd_control'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withSoundAlert(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.SOUND_ALERT)
        assert result == 'sound_alert'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withTimeout(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.TIMEOUT)
        assert result == 'timeout'

    @pytest.mark.asyncio
    async def test_serializeCrowdControlCheerActionType_withButtonPress(self):
        result = await self.jsonMapper.serializeCrowdControlCheerActionType(CrowdControlCheerActionType.BUTTON_PRESS)
        assert result == 'button_press'

    @pytest.mark.asyncio
    async def test_serializeCrowdControlCheerActionType_withGameShuffle(self):
        result = await self.jsonMapper.serializeCrowdControlCheerActionType(CrowdControlCheerActionType.GAME_SHUFFLE)
        assert result == 'game_shuffle'
