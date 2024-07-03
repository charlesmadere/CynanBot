from typing import Any

import requests
from requests.models import Response

from ..misc import utils as utils
from .exceptions import GenericNetworkException
from .networkClientType import NetworkClientType
from .networkHandle import NetworkHandle
from .networkResponse import NetworkResponse
from .requestsResponse import RequestsResponse
from ..timber.timberInterface import TimberInterface


class RequestsHandle(NetworkHandle):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutSeconds: int = 8
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(timeoutSeconds):
            raise TypeError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        elif timeoutSeconds < 3 or timeoutSeconds > 16:
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        self.__timber: TimberInterface = timber
        self.__timeoutSeconds: int = timeoutSeconds

    async def delete(
        self,
        url: str,
        headers: dict[str, Any] | None = None
    ) -> NetworkResponse:
        response: Response | None = None

        try:
            response = requests.delete(
                url = url,
                headers = headers,
                timeout = self.__timeoutSeconds
            )
        except Exception as e:
            self.__timber.log('RequestsHandle', f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\": {e}', e)
            raise GenericNetworkException(f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\": {e}')

        if response is None:
            self.__timber.log('RequestsHandle', f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\"')
            raise GenericNetworkException(f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\"')

        return RequestsResponse(
            response = response,
            url = url,
            timber = self.__timber
        )

    async def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None
    ) -> NetworkResponse:
        response: Response | None = None

        try:
            response = requests.get(
                url = url,
                headers = headers,
                timeout = self.__timeoutSeconds
            )
        except Exception as e:
            self.__timber.log('RequestsHandle', f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\": {e}', e)
            raise GenericNetworkException(f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\": {e}')

        if response is None:
            self.__timber.log('RequestsHandle', f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\"')
            raise GenericNetworkException(f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\"')

        return RequestsResponse(
            response = response,
            url = url,
            timber = self.__timber
        )

    def getNetworkClientType(self) -> NetworkClientType:
        return NetworkClientType.REQUESTS

    async def post(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None
    ) -> NetworkResponse:
        response: Response | None = None

        try:
            response = requests.post(
                url = url,
                headers = headers,
                json = json,
                timeout = self.__timeoutSeconds
            )
        except Exception as e:
            self.__timber.log('RequestsHandle', f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\": {e}', e)
            raise GenericNetworkException(f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\": {e}')

        if response is None:
            self.__timber.log('RequestsHandle', f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\"')
            raise GenericNetworkException(f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\"')

        return RequestsResponse(
            response = response,
            url = url,
            timber = self.__timber
        )
