import traceback
from json import JSONDecodeError
from typing import Any, Final

import xmltodict
from requests.models import Response

from ..exceptions import NetworkResponseIsClosedException
from ..networkClientType import NetworkClientType
from ..networkResponse import NetworkResponse
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class RequestsResponse(NetworkResponse):

    def __init__(
        self,
        response: Response,
        url: str,
        timber: TimberInterface,
    ):
        if not isinstance(response, Response):
            raise TypeError(f'response argument is malformed: \"{response}\"')
        elif not utils.isValidStr(url):
            raise TypeError(f'url argument is malformed: \"{url}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__response: Final[Response] = response
        self.__url: Final[str] = url
        self.__timber: Final[TimberInterface] = timber

        self.__isClosed: bool = False

    async def close(self):
        if self.__isClosed:
            return

        self.__isClosed = True
        self.__response.close()

    def isClosed(self) -> bool:
        return self.__isClosed

    async def json(self) -> dict[str, Any] | list[Any] | None:
        self.__requireNotClosed()

        try:
            return self.__response.json()
        except JSONDecodeError as e:
            self.__timber.log('RequestsResponse', f'Encountered JSON error when trying to decode response into JSON ({self}): {e}', e, traceback.format_exc())
            return None
        except Exception as e:
            self.__timber.log('RequestsResponse', f'Encountered unexpected error when trying to decode response into JSON ({self}): {e}', e, traceback.format_exc())
            return None

    @property
    def networkClientType(self) -> NetworkClientType:
        return NetworkClientType.REQUESTS

    async def read(self) -> bytes | None:
        self.__requireNotClosed()

        try:
            return self.__response.content
        except Exception as e:
            self.__timber.log('RequestsResponse', f'Encountered unexpected error when trying to decode response into bytes ({self}): {e}', e, traceback.format_exc())
            return None

    def __requireNotClosed(self):
        if self.isClosed():
            raise NetworkResponseIsClosedException(f'This response has already been closed! ({self})')

    @property
    def statusCode(self) -> int:
        self.__requireNotClosed()
        return self.__response.status_code

    async def string(self) -> str | None:
        self.__requireNotClosed()

        try:
            return self.__response.text
        except Exception as e:
            self.__timber.log('RequestsResponse', f'Encountered unexpected error when trying to decode response into string ({self}): {e}', e, traceback.format_exc())
            return None

    def toDictionary(self) -> dict[str, Any]:
        return {
            'isClosed': self.__isClosed,
            'networkClientType': self.networkClientType,
            'response': self.__response,
            'url': self.__url,
        }

    @property
    def url(self) -> str:
        return self.__url

    async def xml(self) -> dict[str, Any] | list[Any] | None:
        self.__requireNotClosed()

        try:
            rawBytes = await self.read()

            if rawBytes is None:
                return None

            return xmltodict.parse(rawBytes)
        except Exception as e:
            self.__timber.log('RequestsResponse', f'Encountered unexpected error when trying to decode response into XML ({self}): {e}', e, traceback.format_exc())
            return None
