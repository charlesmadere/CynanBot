import json
import traceback
from json import JSONDecodeError
from typing import Any

from frozenlist import FrozenList

from .timeoutActionHistoryEntry import TimeoutActionHistoryEntry
from .timeoutActionJsonMapperInterface import TimeoutActionJsonMapperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class TimeoutActionJsonMapper(TimeoutActionJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTimeoutActionEntriesString(
        self,
        jsonString: str | Any | None
    ) -> FrozenList[TimeoutActionHistoryEntry] | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonList: list[dict[str, Any] | Any | None] | Any | None

        try:
            jsonList = json.loads(jsonString)
        except JSONDecodeError as e:
            self.__timber.log('TimeoutActionJsonMapper', f'Encountered JSON decode exception when parsing timeout action entries string into JSON ({jsonString=}): {e}', e, traceback.format_exc())
            return None

        if not isinstance(jsonList, list) or len(jsonList) == 0:
            return None

        entries: list[TimeoutActionHistoryEntry] = list()

        for index, entryJson in enumerate(jsonList):
            entry = await self.parseTimeoutActionEntry(entryJson)

            if entry is None:
                self.__timber.log('TimeoutActionJsonMapper', f'Unable to parse timeout action entry value at index {index}: ({entryJson=})')
            else:
                entries.append(entry)

        if len(entries) == 0:
            return None

        entries.sort(key = lambda entry: entry.timedOutAtDateTime, reverse = True)
        frozenEntries: FrozenList[TimeoutActionHistoryEntry] = FrozenList(entries)
        frozenEntries.freeze()

        return frozenEntries

    async def parseTimeoutActionEntry(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TimeoutActionHistoryEntry | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        durationSeconds = utils.getIntFromDict(jsonContents, 'durationSeconds')
        timedOutAtDateTime = utils.getDateTimeFromDict(jsonContents, 'timedOutAtDateTime')
        timedOutByUserId = utils.getStrFromDict(jsonContents, 'timedOutByUserId')

        return TimeoutActionHistoryEntry(
            durationSeconds = durationSeconds,
            timedOutAtDateTime = timedOutAtDateTime,
            timedOutByUserId = timedOutByUserId
        )

    async def serializeTimeoutActionEntriesToJsonString(
        self,
        entries: list[TimeoutActionHistoryEntry] | None
    ) -> str | None:
        if entries is not None and not isinstance(entries, list):
            raise TypeError(f'entries argument is malformed: \"{entries}\"')

        if entries is None or len(entries) == 0:
            return None

        entryDictionaries: list[dict[str, Any]] = list()

        for index, entry in enumerate(entries):
            entryDictionary = await self.serializeTimeoutActionEntry(entry)

            if entryDictionary is None:
                self.__timber.log('TimeoutActionJsonMapper', f'Unable to serialize timeout action entry value at index {index}: ({entry=})')
            else:
                entryDictionaries.append(entryDictionary)

        if len(entryDictionaries) == 0:
            return None

        return json.dumps(entryDictionaries)

    async def serializeTimeoutActionEntry(
        self,
        entry: TimeoutActionHistoryEntry | None
    ) -> dict[str, Any] | None:
        if entry is not None and not isinstance(entry, TimeoutActionHistoryEntry):
            raise TypeError(f'entry argument is malformed: \"{entry}\"')

        if entry is None:
            return None

        return {
            'durationSeconds': entry.durationSeconds,
            'timedOutAtDateTime': entry.timedOutAtDateTime.isoformat(),
            'timedOutByUserId': entry.timedOutByUserId
        }
