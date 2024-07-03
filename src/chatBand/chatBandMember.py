from ..misc import utils as utils
from .chatBandInstrument import ChatBandInstrument


class ChatBandMember():

    def __init__(
        self,
        isEnabled: bool,
        instrument: ChatBandInstrument,
        author: str,
        keyPhrase: str
    ):
        if not utils.isValidBool(isEnabled):
            raise ValueError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not isinstance(instrument, ChatBandInstrument):
            raise ValueError(f'instrument argument is malformed: \"{instrument}\"')
        elif not utils.isValidStr(author):
            raise ValueError(f'author argument is malformed: \"{author}\"')
        elif not utils.isValidStr(keyPhrase):
            raise ValueError(f'keyPhrase argument is malformed: \"{keyPhrase}\"')

        self.__isEnabled: bool = isEnabled
        self.__instrument: ChatBandInstrument = instrument
        self.__author: str = author
        self.__keyPhrase: str = keyPhrase

    def getAuthor(self) -> str:
        return self.__author

    def getInstrument(self) -> ChatBandInstrument:
        return self.__instrument

    def getKeyPhrase(self) -> str:
        return self.__keyPhrase

    def isEnabled(self) -> bool:
        return self.__isEnabled
