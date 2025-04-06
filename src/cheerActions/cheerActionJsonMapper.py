import json
import re
from typing import Any, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .absCheerAction import AbsCheerAction
from .adge.adgeCheerAction import AdgeCheerAction
from .beanChance.beanChanceCheerAction import BeanChanceCheerAction
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .crowdControl.crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from .crowdControl.crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from .soundAlert.soundAlertCheerAction import SoundAlertCheerAction
from .timeout.timeoutCheerAction import TimeoutCheerAction
from .timeout.timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from .tnt.tntCheerAction import TntCheerAction
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class CheerActionJsonMapper(CheerActionJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__timeoutCheerActionTargetTypeRegExes = self.__createTimeoutCheerActionTargetTypeRegExes()

    def __createTimeoutCheerActionTargetTypeRegExes(self) -> frozendict[TimeoutCheerActionTargetType, FrozenList[Pattern]]:
        anyRegExes: FrozenList[Pattern] = FrozenList()
        anyRegExes.append(re.compile(r'^\s*any\s*$', re.IGNORECASE))
        anyRegExes.freeze()

        randomRegExes: FrozenList[Pattern] = FrozenList()
        randomRegExes.append(re.compile(r'^\s*random\s*$', re.IGNORECASE))
        randomRegExes.append(re.compile(r'^\s*random\s*only\s*$', re.IGNORECASE))
        randomRegExes.freeze()

        specificTargetOnlyRegExes: FrozenList[Pattern] = FrozenList()
        specificTargetOnlyRegExes.append(re.compile(r'^\s*specific\s*$', re.IGNORECASE))
        specificTargetOnlyRegExes.append(re.compile(r'^\s*specific\s*targets?\s*$', re.IGNORECASE))
        specificTargetOnlyRegExes.append(re.compile(r'^\s*specific\s*targets?\s*only\s*$', re.IGNORECASE))
        specificTargetOnlyRegExes.freeze()

        return frozendict({
            TimeoutCheerActionTargetType.ANY: anyRegExes,
            TimeoutCheerActionTargetType.RANDOM_ONLY: randomRegExes,
            TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY: specificTargetOnlyRegExes
        })

    async def parseAdgeCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> AdgeCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        adgeLengthSeconds = utils.getIntFromDict(
            d = jsonContents,
            key = 'adgeLengthSeconds',
            fallback = 30
        )

        return AdgeCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            adgeLengthSeconds = adgeLengthSeconds,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

    async def parseBeanChanceCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> BeanChanceCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        randomChance = utils.getIntFromDict(
            d = jsonContents,
            key = 'randomChance'
        )

        return BeanChanceCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            randomChance = randomChance,
            twitchChannelId = twitchChannelId
        )

    async def parseCheerActionStreamStatusRequirement(
        self,
        jsonString: str | Any | None
    ) -> CheerActionStreamStatusRequirement | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'any': return CheerActionStreamStatusRequirement.ANY
            case 'offline': return CheerActionStreamStatusRequirement.OFFLINE
            case 'online': return CheerActionStreamStatusRequirement.ONLINE
            case _:
                self.__timber.log('CheerActionJsonMapper', f'Encountered unknown CheerActionStreamStatusRequirement value: \"{jsonString}\"')
                return None

    async def parseCheerActionType(
        self,
        jsonString: str | Any | None
    ) -> CheerActionType | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'adge': return CheerActionType.ADGE
            case 'bean_chance': return CheerActionType.BEAN_CHANCE
            case 'crowd_control': return CheerActionType.CROWD_CONTROL
            case 'game_shuffle': return CheerActionType.GAME_SHUFFLE
            case 'sound_alert': return CheerActionType.SOUND_ALERT
            case 'timeout': return CheerActionType.TIMEOUT
            case 'tnt': return CheerActionType.TNT
            case _:
                self.__timber.log('CheerActionJsonMapper', f'Encountered unknown CheerActionType value: \"{jsonString}\"')
                return None

    async def parseCrowdControlButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlButtonPressCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        return CrowdControlButtonPressCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

    async def parseCrowdControlGameShuffleCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlGameShuffleCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        gigaShuffleChance: int | None = None
        if 'gigaShuffleChance' in jsonContents and utils.isValidInt(jsonContents.get('gigaShuffleChance')):
            gigaShuffleChance = utils.getIntFromDict(jsonContents, 'gigaShuffleChance')

        return CrowdControlGameShuffleCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            gigaShuffleChance = gigaShuffleChance,
            twitchChannelId = twitchChannelId
        )

    async def parseSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> SoundAlertCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        directory = utils.getStrFromDict(
            d = jsonContents,
            key = 'directory',
            fallback = ''
        )

        if not utils.isValidStr(directory):
            self.__timber.log('CheerActionJsonMapper', f'Unable to read in \"directory\" value from sound alert cheer action JSON ({directory=}) ({jsonContents=})')
            return None

        return SoundAlertCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            directory = directory,
            twitchChannelId = twitchChannelId
        )

    async def parseTimeoutCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        durationSeconds = utils.getIntFromDict(
            d = jsonContents,
            key = 'durationSeconds',
            fallback = 60
        )

        isRandomChanceEnabled = utils.getBoolFromDict(
            d = jsonContents,
            key = 'randomChanceEnabled',
            fallback = True
        )

        targetTypeString = utils.getStrFromDict(
            d = jsonContents,
            key = 'targetType',
            fallback = await self.serializeTimeoutCheerActionTargetType(TimeoutCheerActionTargetType.ANY)
        )

        targetType = await self.requireTimeoutCheerActionTargetType(targetTypeString)

        return TimeoutCheerAction(
            isEnabled = isEnabled,
            isRandomChanceEnabled = isRandomChanceEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            durationSeconds = durationSeconds,
            twitchChannelId = twitchChannelId,
            targetType = targetType
        )

    async def parseTimeoutCheerActionTargetType(
        self,
        string: str | Any | None
    ) -> TimeoutCheerActionTargetType | None:
        if not utils.isValidStr(string):
            return None

        for timeoutCheerActionTargetType, regExes in self.__timeoutCheerActionTargetTypeRegExes.items():
            for regEx in regExes:
                if regEx.fullmatch(string) is not None:
                    return timeoutCheerActionTargetType

        return None

    async def parseTntCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> TntCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] = json.loads(jsonString)

        maxDurationSeconds = utils.getIntFromDict(
            d = jsonContents,
            key = 'maxDurationSeconds',
            fallback = 60
        )

        minDurationSeconds = utils.getIntFromDict(
            d = jsonContents,
            key = 'minDurationSeconds',
            fallback = 60
        )

        maxTimeoutChatters = utils.getIntFromDict(
            d = jsonContents,
            key = 'maxTimeoutChatters',
            fallback = 10
        )

        minTimeoutChatters = utils.getIntFromDict(
            d = jsonContents,
            key = 'minTimeoutChatters',
            fallback = 3
        )

        return TntCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            maxDurationSeconds = maxDurationSeconds,
            minDurationSeconds = minDurationSeconds,
            maxTimeoutChatters = maxTimeoutChatters,
            minTimeoutChatters = minTimeoutChatters,
            twitchChannelId = twitchChannelId
        )

    async def requireAdgeCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> AdgeCheerAction:
        action = await self.parseAdgeCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create AdgeCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireBeanChanceCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> BeanChanceCheerAction:
        action = await self.parseBeanChanceCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create BeanChanceCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireCheerActionStreamStatusRequirement(
        self,
        jsonString: str | Any | None
    ) -> CheerActionStreamStatusRequirement:
        streamStatusRequirement = await self.parseCheerActionStreamStatusRequirement(jsonString)

        if streamStatusRequirement is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionStreamStatusRequirement value!')

        return streamStatusRequirement

    async def requireCheerActionType(
        self,
        jsonString: str | Any | None
    ) -> CheerActionType:
        actionType = await self.parseCheerActionType(jsonString)

        if actionType is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionType value!')

        return actionType

    async def requireCrowdControlButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlButtonPressCheerAction:
        action = await self.parseCrowdControlButtonPressCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create CrowdControlButtonPressCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireCrowdControlGameShuffleCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> CrowdControlGameShuffleCheerAction:
        action = await self.parseCrowdControlGameShuffleCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create CrowdControlGameShuffleCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> SoundAlertCheerAction:
        action = await self.parseSoundAlertCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create SoundAlertCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireTimeoutCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerAction:
        action = await self.parseTimeoutCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create TimeoutCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def requireTimeoutCheerActionTargetType(
        self,
        string: str | Any | None
    ) -> TimeoutCheerActionTargetType:
        targetType = await self.parseTimeoutCheerActionTargetType(string)

        if targetType is None:
            raise ValueError(f'Unable to parse \"{string}\" into TimeoutCheerActionTargetType value!')

        return targetType

    async def requireTntCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannelId: str
    ) -> TntCheerAction:
        action = await self.parseTntCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            jsonString = jsonString,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise ValueError(f'Unable to create TntCheerAction! ({isEnabled=}) ({streamStatusRequirement=}) ({bits=}) ({jsonString=}) ({twitchChannelId=})')

        return action

    async def serializeAbsCheerAction(
        self,
        cheerAction: AbsCheerAction
    ) -> str:
        if not isinstance(cheerAction, AbsCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        if isinstance(cheerAction, AdgeCheerAction):
            return await self.__serializeAdgeCheerAction(cheerAction)
        elif isinstance(cheerAction, BeanChanceCheerAction):
            return await self.__serializeBeanChanceCheerAction(cheerAction)
        elif isinstance(cheerAction, CrowdControlButtonPressCheerAction):
            return await self.__serializeCrowdControlButtonPressCheerAction(cheerAction)
        elif isinstance(cheerAction, CrowdControlGameShuffleCheerAction):
            return await self.__serializeCrowdControlGameShuffleCheerAction(cheerAction)
        elif isinstance(cheerAction, SoundAlertCheerAction):
            return await self.__serializeSoundAlertCheerAction(cheerAction)
        elif isinstance(cheerAction, TimeoutCheerAction):
            return await self.__serializeTimeoutCheerAction(cheerAction)
        elif isinstance(cheerAction, TntCheerAction):
            return await self.__serializeTntCheerAction(cheerAction)
        else:
            raise RuntimeError(f'Encountered unknown AbsCheerAction type ({cheerAction=})')

    async def __serializeAdgeCheerAction(
        self,
        cheerAction: AdgeCheerAction
    ) -> str:
        if not isinstance(cheerAction, AdgeCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = {
            'adgeLengthSeconds': cheerAction.adgeLengthSeconds
        }

        return json.dumps(jsonContents)

    async def __serializeBeanChanceCheerAction(
        self,
        cheerAction: BeanChanceCheerAction
    ) -> str:
        if not isinstance(cheerAction, BeanChanceCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = {
            'randomChance': cheerAction.randomChance
        }

        return json.dumps(jsonContents)

    async def serializeCheerActionStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement
    ) -> str:
        if not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')

        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ANY: return 'any'
            case CheerActionStreamStatusRequirement.OFFLINE: return 'offline'
            case CheerActionStreamStatusRequirement.ONLINE: return 'online'
            case _: raise ValueError(f'The given CheerActionStreamStatusRequirement value is unknown: \"{streamStatusRequirement}\"')

    async def serializeCheerActionType(
        self,
        actionType: CheerActionType
    ) -> str:
        if not isinstance(actionType, CheerActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')

        match actionType:
            case CheerActionType.ADGE: return 'adge'
            case CheerActionType.BEAN_CHANCE: return 'bean_chance'
            case CheerActionType.CROWD_CONTROL: return 'crowd_control'
            case CheerActionType.GAME_SHUFFLE: return 'game_shuffle'
            case CheerActionType.SOUND_ALERT: return 'sound_alert'
            case CheerActionType.TIMEOUT: return 'timeout'
            case CheerActionType.TNT: return 'tnt'
            case _: raise ValueError(f'The given CheerActionType value is unknown: \"{actionType}\"')

    async def __serializeCrowdControlButtonPressCheerAction(
        self,
        cheerAction: CrowdControlButtonPressCheerAction
    ) -> str:
        if not isinstance(cheerAction, CrowdControlButtonPressCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = dict()
        return json.dumps(jsonContents)

    async def __serializeCrowdControlGameShuffleCheerAction(
        self,
        cheerAction: CrowdControlGameShuffleCheerAction
    ) -> str:
        if not isinstance(cheerAction, CrowdControlGameShuffleCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = dict()

        if utils.isValidInt(cheerAction.gigaShuffleChance):
            jsonContents['gigaShuffleChance'] = cheerAction.gigaShuffleChance

        return json.dumps(jsonContents)

    async def __serializeSoundAlertCheerAction(
        self,
        cheerAction: SoundAlertCheerAction
    ) -> str:
        if not isinstance(cheerAction, SoundAlertCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = {
            'directory': cheerAction.directory
        }

        return json.dumps(jsonContents)

    async def __serializeTimeoutCheerAction(
        self,
        cheerAction: TimeoutCheerAction
    ) -> str:
        if not isinstance(cheerAction, TimeoutCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        targetTypeString = await self.serializeTimeoutCheerActionTargetType(cheerAction.targetType)

        jsonContents: dict[str, Any] = {
            'durationSeconds': cheerAction.durationSeconds,
            'randomChanceEnabled': cheerAction.isRandomChanceEnabled,
            'targetType': targetTypeString
        }

        return json.dumps(jsonContents)

    async def serializeTimeoutCheerActionTargetType(
        self,
        targetType: TimeoutCheerActionTargetType
    ) -> str:
        if not isinstance(targetType, TimeoutCheerActionTargetType):
            raise TypeError(f'targetType argument is malformed: \"{targetType}\"')

        match targetType:
            case TimeoutCheerActionTargetType.ANY: return 'any'
            case TimeoutCheerActionTargetType.RANDOM_ONLY: return 'random'
            case TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY: return 'specific'
            case _: raise ValueError(f'The given TimeoutCheerActionTargetType value is unknown: \"{targetType}\"')

    async def __serializeTntCheerAction(
        self,
        cheerAction: TntCheerAction
    ) -> str:
        if not isinstance(cheerAction, TntCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        jsonContents: dict[str, Any] = {
            'maxDurationSeconds': cheerAction.maxDurationSeconds,
            'minDurationSeconds': cheerAction.minDurationSeconds,
            'maxTimeoutChatters': cheerAction.maxTimeoutChatters,
            'minTimeoutChatters': cheerAction.minTimeoutChatters
        }

        return json.dumps(jsonContents)
