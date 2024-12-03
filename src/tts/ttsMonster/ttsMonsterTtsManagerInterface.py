from abc import abstractmethod

from ..ttsManagerInterface import TtsManagerInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider


class TtsMonsterTtsManagerInterface(TtsManagerInterface):

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
