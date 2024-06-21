import json
import traceback
from json import JSONDecodeError
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.timeout.timeoutCheerActionEntry import \
    TimeoutCheerActionEntry
from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface


class TimeoutCheerActionJsonMapper(TimeoutCheerActionJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTimeoutCheerActionEntriesString(
        self,
        jsonString: str | Any | None
    ) -> list[TimeoutCheerActionEntry] | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: list[dict[str, Any] | Any | None] | Any | None = None

        try:
            jsonContents = json.loads(jsonString)
        except JSONDecodeError as e:
            self.__timber.log('TimeoutCheerActionJsonMapper', f'Encountered JSON decode exception when parsing timeout cheer action entries string into JSON ({jsonString=}): {e}', e, traceback.format_exc())
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

        return TimeoutCheerActionEntry(
            bitAmount = bitAmount,
            durationSeconds = durationSeconds,
            timedOutAtDateTime = timedOutAtDateTime,
            timedOutByUserId = timedOutByUserId
        )

    async def serializeTimeoutCheerActionEntriesToJsonString(
        self,
        entries: list[TimeoutCheerActionEntry] | None
    ) -> str | None:
        if entries is not None and not isinstance(entries, list):
            raise TypeError(f'entries argument is malformed: \"{entries}\"')

        if entries is None or len(entries) == 0:
            return None

        entryDictionaries: list[dict[str, Any]] = list()

        for index, entry in enumerate(entries):
            entryDictionary = await self.serializeTimeoutCheerActionEntry(entry)

            if entryDictionary is None:
                self.__timber.log('TimeoutCheerActionJsonMapper', f'Unable to serialize timeout cheer action entry value at index {index}: ({entry=})')
            else:
                entryDictionaries.append(entryDictionary)

        if len(entryDictionaries) == 0:
            return None

        return json.dumps(entryDictionaries)

    async def serializeTimeoutCheerActionEntry(
        self,
        entry: TimeoutCheerActionEntry | None
    ) -> dict[str, Any] | None:
        if entry is not None and not isinstance(entry, TimeoutCheerActionEntry):
            raise TypeError(f'entry argument is malformed: \"{entry}\"')

        if entry is None:
            return None

        return {
            'bitAmount': entry.bitAmount,
            'durationSeconds': entry.durationSeconds,
            'timedOutAtDateTime': entry.timedOutAtDateTime.isoformat(),
            'timedOutByUserId': entry.timedOutByUserId
        }
