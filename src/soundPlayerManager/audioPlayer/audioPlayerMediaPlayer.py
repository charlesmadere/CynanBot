from ...timber.timberInterface import TimberInterface


class AudioPlayerMediaPlayer:

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    @property
    def isPlaying(self) -> bool:
        return False

    async def play(self):
        # TODO
        pass

    async def setMedia(self, filePath: str):
        # TODO
        pass

    async def setVolume(self, volume: int):
        # TODO
        pass

    async def stop(self):
        # TODO
        pass

    @property
    def volume(self) -> int:
        # TODO
        return 100
