from .decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ..models.decTalkVoice import DecTalkVoice


class DecTalkSettingsRepository(DecTalkSettingsRepositoryInterface):

    def __init__(self):
        # TODO
        pass

    async def clearCaches(self):
        # TODO
        pass

    async def getDecTalkExecutablePath(self) -> str | None:
        # TODO
        return None

    async def getDefaultVoice(self) -> DecTalkVoice:
        # TODO
        return DecTalkVoice.PAUL

    async def getMediaPlayerVolume(self) -> int | None:
        # TODO
        return None

    async def requireDecTalkExecutablePath(self) -> str:
        # TODO
        return ''
