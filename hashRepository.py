import hashlib


class HashRepository():

    def __init__(self):
        self.__cache = dict()

    def getHash(self, string: str):
        if string == None or len(string) == 0:
            raise ValueError(f'string argument is malformed: \"{string}\"')

        string = string.lower()

        if string in self.__cache:
            return self.__cache[string]

        result = hashlib.md5(string.encode())
        newHash = result.hexdigest()
        self.__cache[string] = newHash
        return newHash
