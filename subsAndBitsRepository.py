from CynanBotCommon.backingDatabase import BackingDatabase

# For this class to ever be fleshed out, we're going to need to look into this:
# https://dev.twitch.tv/docs/irc/tags#usernotice-twitch-tags

class SubsAndBitsRepository():

    def __init__(self, backingDatabase: BackingDatabase):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase = backingDatabase
