from ..cheerActionHelperInterface import CheerActionHelperInterface


class StubCheerActionHelper(CheerActionHelperInterface):

    async def handleCheer(self, cheerInfo: CheerActionHelperInterface.CheerInfo) -> bool:
        # this method is intentionally empty
        return False

    def start(self):
        # this method is intentionally empty
        pass

    def submitCheer(self, cheerInfo: CheerActionHelperInterface.CheerInfo):
        # this method is intentionally empty
        pass
