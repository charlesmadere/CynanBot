from typing import Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface


class NonceRepository():

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber
        self.__nonces: Dict[str, Optional[str]] = dict()

    def __delitem__(self, key: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        key = key.lower()
        previousValue = self.__nonces.get(key, None)
        self.__nonces.pop(key, None)
        self.__timber.log('NonceRepository', f'Key \"{key}\" has been deleted, previous value was \"{previousValue}\".')

    def __getitem__(self, key: str) -> Optional[str]:
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        return self.__nonces.get(key.lower(), None)

    def __setitem__(self, key: str, value: Optional[str]):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        key = key.lower()

        if utils.isValidStr(value):
            self.__nonces[key] = value
        else:
            self.__delitem__(key)
