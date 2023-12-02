from enum import auto

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


class NetworkClientType(EnumWithToFromStr):

    AIOHTTP = auto()
    REQUESTS = auto()
