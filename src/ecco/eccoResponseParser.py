import re
import traceback
from datetime import datetime
from typing import Any, Collection, Final, Pattern
from xml.etree.ElementTree import Element

from frozenlist import FrozenList
from lxml import etree
from lxml.etree import HTMLParser

from .eccoConstants import EccoConstants
from .eccoResponseParserInterface import EccoResponseParserInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class EccoResponseParser(EccoResponseParserInterface):

    def __init__(
        self,
        eccoConstants: EccoConstants,
        timber: TimberInterface,
    ):
        if not isinstance(eccoConstants, EccoConstants):
            raise TypeError(f'eccoConstants argument is malformed: \"{eccoConstants}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eccoConstants: Final[EccoConstants] = eccoConstants
        self.__timber: Final[TimberInterface] = timber

        self.__htmlParser: Final[HTMLParser] = etree.HTMLParser(
            no_network = True,
            recover = True,
            remove_blank_text = True,
            remove_comments = True,
        )

        self.__dateTimeAndTimeZoneRegEx: Final[Pattern] = re.compile(r'^(.+?)(?:\s+([a-z]{2,3}))?\s*$', re.IGNORECASE)
        self.__scriptSourceRegEx: Final[Pattern] = re.compile(r'page-\w+\.js$', re.IGNORECASE)
        self.__scriptTimerRegEx: Final[Pattern] = re.compile(r'new Date\(\"(.*?)\"\);')

    async def findTimerDateTimeValue(
        self,
        scriptString: str | Any | None,
    ) -> datetime | None:
        if not utils.isValidStr(scriptString):
            return None

        scriptTimerMatch = self.__scriptTimerRegEx.search(scriptString)

        if scriptTimerMatch is None:
            self.__timber.log('EccoResponseParser', f'Unable to find script timer match ({scriptTimerMatch=})')
            return None

        scriptTimerString = scriptTimerMatch.group(1)

        if not utils.isValidStr(scriptTimerString):
            self.__timber.log('EccoResponseParser', f'Unable to clean date time info ({scriptTimerString=}) ({scriptTimerMatch=})')
            return None

        try:
            return datetime.fromisoformat(scriptTimerString)
        except Exception as e:
            self.__timber.log('EccoResponseParser', f'Unable to parse datetime ({scriptTimerString=}) ({scriptTimerMatch=})', e, traceback.format_exc())
            return None

    async def findTimerScriptSource(
        self,
        htmlString: str | Any | None,
    ) -> str | None:
        if not utils.isValidStr(htmlString):
            return None

        result = etree.fromstring(
            text = htmlString,
            parser = self.__htmlParser,
            base_url = self.__eccoConstants.websiteUrl,
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
                return f'{self.__eccoConstants.baseUrl}{scriptSrc}'

        return None
