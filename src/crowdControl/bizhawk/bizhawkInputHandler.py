from ..crowdControlInput import CrowdControlInput
from ..crowdControlInputHandler import CrowdControlInputHandler
from ...timber.timberInterface import  TimberInterface


class BizhawkInputHandler(CrowdControlInputHandler):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def handleInput(self, input: CrowdControlInput) -> bool:
        if not isinstance(input, CrowdControlInput):
            raise TypeError(f'input argument is malformed: \"{input}\"')

        # TODO
        return False
