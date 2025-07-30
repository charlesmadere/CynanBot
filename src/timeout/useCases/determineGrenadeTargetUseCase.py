from typing import Final

from ..models.grenadeTargetData import GrenadeTargetData
from ..models.grenadeTimeoutAction import GrenadeTimeoutAction
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface


class DetermineGrenadeTargetUseCase:

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository

    async def invoke(
        self,
        timeoutAction: GrenadeTimeoutAction,
    ) -> GrenadeTargetData:
        if not isinstance(timeoutAction, GrenadeTimeoutAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{timeoutAction}\"')

        # TODO
        pass
        raise RuntimeError()
