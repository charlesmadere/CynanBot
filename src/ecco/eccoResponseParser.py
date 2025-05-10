import re
import traceback
from datetime import datetime
from typing import Any, Collection, Final, Pattern
from xml.etree.ElementTree import Element

from frozenlist import FrozenList
from lxml import etree
from lxml.etree import HTMLParser

from .eccoResponseParserInterface import EccoResponseParserInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class EccoResponseParser(EccoResponseParserInterface):

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

        self.__htmlParser: Final[HTMLParser] = etree.HTMLParser(
            no_network = True,
            recover = True,
            remove_blank_text = True,
            remove_comments = True
        )

        self.__scriptSourceRegEx: Final[Pattern] = re.compile(r'page-\w+\.js$', re.IGNORECASE)
        self.__timerDateValueRegEx: Final[Pattern] = re.compile(r'new Date\("(.*?)"\)', re.IGNORECASE)

    async def findTimerDateTimeValue(
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

        return dateTime.replace(tzinfo = self.__timeZoneRepository.getDefault())

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
