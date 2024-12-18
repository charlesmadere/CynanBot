from .decTalkFileManagerInterface import DecTalkFileManagerInterface
from ...misc import utils as utils
from ...storage.tempFileHelperInterface import TempFileHelperInterface

class DecTalkFileManager(DecTalkFileManagerInterface):

    def __init__(
        self,
        tempFileHelper: TempFileHelperInterface,
        fileExtension: str = 'wav'
    ):
        if not isinstance(tempFileHelper, TempFileHelperInterface):
            raise TypeError(f'tempFileHelper argument is malformed: \"{tempFileHelper}\"')
        elif not utils.isValidStr(fileExtension):
            raise TypeError(f'fileExtension argument is malformed: \"{fileExtension}\"')

        self.__tempFileHelper: TempFileHelperInterface = tempFileHelper
        self.__fileExtension: str = fileExtension

    async def generateNewSpeechFile(self) -> str | None:
        fileName = await self.__tempFileHelper.getTempFileName(
            prefix = 'dectalk',
            extension = self.__fileExtension
        )

        return fileName
