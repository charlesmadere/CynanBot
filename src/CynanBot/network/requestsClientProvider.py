import CynanBot.misc.utils as utils
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkHandle import NetworkHandle
from CynanBot.network.requestsHandle import RequestsHandle
from CynanBot.timber.timberInterface import TimberInterface


class RequestsClientProvider(NetworkClientProvider):

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

    async def get(self) -> NetworkHandle:
        return RequestsHandle(
            timber = self.__timber,
            timeoutSeconds = self.__timeoutSeconds
        )

    def getNetworkClientType(self) -> NetworkClientType:
        return NetworkClientType.REQUESTS
