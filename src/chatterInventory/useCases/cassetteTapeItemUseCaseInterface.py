from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.useChatterItemAction import UseChatterItemAction
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface
from ...voicemail.models.addVoicemailResult import AddVoicemailResult


class CassetteTapeItemUseCaseInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        addVoicemailResult: AddVoicemailResult
        targetUserData: TwitchUserInterface

    @abstractmethod
    async def invoke(
        self,
        twitchAccessToken: str,
        action: UseChatterItemAction,
    ) -> Result:
        pass
