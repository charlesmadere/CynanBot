from abc import abstractmethod

from ..ttsManagerInterface import TtsManagerInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider


class TtsMonsterManagerInterface(TtsManagerInterface):

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
