from abc import ABC, abstractmethod

from .funtoonPkmnCatchType import FuntoonPkmnCatchType


class FuntoonHelperInterface(ABC):

    @abstractmethod
    async def banTriviaQuestion(self, triviaId: str) -> bool:
        pass

    @abstractmethod
    async def pkmnBattle(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str,
        userToBattle: str,
    ) -> bool:
        pass

    @abstractmethod
    async def pkmnCatch(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str,
        funtoonPkmnCatchType: FuntoonPkmnCatchType | None = None,
    ) -> bool:
        pass

    @abstractmethod
    async def pkmnGiveEvolve(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str,
    ) -> bool:
        pass

    @abstractmethod
    async def pkmnGiveShiny(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userThatRedeemed: str,
    ) -> bool:
        pass
