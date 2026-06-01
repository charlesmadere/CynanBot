from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.useChatterItemAction import UseChatterItemAction
from ...voicemail.models.addVoicemailResult import AddVoicemailResult


class CassetteTapeItemUseCaseInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        addVoicemailResult: AddVoicemailResult
        targetUserId: str
        targetUserName: str

    @abstractmethod
    async def invoke(self, action: UseChatterItemAction) -> Result:
        pass
