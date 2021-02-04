from CynanBotCommon.backingDatabase import BackingDatabase


class SubsAndBitsRepository():

    def __init__(self, backingDatabase: BackingDatabase):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase = backingDatabase
