from abc import ABC, abstractmethod

from CynanBot.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType


class FuntoonRepositoryInterface(ABC):

    @abstractmethod
    async def banTriviaQuestion(self, triviaId: str) -> bool:
        pass

    @abstractmethod
    async def pkmnBattle(
        self,
        twitchChannel: str,
        userThatRedeemed: str,
        userToBattle: str
    ) -> bool:
        pass

    @abstractmethod
    async def pkmnCatch(
        self,
        twitchChannel: str,
        userThatRedeemed: str,
        funtoonPkmnCatchType: FuntoonPkmnCatchType = None
    ) -> bool:
        pass

    @abstractmethod
    async def pkmnGiveEvolve(
        self,
        twitchChannel: str,
        userThatRedeemed: str
    ) -> bool:
        pass

    @abstractmethod
    async def pkmnGiveShiny(
        self,
        twitchChannel: str,
        userThatRedeemed: str
    ) -> bool:
        pass
