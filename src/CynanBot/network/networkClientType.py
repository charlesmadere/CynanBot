from enum import Enum, auto

import CynanBot.misc.utils as utils


class NetworkClientType(Enum):

    AIOHTTP = auto()
    REQUESTS = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'aiohttp':
            return NetworkClientType.AIOHTTP
        elif text == 'requests':
            return NetworkClientType.REQUESTS
        else:
            raise ValueError(f'unknown NetworkClientType: \"{text}\"')
