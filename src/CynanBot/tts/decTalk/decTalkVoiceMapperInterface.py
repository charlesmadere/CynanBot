from abc import ABC, abstractmethod

from CynanBot.tts.decTalk.decTalkVoice import DecTalkVoice


class DecTalkVoiceMapperInterface(ABC):

    @abstractmethod
    async def toString(self, voice: DecTalkVoice) -> str:
        pass
