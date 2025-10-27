from typing import Final

from .requestsHandle import RequestsHandle
from ..networkClientProvider import NetworkClientProvider
from ..networkClientType import NetworkClientType
from ..networkHandle import NetworkHandle
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class RequestsClientProvider(NetworkClientProvider):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutSeconds: int = 30,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(timeoutSeconds):
            raise TypeError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        elif timeoutSeconds < 3 or timeoutSeconds > 60:
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        self.__timber: Final[TimberInterface] = timber
        self.__timeoutSeconds: Final[int] = timeoutSeconds

    async def get(self) -> NetworkHandle:
        return RequestsHandle(
            timber = self.__timber,
            timeoutSeconds = self.__timeoutSeconds,
        )

    @property
    def networkClientType(self) -> NetworkClientType:
        return NetworkClientType.REQUESTS
