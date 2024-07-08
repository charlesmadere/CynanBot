from enum import Enum, auto


class NetworkClientType(Enum):

    AIOHTTP = auto()
    REQUESTS = auto()
