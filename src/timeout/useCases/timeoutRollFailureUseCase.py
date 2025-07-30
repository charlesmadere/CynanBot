from datetime import datetime
from typing import Final

from ..models.absTimeoutAction import AbsTimeoutAction
from ..models.timeoutDiceRoll import TimeoutDiceRoll
from ..models.timeoutRollFailureData import TimeoutRollFailureData
from ..settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ..timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from ...misc import utils as utils


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

    async def invoke(
        self,
        timeoutAction: AbsTimeoutAction,
        now: datetime,
        timeoutTargetUserId: str,
        diceRoll: TimeoutDiceRoll,
    ) -> TimeoutRollFailureData:
        if not isinstance(timeoutAction, AbsTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')
        elif not isinstance(now, datetime):
            raise TypeError(f'now argument is malformed: \"{now}\"')
        elif not utils.isValidStr(timeoutTargetUserId):
            raise TypeError(f'timeoutTargetUserId argument is malformed: \"{timeoutTargetUserId}\"')
        elif not isinstance(diceRoll, TimeoutDiceRoll):
            raise TypeError(f'diceRoll argument is malformed: \"{diceRoll}\"')

        # TODO
        pass
        raise RuntimeError()
