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
from src.cheerActions.timeout.timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from src.cheerActions.tnt.tntCheerAction import TntCheerAction
from src.cheerActions.voicemail.voicemailCheerAction import VoicemailCheerAction
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestCheerActionJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withEmptyString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withNone(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_parseCheerActionStreamStatusRequirement_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionStreamStatusRequirement(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withAdgeString(self):
        result = await self.jsonMapper.parseCheerActionType('adge')
        assert result is CheerActionType.ADGE

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
    async def test_parseCheerActionType_withVoicemailString(self):
        result = await self.jsonMapper.parseCheerActionType('voicemail')
        assert result is CheerActionType.VOICEMAIL

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseCheerActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withAny(self):
        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('any')
        assert result is TimeoutCheerActionTargetType.ANY

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withEmptyString(self):
        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withNone(self):
        result = await self.jsonMapper.parseTimeoutCheerActionTargetType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withRandomOnly(self):
        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('random')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('random only')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withSpecificTargetOnly(self):
        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('specific')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('specific target')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('specific targets')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('specific target only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.parseTimeoutCheerActionTargetType('specific targets only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withWhitespaceString(self):
        result = await self.jsonMapper.parseTimeoutCheerActionTargetType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicemailCheerAction(self):
        result = await self.jsonMapper.parseVoicemailCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 999,
            jsonString = None,
            twitchChannelId = 'abc123'
        )

        assert isinstance(result, VoicemailCheerAction)
        assert result.isEnabled
        assert result.streamStatusRequirement is CheerActionStreamStatusRequirement.ANY
        assert result.bits == 999
        assert result.twitchChannelId == 'abc123'

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withAnyString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('any')
        assert result is CheerActionStreamStatusRequirement.ANY

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withEmptyString(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withNone(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireCheerActionStreamStatusRequirement(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOfflineString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('offline')
        assert result is CheerActionStreamStatusRequirement.OFFLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withOnlineString(self):
        result = await self.jsonMapper.requireCheerActionStreamStatusRequirement('online')
        assert result is CheerActionStreamStatusRequirement.ONLINE

    @pytest.mark.asyncio
    async def test_requireCheerActionStreamStatusRequirement_withWhitespaceString(self):
        result: CheerActionStreamStatusRequirement | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireCheerActionStreamStatusRequirement(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withAdgeString(self):
        result = await self.jsonMapper.requireCheerActionType('adge')
        assert result is CheerActionType.ADGE

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
    async def test_requireCheerActionType_withVoicemailString(self):
        result = await self.jsonMapper.requireCheerActionType('voicemail')
        assert result is CheerActionType.VOICEMAIL

    @pytest.mark.asyncio
    async def test_requireTimeoutCheerActionTargetType_withAny(self):
        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('any')
        assert result is TimeoutCheerActionTargetType.ANY

    @pytest.mark.asyncio
    async def test_requireTimeoutCheerActionTargetType_withRandomOnly(self):
        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('random')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('random only')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

    @pytest.mark.asyncio
    async def test_requireTimeoutCheerActionTargetType_withSpecificTargetOnly(self):
        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('specific')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('specific target')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('specific targets')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('specific target only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.jsonMapper.requireTimeoutCheerActionTargetType('specific targets only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, CheerActionJsonMapper)
        assert isinstance(self.jsonMapper, CheerActionJsonMapperInterface)

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
            targetType = TimeoutCheerActionTargetType.ANY
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 3

        assert dictionary['durationSeconds'] == cheerAction.durationSeconds
        assert dictionary['randomChanceEnabled'] == cheerAction.isRandomChanceEnabled
        assert dictionary['targetType'] == await self.jsonMapper.serializeTimeoutCheerActionTargetType(cheerAction.targetType)

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withTimeoutCheerAction2(self):
        cheerAction = TimeoutCheerAction(
            isEnabled = True,
            isRandomChanceEnabled = False,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            durationSeconds = 300,
            twitchChannelId = 'abc123',
            targetType = TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 3

        assert dictionary['durationSeconds'] == cheerAction.durationSeconds
        assert dictionary['randomChanceEnabled'] == cheerAction.isRandomChanceEnabled
        assert dictionary['targetType'] == await self.jsonMapper.serializeTimeoutCheerActionTargetType(cheerAction.targetType)

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
    async def test_serializeCheerAction_withVoicemailCheerAction(self):
        cheerAction = VoicemailCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            twitchChannelId = 'abc123'
        )

        result = await self.jsonMapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 0

    @pytest.mark.asyncio
    async def test_serializeCheerActionStreamStatusRequirement(self):
        results: set[str] = set()

        for streamStatusRequirement in CheerActionStreamStatusRequirement:
            results.add(await self.jsonMapper.serializeCheerActionStreamStatusRequirement(streamStatusRequirement))

        assert len(results) == len(CheerActionStreamStatusRequirement)

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
    async def test_serializeCheerActionType(self):
        results: set[str] = set()

        for cheerActionType in CheerActionType:
            results.add(await self.jsonMapper.serializeCheerActionType(cheerActionType))

        assert len(results) == len(CheerActionType)

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withAdge(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.ADGE)
        assert result == 'adge'

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

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withVoicemail(self):
        result = await self.jsonMapper.serializeCheerActionType(CheerActionType.VOICEMAIL)
        assert result == 'voicemail'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionTargetType_withAny(self):
        result = await self.jsonMapper.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.ANY)
        assert result == 'any'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionTargetType_withRandomOnly(self):
        result = await self.jsonMapper.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.RANDOM_ONLY)
        assert result == 'random'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionTargetType_withSpecificTargetOnly(self):
        result = await self.jsonMapper.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY)
        assert result == 'specific'
