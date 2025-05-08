import re
import traceback
from datetime import datetime, timezone
from typing import Any, Collection, Final, Pattern
from xml.etree.ElementTree import Element

from frozenlist import FrozenList
from lxml import etree
from lxml.etree import HTMLParser

from .eccoResponseParserInterface import EccoResponseParserInterface
from .models.eccoTimerData import EccoTimerData
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class EccoResponseParser(EccoResponseParserInterface):

    def __init__(
        self,
        timber: TimberInterface,
        baseUrl: str = 'https://www.eccothedolphin.com'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidUrl(baseUrl):
            raise TypeError(f'baseUrl argument is malformed: \"{baseUrl}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__baseUrl: Final[str] = baseUrl

        self.__htmlParser: Final[HTMLParser] = etree.HTMLParser(
            no_network = True,
            recover = True,
            remove_blank_text = True,
            remove_comments = True
        )

        self.__hoursMinutesSecondsRegEx: Final[Pattern] = re.compile(r'^(\d+):(\d+):(\d+)$', re.IGNORECASE)
        self.__minutesSecondsRegEx: Final[Pattern] = re.compile(r'^(\d+):(\d+)$', re.IGNORECASE)
        self.__secondsRegEx: Final[Pattern] = re.compile(r'^(\d+)$', re.IGNORECASE)
        self.__scriptSourceRegEx: Final[Pattern] = re.compile(r'page-\w+\.js$', re.IGNORECASE)
        self.__timerDateValueRegEx: Final[Pattern] = re.compile(r'new Date\("(.*?)"\)', re.IGNORECASE)

    async def findTimerDateValue(
        self,
        htmlString: str | Any | None
    ) -> datetime | None:
        if not utils.isValidStr(htmlString):
            return None

        match = self.__timerDateValueRegEx.search(htmlString)

        if match is None:
            return None

        dateTimeString = match.group(1)

        try:
            dateTime = datetime.strptime(dateTimeString, '%b %d, %Y %H:%M:%S')
        except Exception as e:
            self.__timber.log('EccoResponseParser', f'Unable to parse datetime ({match=}) ({dateTimeString=}): {e}', e, traceback.format_exc())
            return None

        return dateTime.replace(tzinfo = timezone.utc)

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

    async def parseTimerData(
        self,
        htmlString: str | Any | None
    ) -> EccoTimerData | None:
        if not utils.isValidStr(htmlString):
            return None

        result = etree.fromstring(
            text = htmlString,
            parser = self.__htmlParser
        )

        if result is None:
            self.__timber.log('EccoResponseParser', f'Unable to parse HTML contents ({result=})')
            return None

        h1Elements: Collection[Element] | Any | None = result.xpath('.//h1')

        if not isinstance(h1Elements, Collection):
            self.__timber.log('EccoResponseParser', f'Unable to find any H1 elements ({h1Elements=})')
            return None

        frozenH1Elements: FrozenList[Element] = FrozenList(h1Elements)
        frozenH1Elements.freeze()

        if len(frozenH1Elements) != 1:
            self.__timber.log('EccoResponseParser', f'Unable to find any H1 elements ({h1Elements=})')
            return None

        h1Element = frozenH1Elements[0]
        h1Text: str | Any | None = h1Element.text
        result = await self.__parseTextIntoTimerData(h1Text)

        if result is None:
            self.__timber.log('EccoResponseParser', f'Unable to parse timer text ({h1Element=}) ({h1Text=})')
            return None
        else:
            return result

    async def __parseTextIntoTimerData(
        self,
        text: str | Any | None
    ) -> EccoTimerData | None:
        if not utils.isValidStr(text):
            return None

        hoursMinutesSecondsMatch = self.__hoursMinutesSecondsRegEx.fullmatch(text)
        minutesSecondsMatch = self.__minutesSecondsRegEx.fullmatch(text)
        secondsMatch = self.__secondsRegEx.fullmatch(text)

        hours: int | None = None
        minutes: int | None = None
        seconds: int | None = None

        if hoursMinutesSecondsMatch is not None:
            hours = int(hoursMinutesSecondsMatch.group(1))
            minutes = int(hoursMinutesSecondsMatch.group(2))
            seconds = int(hoursMinutesSecondsMatch.group(3))
        elif minutesSecondsMatch is not None:
            hours = 0
            minutes = int(minutesSecondsMatch.group(1))
            seconds = int(minutesSecondsMatch.group(2))
        elif secondsMatch is not None:
            hours = 0
            minutes = 0
            seconds = int(secondsMatch.group(1))

        if hours is None or minutes is None or seconds is None:
            return None
        else:
            return EccoTimerData(
                hours = hours,
                minutes = minutes,
                seconds = seconds,
                rawText = text
            )
