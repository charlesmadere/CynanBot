from datetime import datetime


class TimedDict():

    def __init__(self, timeDelta):
        if timeDelta is None:
            raise ValueError(f'timeDelta argument is malformed: \"{timeDelta}\"')

        self.__timeDelta = timeDelta
        self.__times = dict()
        self.__values = dict()

    def __delitem__(self, key):
        self.__times.pop(key, None)
        self.__values.pop(key, None)

    def __getitem__(self, key):
        if key not in self.__times or key not in self.__values:
            return None

        now = datetime.now()

        if now > self.__times[key]:
            return None

        return self.__values[key]

    def isReady(self, key):
        return self[key] is None

    def isReadyAndUpdate(self, key):
        if self.isReady(key):
            self.update(key)
            return True
        else:
            return False

    def __setitem__(self, key, value):
        self.__times[key] = datetime.now() + self.__timeDelta
        self.__values[key] = value

    def update(self, key):
        self.__times[key] = datetime.now() + self.__timeDelta
        self.__values[key] = self.__times[key]
