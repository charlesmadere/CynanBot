from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.crowdMicrophoneStatus import CrowdMicrophoneStatus


class RefreshCrowdMicrophonesUseCaseInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        deadMicrophones: frozenset[CrowdMicrophoneStatus]

    @abstractmethod
    async def invoke(self) -> Result:
        pass
