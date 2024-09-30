from abc import ABC, abstractmethod


class DecTalkVoiceChooserInterface(ABC):

    @abstractmethod
    async def choose(self, messageText: str | None) -> str | None:
        pass
