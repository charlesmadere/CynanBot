import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionJsonMapperInterface import \
    CheerActionJsonMapperInterface
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.timber.timberInterface import TimberInterface


class CheerActionJsonMapper(CheerActionJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

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
            case 'sound_alert': return CheerActionType.SOUND_ALERT
            case 'timeout': return CheerActionType.TIMEOUT
            case _:
                self.__timber.log('CheerActionJsonMapper', f'Encountered unknown CheerActionType value: \"{jsonString}\"')
                return None

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
            case CheerActionType.SOUND_ALERT: return 'sound_alert'
            case CheerActionType.TIMEOUT: return 'timeout'
            case _: raise ValueError(f'The given CheerActionType value is unknown: \"{actionType}\"')
