from typing import Collection, Final

from ..models.airStrikeTargetData import AirStrikeTargetData
from ..models.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface


class DetermineAirStrikeTargetsUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository

    async def invoke(
        self,
        timeoutAction: AirStrikeTimeoutAction,
    ) -> Collection[AirStrikeTargetData]:
        if not isinstance(timeoutAction, AirStrikeTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        # TODO
        pass
        raise RuntimeError()
