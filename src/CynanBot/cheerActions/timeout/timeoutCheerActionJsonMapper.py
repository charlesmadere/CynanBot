import json
from json import JSONDecodeError
import traceback
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.timeout.timeoutCheerActionEntry import TimeoutCheerActionEntry
from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface


class TimeoutCheerActionJsonMapper(TimeoutCheerActionJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTimeoutCheerActionEntry(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TimeoutCheerActionEntry | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        bitAmount = utils.getIntFromDict(jsonContents, 'bitAmount')
        durationSeconds = utils.getIntFromDict(jsonContents, 'durationSeconds')
        timedOutAtDateTime = utils.getDateTimeFromDict(jsonContents, 'timedOutAtDateTime')
        timedOutByUserId = utils.getStrFromDict(jsonContents, 'timedOutByUserId')
        timedOutByUserName = utils.getStrFromDict(jsonContents, 'timedOutByUserName')

        return TimeoutCheerActionEntry(
            bitAmount = bitAmount,
            durationSeconds = durationSeconds,
            timedOutAtDateTime = timedOutAtDateTime,
            timedOutByUserId = timedOutByUserId,
            timedOutByUserName = timedOutByUserName
        )

    async def parseTimeoutCheerActionEntriesString(
        self,
        string: str | Any | None
    ) -> list[TimeoutCheerActionEntry] | None:
        if not utils.isValidStr(string):
            return None

        jsonContents: list[dict[str, Any] | Any | None] | Any | None = None

        try:
            jsonContents = json.loads(string)
        except JSONDecodeError as e:
            self.__timber.log('TimeoutCheerActionJsonMapper', f'Encountered JSON decode exception when parsing timeout cheer action entries string into JSON ({string=}): {e}', e, traceback.format_exc())
            return None

        entries: list[TimeoutCheerActionEntry] = list()

        if isinstance(jsonContents, list) and len(jsonContents) >= 1:
            for index, entryJson in enumerate(jsonContents):
                entry = await self.parseTimeoutCheerActionEntry(entryJson)

                if entry is None:
                    self.__timber.log('TimeoutCheerActionJsonMapper', f'Unable to parse timeout cheer action entry value at index {index}: ({entryJson=})')
                else:
                    entries.append(entry)

        if len(entries) == 0:
            return None

        entries.sort(key = lambda entry: entry.timedOutAtDateTime, reverse = True)
        return entries
