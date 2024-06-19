from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionJsonMapperInterface import \
    CheerActionJsonMapperInterface
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.timber.timberInterface import TimberInterface


class CheerActionJsonMapper(CheerActionJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

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

    async def requireCheerActionType(
        self,
        jsonString: str | None
    ) -> CheerActionType:
        actionType = await self.parseCheerActionType(jsonString)

        if actionType is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into CheerActionType value!')

        return actionType

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
