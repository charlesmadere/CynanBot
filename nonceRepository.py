class NonceRepository():

    def __init__(self):
        self.__cache = dict()

    def getNonce(self, key: str):
        if key is None or len(key) == 0 or key.isspace():
            raise ValueError(f'key argument is malformed: \"{key}\"')

        key = key.lower()
        return self.__cache.get(key)

    def setNonce(self, key: str, nonce: str):
        if key is None or len(key) == 0 or key.isspace():
            raise ValueError(f'key argument is malformed: \"{key}\"')

        if nonce is None or len(nonce) == 0 or nonce.isspace():
            print(f'key \"{key}\" has an invalid nonce: \"{nonce}\"')
            self.__cache.pop(key, None)
            return

        key = key.lower()
        self.__cache[key] = nonce
