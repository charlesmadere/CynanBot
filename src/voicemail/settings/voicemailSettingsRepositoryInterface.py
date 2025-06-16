from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class VoicemailSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getHoursBetweenAutomaticVoicemailChatNotifications(self) -> int:
        pass

    @abstractmethod
    async def getMaximumPerOriginatingUser(self) -> int:
        pass

    @abstractmethod
    async def getMaximumPerTargetUser(self) -> int:
        pass

    @abstractmethod
    async def getMaximumVoicemailAgeDays(self) -> int:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass

    @abstractmethod
    async def targetUserMustBeFollowing(self) -> bool:
        pass

    @abstractmethod
    async def targetUserMustNotBeActiveInChat(self) -> bool:
        pass

    @abstractmethod
    async def useMessageQueueing(self) -> bool:
        pass
