from .absCheerAction import AbsCheerAction
from .beanChanceCheerAction import BeanChanceCheerAction
from .cheerActionBitRequirement import CheerActionBitRequirement
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
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
        twitchChannel: str,
        twitchChannelId: str
    ) -> BeanChanceCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] | None = json.loads(jsonString)

        randomChance = utils.getIntFromDict(
            d = jsonContents,
            key = 'randomChance',
            fallback = 0
        )

        if randomChance < 0 or randomChance > 100:
            self.__timber.log('CheerActionJsonMapper', f'Unable to read in \"randomChance\" value from bean chance cheer action JSON ({randomChance=}) ({jsonContents=})')
            return None

        return BeanChanceCheerAction(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            randomChance = randomChance,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def parseCheerActionBitRequirement(
        self,
        jsonString: str | None
    ) -> CheerActionBitRequirement | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'exact': return CheerActionBitRequirement.EXACT
            case 'greater_than_or_equal_to': return CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO
            case _:
                self.__timber.log('CheerActionJsonMapper', f'Encountered unknown CheerActionBitRequirement value: \"{jsonString}\"')
                return None

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
            case 'sound_alert': return CheerActionType.SOUND_ALERT
            case 'timeout': return CheerActionType.TIMEOUT
            case _:
                self.__timber.log('CheerActionJsonMapper', f'Encountered unknown CheerActionType value: \"{jsonString}\"')
                return None

    async def parseSoundAlertCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SoundAlertCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] | None = json.loads(jsonString)

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
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def parseTimeoutCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TimeoutCheerAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] | None = json.loads(jsonString)

        durationSeconds = utils.getStrFromDict(
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
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def requireCheerActionBitRequirement(
        self,
        jsonString: str | None
    ) -> CheerActionBitRequirement:
        bitRequirement = await self.parseCheerActionBitRequirement(jsonString)

        if bitRequirement is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionBitRequirement value!')

        return bitRequirement

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

    async def serializeAbsCheerAction(
        self,
        cheerAction: AbsCheerAction
    ) -> str:
        if not isinstance(cheerAction, AbsCheerAction):
            raise TypeError(f'cheerAction argument is malformed: \"{cheerAction}\"')

        if isinstance(cheerAction, BeanChanceCheerAction):
            return await self.__serializeBeanChanceCheerAction(cheerAction)
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

    async def serializeCheerActionBitRequirement(
        self,
        bitRequirement: CheerActionBitRequirement
    ) -> str:
        if not isinstance(bitRequirement, CheerActionBitRequirement):
            raise TypeError(f'bitRequirement argument is malformed: \"{bitRequirement}\"')

        match bitRequirement:
            case CheerActionBitRequirement.EXACT: return 'exact'
            case CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO: return 'greater_than_or_equal_to'
            case _: raise ValueError(f'The given CheerActionBitRequirement value is unknown: \"{bitRequirement}\"')

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
            case CheerActionType.SOUND_ALERT: return 'sound_alert'
            case CheerActionType.TIMEOUT: return 'timeout'
            case _: raise ValueError(f'The given CheerActionType value is unknown: \"{actionType}\"')

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
