from datetime import datetime
from typing import Final

from ..models.absTimeoutAction import AbsTimeoutAction
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutRollFailureData import TimeoutRollFailureData
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ..timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface


class TimeoutRollFailureUseCase:

    def __init__(
        self,
        timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface,
        timeoutActionSettings: TimeoutActionSettingsInterface,
    ):
        if not isinstance(timeoutActionHistoryRepository, TimeoutActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutActionHistoryRepository argument is malformed: \"{timeoutActionHistoryRepository}\"')
        if not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')

        self.__timeoutActionHistoryRepository: Final[TimeoutActionHistoryRepositoryInterface] = timeoutActionHistoryRepository
        self.__timeoutActionSettings: Final[TimeoutActionSettingsInterface] = timeoutActionSettings

    async def generate(
        self,
        timeoutAction: AbsTimeoutAction,
        now: datetime,
        timeoutTargetUserId: str,
        diceRoll: TimeoutDiceRoll,
    ) -> TimeoutRollFailureData:
        # TODO
        pass
        raise RuntimeError()
