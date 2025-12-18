from typing import Final

from .anivContentScannerInterface import AnivContentScannerInterface
from ..models.anivContentCode import AnivContentCode
from ...contentScanner.contentCode import ContentCode
from ...contentScanner.contentScannerInterface import ContentScannerInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class AnivContentScanner(AnivContentScannerInterface):

    def __init__(
        self,
        contentScanner: ContentScannerInterface,
        timber: TimberInterface,
    ):
        if not isinstance(contentScanner, ContentScannerInterface):
            raise TypeError(f'contentScanner argument is malformed: \"{contentScanner}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__contentScanner: Final[ContentScannerInterface] = contentScanner
        self.__timber: Final[TimberInterface] = timber

    async def scan(self, message: str | None) -> AnivContentCode:
        if not utils.isValidStr(message):
            return AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK

        contentCode = await self.__contentScanner.scan(message)

        if contentCode is ContentCode.CONTAINS_BANNED_CONTENT:
            return AnivContentCode.CONTAINS_BANNED_CONTENT
        elif contentCode is ContentCode.CONTAINS_URL:
            return AnivContentCode.CONTAINS_URL
        elif contentCode is ContentCode.IS_NONE or contentCode is ContentCode.IS_EMPTY or contentCode is ContentCode.IS_BLANK:
            return AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK
        elif contentCode is not ContentCode.OK:
            # This case is actually a programmatic error of some kind, it means that we're not
            # properly mapping together ContentCode values and AnivContentCode values.
            self.__timber.log('AnivContentScanner', f'Message from aniv returned a ContentCode that we\'re not properly supporting ({contentCode=}) ({message=})')
            return AnivContentCode.CONTAINS_BANNED_CONTENT
        else:
            return AnivContentCode.OK
