from .bizhawkKey import BizhawkKey
from .bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from ..actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..actions.crowdControlAction import CrowdControlAction
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControlActionHandleResult import CrowdControlActionHandleResult
from ..crowdControlActionHandler import CrowdControlActionHandler
from ...timber.timberInterface import TimberInterface


class BizhawkActionHandler(CrowdControlActionHandler):

    def __init__(
        self,
        bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface,
        timber: TimberInterface,
        keyPressDelayMillis: int = 64
    ):
        if not isinstance(bizhawkSettingsRepository, BizhawkSettingsRepositoryInterface):
            raise TypeError(f'bizhawkSettingsRepository argument is malformed: \"{bizhawkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(keyPressDelayMillis):
            raise TypeError(f'keyPressDelayMillis argument is malformed: \"{keyPressDelayMillis}\"')
        elif keyPressDelayMillis < 32 or keyPressDelayMillis > 250:
            raise ValueError(f'keyPressDelayMillis argument is out of bounds: {keyPressDelayMillis}')

        self.__bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface = bizhawkSettingsRepository
        self.__timber: TimberInterface = timber
        self.__keyPressDelayMillis: int = keyPressDelayMillis

    async def __handleBizhawkKeyPress(
        self,
        keyBind: BizhawkKey,
        action: CrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(keyBind, BizhawkKey):
            raise TypeError(f'keyBind argument is malformed: \"{keyBind}\"')
        elif not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        return CrowdControlActionHandleResult.ABANDON

    async def handleButtonPressAction(
        self,
        action: ButtonPressCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, ButtonPressCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        keyBind = await self.__bizhawkSettingsRepository.getButtonKeyBind(
            button = action.button
        )

        if keyBind is None:
            return CrowdControlActionHandleResult.ABANDON
        else:
            return await self.__handleBizhawkKeyPress(
                keyBind = keyBind,
                action = action
            )

    async def handleGameShuffleAction(
        self,
        action: GameShuffleCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, GameShuffleCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        keyBind = await self.__bizhawkSettingsRepository.getGameShuffleKeyBind()

        if keyBind is None:
            return CrowdControlActionHandleResult.ABANDON
        else:
            return await self.__handleBizhawkKeyPress(
                keyBind = keyBind,
                action = action
            )
