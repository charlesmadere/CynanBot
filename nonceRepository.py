import CynanBotCommon.utils as utils


class NonceRepository():

    def __init__(self):
        self.__cache = dict()

    def getNonce(self, key: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        key = key.lower()
        return self.__cache.get(key)

    def setNonce(self, key: str, nonce: str):
        if not utils.isValidStr(key):
            raise ValueError(f'key argument is malformed: \"{key}\"')

        if not utils.isValidStr(nonce):
            print(f'key \"{key}\" has an invalid nonce: \"{nonce}\"')
            self.__cache.pop(key, None)
            return

        key = key.lower()
        self.__cache[key] = nonce
