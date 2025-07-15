import json

import pytest

from src.cheerActions.absCheerAction import AbsCheerAction
from src.cheerActions.airStrike.airStrikeCheerAction import AirStrikeCheerAction
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
from src.cheerActions.voicemail.voicemailCheerAction import VoicemailCheerAction


class TestCheerActionJsonMapper:

    mapper: CheerActionJsonMapperInterface = CheerActionJsonMapper()

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
    async def test_parseCheerActionType_withAdgeString(self):
        result = await self.mapper.parseCheerActionType('adge')
        assert result is CheerActionType.ADGE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withAirStrikeStrings(self):
        result = await self.mapper.parseCheerActionType('air_strike')
        assert result is CheerActionType.AIR_STRIKE

        result = await self.mapper.parseCheerActionType('air-strike')
        assert result is CheerActionType.AIR_STRIKE

        result = await self.mapper.parseCheerActionType('air strike')
        assert result is CheerActionType.AIR_STRIKE

        result = await self.mapper.parseCheerActionType('airstrike')
        assert result is CheerActionType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withBeanChanceString(self):
        result = await self.mapper.parseCheerActionType('bean_chance')
        assert result is CheerActionType.BEAN_CHANCE

        result = await self.mapper.parseCheerActionType('bean-chance')
        assert result is CheerActionType.BEAN_CHANCE

        result = await self.mapper.parseCheerActionType('bean chance')
        assert result is CheerActionType.BEAN_CHANCE

        result = await self.mapper.parseCheerActionType('beanchance')
        assert result is CheerActionType.BEAN_CHANCE

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
    async def test_parseCheerActionType_withGameShuffle(self):
        result = await self.mapper.parseCheerActionType('game_shuffle')
        assert result is CheerActionType.GAME_SHUFFLE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withNone(self):
        result = await self.mapper.parseCheerActionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withSoundAlertString(self):
        result = await self.mapper.parseCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withTimeoutString(self):
        result = await self.mapper.parseCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withTntString(self):
        result = await self.mapper.parseCheerActionType('tnt')
        assert result is CheerActionType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withVoicemailString(self):
        result = await self.mapper.parseCheerActionType('voicemail')
        assert result is CheerActionType.VOICEMAIL

    @pytest.mark.asyncio
    async def test_parseCheerActionType_withWhitespaceString(self):
        result = await self.mapper.parseCheerActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withAny(self):
        result = await self.mapper.parseTimeoutCheerActionTargetType('any')
        assert result is TimeoutCheerActionTargetType.ANY

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withEmptyString(self):
        result = await self.mapper.parseTimeoutCheerActionTargetType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withNone(self):
        result = await self.mapper.parseTimeoutCheerActionTargetType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withRandomOnly(self):
        result = await self.mapper.parseTimeoutCheerActionTargetType('random')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

        result = await self.mapper.parseTimeoutCheerActionTargetType('random only')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withSpecificTargetOnly(self):
        result = await self.mapper.parseTimeoutCheerActionTargetType('specific')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.parseTimeoutCheerActionTargetType('specific target')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.parseTimeoutCheerActionTargetType('specific targets')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.parseTimeoutCheerActionTargetType('specific target only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.parseTimeoutCheerActionTargetType('specific targets only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

    @pytest.mark.asyncio
    async def test_parseTimeoutCheerActionTargetType_withWhitespaceString(self):
        result = await self.mapper.parseTimeoutCheerActionTargetType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicemailCheerAction(self):
        result = await self.mapper.parseVoicemailCheerAction(
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
    async def test_requireCheerActionType_withAdgeString(self):
        result = await self.mapper.requireCheerActionType('adge')
        assert result is CheerActionType.ADGE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withAirStrikeStrings(self):
        result = await self.mapper.requireCheerActionType('air_strike')
        assert result is CheerActionType.AIR_STRIKE

        result = await self.mapper.requireCheerActionType('air-strike')
        assert result is CheerActionType.AIR_STRIKE

        result = await self.mapper.requireCheerActionType('air strike')
        assert result is CheerActionType.AIR_STRIKE

        result = await self.mapper.requireCheerActionType('airstrike')
        assert result is CheerActionType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withBeanChanceString(self):
        result = await self.mapper.requireCheerActionType('bean_chance')
        assert result is CheerActionType.BEAN_CHANCE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withCrowdControlString(self):
        result = await self.mapper.requireCheerActionType('crowd_control')
        assert result is CheerActionType.CROWD_CONTROL

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withSoundAlertString(self):
        result = await self.mapper.requireCheerActionType('sound_alert')
        assert result is CheerActionType.SOUND_ALERT

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withTimeoutString(self):
        result = await self.mapper.requireCheerActionType('timeout')
        assert result is CheerActionType.TIMEOUT

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withTntString(self):
        result = await self.mapper.requireCheerActionType('tnt')
        assert result is CheerActionType.AIR_STRIKE

    @pytest.mark.asyncio
    async def test_requireCheerActionType_withVoicemailString(self):
        result = await self.mapper.requireCheerActionType('voicemail')
        assert result is CheerActionType.VOICEMAIL

    @pytest.mark.asyncio
    async def test_requireTimeoutCheerActionTargetType_withAny(self):
        result = await self.mapper.requireTimeoutCheerActionTargetType('any')
        assert result is TimeoutCheerActionTargetType.ANY

    @pytest.mark.asyncio
    async def test_requireTimeoutCheerActionTargetType_withRandomOnly(self):
        result = await self.mapper.requireTimeoutCheerActionTargetType('random')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

        result = await self.mapper.requireTimeoutCheerActionTargetType('random only')
        assert result is TimeoutCheerActionTargetType.RANDOM_ONLY

    @pytest.mark.asyncio
    async def test_requireTimeoutCheerActionTargetType_withSpecificTargetOnly(self):
        result = await self.mapper.requireTimeoutCheerActionTargetType('specific')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.requireTimeoutCheerActionTargetType('specific target')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.requireTimeoutCheerActionTargetType('specific targets')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.requireTimeoutCheerActionTargetType('specific target only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

        result = await self.mapper.requireTimeoutCheerActionTargetType('specific targets only')
        assert result is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, CheerActionJsonMapper)
        assert isinstance(self.mapper, CheerActionJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withAirStrikeCheerAction(self):
        cheerAction = AirStrikeCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            maxDurationSeconds = 90,
            minDurationSeconds = 55,
            maxTimeoutChatters = 10,
            minTimeoutChatters = 3,
            twitchChannelId = 'abc123',
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 4

        assert dictionary['maxDurationSeconds'] == cheerAction.maxDurationSeconds
        assert dictionary['minDurationSeconds'] == cheerAction.minDurationSeconds
        assert dictionary['maxTimeoutChatters'] == cheerAction.maxTimeoutChatters
        assert dictionary['minTimeoutChatters'] == cheerAction.minTimeoutChatters

    @pytest.mark.asyncio
    async def test_serializeAbsCheerAction_withBeanChanceCheerAction(self):
        cheerAction: AbsCheerAction = BeanChanceCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 50,
            randomChance = 70,
            twitchChannelId = 'abc123',
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
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

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
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

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
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

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
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

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
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

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 3

        assert dictionary['durationSeconds'] == cheerAction.durationSeconds
        assert dictionary['randomChanceEnabled'] == cheerAction.isRandomChanceEnabled
        assert dictionary['targetType'] == await self.mapper.serializeTimeoutCheerActionTargetType(cheerAction.targetType)

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

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 3

        assert dictionary['durationSeconds'] == cheerAction.durationSeconds
        assert dictionary['randomChanceEnabled'] == cheerAction.isRandomChanceEnabled
        assert dictionary['targetType'] == await self.mapper.serializeTimeoutCheerActionTargetType(cheerAction.targetType)

    @pytest.mark.asyncio
    async def test_serializeCheerAction_withVoicemailCheerAction(self):
        cheerAction = VoicemailCheerAction(
            isEnabled = True,
            streamStatusRequirement = CheerActionStreamStatusRequirement.ANY,
            bits = 100,
            twitchChannelId = 'abc123'
        )

        result = await self.mapper.serializeAbsCheerAction(cheerAction)
        assert isinstance(result, str)

        dictionary = json.loads(result)
        assert isinstance(dictionary, dict)
        assert len(dictionary) == 0

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
    async def test_serializeCheerActionType_withAdge(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.ADGE)
        assert result == 'adge'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withAirStrike(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.AIR_STRIKE)
        assert result == 'air_strike'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withBeanChance(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.BEAN_CHANCE)
        assert result == 'bean_chance'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withCrowdControl(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.CROWD_CONTROL)
        assert result == 'crowd_control'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withGameShuffle(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.GAME_SHUFFLE)
        assert result == 'game_shuffle'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withSoundAlert(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.SOUND_ALERT)
        assert result == 'sound_alert'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withTimeout(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.TIMEOUT)
        assert result == 'timeout'

    @pytest.mark.asyncio
    async def test_serializeCheerActionType_withVoicemail(self):
        result = await self.mapper.serializeCheerActionType(CheerActionType.VOICEMAIL)
        assert result == 'voicemail'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionTargetType_withAny(self):
        result = await self.mapper.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.ANY)
        assert result == 'any'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionTargetType_withRandomOnly(self):
        result = await self.mapper.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.RANDOM_ONLY)
        assert result == 'random'

    @pytest.mark.asyncio
    async def test_serializeTimeoutCheerActionTargetType_withSpecificTargetOnly(self):
        result = await self.mapper.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY)
        assert result == 'specific'
