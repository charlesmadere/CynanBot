from src.soundPlayerManager.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.users.chatSoundAlert.chatSoundAlertJsonParser import ChatSoundAlertJsonParser
from src.users.chatSoundAlert.chatSoundAlertJsonParserInterface import ChatSoundAlertJsonParserInterface
from src.users.chatSoundAlert.chatSoundAlertQualifier import ChatSoundAlertQualifer
from src.users.chatSoundAlert.chatSoundAlertType import ChatSoundAlertType


class TestChatSoundAlertJsonParser:

    soundAlertJsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper()

    jsonParser: ChatSoundAlertJsonParserInterface = ChatSoundAlertJsonParser(
        soundAlertJsonMapper = soundAlertJsonMapper
    )

    def test_parseAlertQualifier_withContainsString(self):
        result = self.jsonParser.parseAlertQualifier('contains')
        assert result is ChatSoundAlertQualifer.CONTAINS

    def test_parseAlertQualifier_withExactString(self):
        result = self.jsonParser.parseAlertQualifier('exact')
        assert result is ChatSoundAlertQualifer.EXACT

    def test_parseAlertType_withDirectoryPathString(self):
        result = self.jsonParser.parseAlertType('directory_path')
        assert result is ChatSoundAlertType.DIRECTORY_PATH

    def test_parseAlertType_withFilePathString(self):
        result = self.jsonParser.parseAlertType('file_path')
        assert result is ChatSoundAlertType.FILE_PATH

    def test_parseAlertType_withSoundAlertString(self):
        result = self.jsonParser.parseAlertType('sound_alert')
        assert result is ChatSoundAlertType.SOUND_ALERT

    def test_sanity(self):
        assert self.jsonParser is not None
        assert isinstance(self.jsonParser, ChatSoundAlertJsonParser)
        assert isinstance(self.jsonParser, ChatSoundAlertJsonParserInterface)
