import json
from typing import Any

from .absCheerAction import AbsCheerAction
from .beanChanceCheerAction import BeanChanceCheerAction
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .crowdControl.crowdControlButtonPressCheerAction import CrowdControlButtonPressCheerAction
from .crowdControl.crowdControlGameShuffleCheerAction import CrowdControlGameShuffleCheerAction
from .soundAlertCheerAction import SoundAlertCheerAction
from .timeoutCheerAction import TimeoutCheerAction
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class CheerActionJsonMapper(CheerActionJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

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
            key = 'randomChance',
        )

        return BeanChanceCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            randomChance = randomChance,
            twitchChannelId = twitchChannelId
        )

    async def __parseButtonPressCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonContents: dict[str, Any],
        twitchChannelId: str
    ) -> CrowdControlButtonPressCheerAction:
        return CrowdControlButtonPressCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

    async def parseCheerActionStreamStatusRequirement(
        self,
        jsonString: str | None
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
        jsonString: str | None
    ) -> CheerActionType | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'bean_chance': return CheerActionType.BEAN_CHANCE
            case 'crowd_control': return CheerActionType.CROWD_CONTROL
            case 'game_shuffle': return CheerActionType.GAME_SHUFFLE
            case 'sound_alert': return CheerActionType.SOUND_ALERT
            case 'timeout': return CheerActionType.TIMEOUT
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
    ) -> CrowdControlGameShuffleCheerAction:
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
            fallback = 0
        )

        if durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            self.__timber.log('CheerActionJsonMapper', f'Unable to read in \"durationSeconds\" value from timeout cheer action JSON ({durationSeconds=}) ({jsonContents=})')
            return None

        return TimeoutCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            durationSeconds = durationSeconds,
            twitchChannelId = twitchChannelId
        )

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
        jsonString: str | None
    ) -> CheerActionStreamStatusRequirement:
        streamStatusRequirement = await self.parseCheerActionStreamStatusRequirement(jsonString)

        if streamStatusRequirement is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionStreamStatusRequirement value!')

        return streamStatusRequirement

    async def requireCheerActionType(
        self,
        jsonString: str | None
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

    async def serializeAbsCheerAction(
        self,
        cheerAction: AbsCheerAction
    ) -> str:
        if not isinstance(cheerAction, AbsCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        if isinstance(cheerAction, BeanChanceCheerAction):
            return await self.__serializeBeanChanceCheerAction(cheerAction)
        elif isinstance(cheerAction, CrowdControlButtonPressCheerAction):
            return await self.__serializeCrowdControlButtonPressCheerAction(cheerAction)
        elif isinstance(cheerAction, CrowdControlGameShuffleCheerAction):
            return await self.__serializeCrowdControlGameShuffleCheerAction(cheerAction)
        elif isinstance(cheerAction, SoundAlertCheerAction):
            return await self.__serializeSoundAlertCheerAction(cheerAction)
        elif isinstance(cheerAction, TimeoutCheerAction):
            return await self.__serializeTimeoutCheerAction(cheerAction)
        else:
            raise RuntimeError(f'Encountered unknown AbsCheerAction type ({cheerAction=})')

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
            case CheerActionType.BEAN_CHANCE: return 'bean_chance'
            case CheerActionType.CROWD_CONTROL: return 'crowd_control'
            case CheerActionType.GAME_SHUFFLE: return 'game_shuffle'
            case CheerActionType.SOUND_ALERT: return 'sound_alert'
            case CheerActionType.TIMEOUT: return 'timeout'
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

        jsonContents: dict[str, Any] = {
            'durationSeconds': cheerAction.durationSeconds
        }

        return json.dumps(jsonContents)
