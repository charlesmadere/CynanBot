import misc.utils as utils
from network.networkClientProvider import NetworkClientProvider
from network.networkClientType import NetworkClientType
from network.networkHandle import NetworkHandle
from network.requestsHandle import RequestsHandle
from timber.timberInterface import TimberInterface


class RequestsClientProvider(NetworkClientProvider):

    def __init__(
        self,
        timber: TimberInterface,
        timeoutSeconds: int = 8
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(timeoutSeconds):
            raise ValueError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        elif timeoutSeconds < 2 or timeoutSeconds > 16:
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        self.__timber: TimberInterface = timber
        self.__timeoutSeconds: int = timeoutSeconds

    async def get(self) -> NetworkHandle:
        return RequestsHandle(
            timber = self.__timber,
            timeoutSeconds = self.__timeoutSeconds
        )

    def getNetworkClientType(self) -> NetworkClientType:
        return NetworkClientType.REQUESTS
