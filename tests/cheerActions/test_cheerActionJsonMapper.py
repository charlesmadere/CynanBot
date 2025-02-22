import json

import pytest

from src.cheerActions.absCheerAction import AbsCheerAction
from src.cheerActions.beanChance.beanChanceCheerAction import BeanChanceCheerAction
from src.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from src.cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from src.cheerActions.cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from src.cheerActions.cheerActionType import CheerActionType
from src.cheerActions.crowdControl.crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from src.cheerActions.crowdControl.crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from src.cheerActions.soundAlert.soundAlertCheerAction import SoundAlertCheerAction
from src.cheerActions.timeout.timeoutCheerAction import TimeoutCheerAction
from src.cheerActions.tnt.tntCheerAction import TntCheerAction
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
    async def test_parseCheerActionType_withGameShuffle(self):
        result = await self.jsonMapper.parseCheerActionType('game_shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

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
    async def test_parseCheerActionType_withTntString(self):
        result = await self.jsonMapper.parseCheerActionType('tnt')
        assert result is CheerActionType.TNT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionType(' ')
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
    async def test_requireCheerActionType_withTntString(self):
        result = await self.jsonMapper.requireCheerActionType('tnt')
        assert result is CheerActionType.TNT

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
    async def test_serializeAbsCheerAction_withCrowdControlButtonPressCheerAction(self):
        cheerAction: AbsCheerAction = CrowdControlButtonPressCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 0

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withCrowdControlGameShuffleCheerAction1(self):
        cheerAction: AbsCheerAction = CrowdControlGameShuffleCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            gigaShuffleChance = 20,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 1

        assert dictionary['gigaShuffleChance'] == 20

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withCrowdControlGameShuffleCheerAction2(self):
        cheerAction: AbsCheerAction = CrowdControlGameShuffleCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            gigaShuffleChance = None,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 0

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withSoundAlertCheerAction(self):
        cheerAction: AbsCheerAction = SoundAlertCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            directory = 'soundsDirectory',
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 1

        assert dictionary['directory'] == 'soundsDirectory'

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withTimeoutCheerAction1(self):
        cheerAction = TimeoutCheerAction(
            isEnabled = True,
            isRandomChanceEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            durationSeconds = 60,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 2

        assert dictionary['durationSeconds'] == cheerAction.durationSeconds
        assert dictionary['randomChanceEnabled'] == cheerAction.isRandomChanceEnabled

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withTimeoutCheerAction2(self):
        cheerAction = TimeoutCheerAction(
            isEnabled = True,
            isRandomChanceEnabled = False,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            durationSeconds = 300,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 2

        assert dictionary['durationSeconds'] == cheerAction.durationSeconds
        assert dictionary['randomChanceEnabled'] == cheerAction.isRandomChanceEnabled

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withTntCheerAction(self):
        cheerAction = TntCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            maxDurationSeconds = 90,
            minDurationSeconds = 55,
            maxTimeoutChatters = 10,
            minTimeoutChatters = 3,
            twitchChannelId = 'abc123',
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 4

        assert dictionary['maxDurationSeconds'] == cheerAction.maxDurationSeconds
        assert dictionary['minDurationSeconds'] == cheerAction.minDurationSeconds
        assert dictionary['maxTimeoutChatters'] == cheerAction.maxTimeoutChatters
        assert dictionary['minTimeoutChatters'] == cheerAction.minTimeoutChatters

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
    async def test_serializeCheerActionType_withGameShuffle(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.GAME_SHUFFLE)
        assert result == 'game_shuffle'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withSoundAlert(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.SOUND_ALERT)
        assert result == 'sound_alert'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withTimeout(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.TIMEOUT)
        assert result == 'timeout'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withTnt(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.TNT)
        assert result == 'tnt'
