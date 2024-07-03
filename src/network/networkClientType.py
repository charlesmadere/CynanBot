from enum import auto

from ..misc.enumWithToFromStr import EnumWithToFromStr


class NetworkClientType(EnumWithToFromStr):

    AIOHTTP = auto()
    REQUESTS = auto()
