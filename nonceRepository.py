class NonceRepository():

    def __init__(self):
        self.__cache = dict()

    def getNonce(self, key: str):
        if key == None or len(key) == 0 or key.isspace():
            raise ValueError(f'key argument is malformed: \"{key}\"')

        key = key.lower()
        return self.__cache.get(key)

    def setNonce(self, key: str, nonce: str):
        if key == None or len(key) == 0 or key.isspace():
            raise ValueError(f'key argument is malformed: \"{key}\"')
        elif nonce == None or len(nonce) == 0:
            raise ValueError(f'nonce argument is malformed: \"{nonce}\"')

        key = key.lower()
        self.__cache[key] = nonce
