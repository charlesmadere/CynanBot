import re
import traceback
from dataclasses import dataclass
from datetime import datetime, tzinfo
from typing import Any, Collection, Final, Pattern
from xml.etree.ElementTree import Element

from frozendict import frozendict
from frozenlist import FrozenList
from lxml import etree
from lxml.etree import HTMLParser

from .eccoResponseParserInterface import EccoResponseParserInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class EccoResponseParser(EccoResponseParserInterface):

    @dataclass(frozen = True)
    class CleanedDateTimeInfo:
        dateTimeString: str
        timeZone: tzinfo

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        baseUrl: str = 'https://www.eccothedolphin.com'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidUrl(baseUrl):
            raise TypeError(f'baseUrl argument is malformed: \"{baseUrl}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__baseUrl: Final[str] = baseUrl

        self.__timeZoneAbbreviationToTimeZoneName: Final[frozendict[str, str | None]] = frozendict({
            'CDT': 'America/Chicago',
            'CST': 'America/Chicago',
            'EDT': 'America/New_York',
            'EST': 'America/New_York',
            'PDT': 'America/Los_Angeles',
            'PST': 'America/Los_Angeles'
        })

        self.__htmlParser: Final[HTMLParser] = etree.HTMLParser(
            no_network = True,
            recover = True,
            remove_blank_text = True,
            remove_comments = True
        )

        self.__dateTimeAndTimeZoneRegEx: Final[Pattern] = re.compile(r'^(.+?)(?:\s+([a-z]{2,3}))?\s*$', re.IGNORECASE)
        self.__scriptSourceRegEx: Final[Pattern] = re.compile(r'page-\w+\.js$', re.IGNORECASE)
        self.__scriptTimerRegEx: Final[Pattern] = re.compile(r'new Date\("(.*?)"\)', re.IGNORECASE)

    async def findTimerDateTimeValue(
        self,
        scriptString: str | Any | None
    ) -> datetime | None:
        if not utils.isValidStr(scriptString):
            return None

        scriptTimerMatch = self.__scriptTimerRegEx.search(scriptString)

        if scriptTimerMatch is None:
            self.__timber.log('EccoResponseParser', f'Unable to find script timer match ({scriptTimerMatch=})')
            return None

        cleanedDateTimeInfo = await self.__cleanDateTimeInfo(scriptTimerMatch.group(1))

        if cleanedDateTimeInfo is None:
            self.__timber.log('EccoResponseParser', f'Unable to clean date time info ({scriptTimerMatch=}) ({cleanedDateTimeInfo=})')
            return None

        try:
            dateTime = datetime.strptime(cleanedDateTimeInfo.dateTimeString, '%b %d, %Y %H:%M:%S')
        except Exception as e:
            self.__timber.log('EccoResponseParser', f'Unable to parse datetime ({scriptTimerMatch=}) ({cleanedDateTimeInfo=}): {e}', e, traceback.format_exc())
            return None

        return dateTime.replace(tzinfo = cleanedDateTimeInfo.timeZone)

    async def findTimerScriptSource(
        self,
        htmlString: str | Any | None
    ) -> str | None:
        if not utils.isValidStr(htmlString):
            return None

        result = etree.fromstring(
            text = htmlString,
            parser = self.__htmlParser,
            base_url = self.__baseUrl
        )

        if result is None:
            self.__timber.log('EccoResponseParser', f'Unable to parse HTML contents ({result=})')
            return None

        scriptElements: Collection[Element] | Any | None = result.xpath('.//script')

        if not isinstance(scriptElements, Collection):
            self.__timber.log('EccoResponseParser', f'Unable to find any script elements ({scriptElements=})')
            return None

        frozenScriptElements: FrozenList[Element] = FrozenList(scriptElements)
        frozenScriptElements.freeze()

        if len(frozenScriptElements) == 0:
            self.__timber.log('EccoResponseParser', f'Unable to find any script elements ({scriptElements=})')
            return None

        for scriptElement in scriptElements:
            scriptSrc: str | Any | None = scriptElement.get('src', None)

            if utils.isValidStr(scriptSrc) and self.__scriptSourceRegEx.search(scriptSrc):
                return f'{self.__baseUrl}{scriptSrc}'

        return None

    async def __cleanDateTimeInfo(self, scriptTimer: str | None) -> CleanedDateTimeInfo | None:
        if not utils.isValidStr(scriptTimer):
            return None

        dateTimeAndTimeZoneZoneMatch = self.__dateTimeAndTimeZoneRegEx.fullmatch(scriptTimer)

        if dateTimeAndTimeZoneZoneMatch is None:
            return None

        dateTimeString = dateTimeAndTimeZoneZoneMatch.group(1)
        timeZoneAbbreviation: str | None = dateTimeAndTimeZoneZoneMatch.group(2)
        timeZone = await self.__determineTimeZone(timeZoneAbbreviation)

        return EccoResponseParser.CleanedDateTimeInfo(
            dateTimeString = dateTimeString,
            timeZone = timeZone
        )

    async def __determineTimeZone(
        self,
        timeZoneAbbreviation: str | Any | None
    ) -> tzinfo:
        if utils.isValidStr(timeZoneAbbreviation):
            fullTimeZoneName = self.__timeZoneAbbreviationToTimeZoneName.get(timeZoneAbbreviation, None)

            if utils.isValidStr(fullTimeZoneName):
                return self.__timeZoneRepository.getTimeZone(fullTimeZoneName)

        return self.__timeZoneRepository.getDefault()
