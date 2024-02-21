from typing import Any, Dict, Optional

import requests
from requests.models import Response

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkHandle import NetworkHandle
from CynanBot.network.networkResponse import NetworkResponse
from CynanBot.network.requestsResponse import RequestsResponse
from CynanBot.timber.timberInterface import TimberInterface


class RequestsHandle(NetworkHandle):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutSeconds: int = 8
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        if not utils.isValidInt(timeoutSeconds):
            raise ValueError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        if timeoutSeconds < 3 or timeoutSeconds > 16:
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        self.__timber: TimberInterface = timber
        self.__timeoutSeconds: int = timeoutSeconds

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        response: Optional[Response] = None

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
        headers: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        response: Optional[Response] = None

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
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        response: Optional[Response] = None

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
