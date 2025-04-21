from ..compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ...compositeTtsManagerInterface import CompositeTtsManagerInterface
from ...stub.stubCompositeTtsManager import StubCompositeTtsManager


class StubCompositeTtsManagerProvider(CompositeTtsManagerProviderInterface):

    def __init__(self):
        self.__instance: CompositeTtsManagerInterface = StubCompositeTtsManager()

    def constructNewCompositeTtsManagerInstance(self) -> CompositeTtsManagerInterface:
        # this method kinda breaks contract, but it's fine in this case
        return self.__instance

    def getSharedCompositeTtsManagerInstance(self) -> CompositeTtsManagerInterface:
        return self.__instance
