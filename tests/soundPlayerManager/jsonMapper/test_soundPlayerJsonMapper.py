from src.soundPlayerManager.jsonMapper.soundPlayerJsonMapper import SoundPlayerJsonMapper
from src.soundPlayerManager.jsonMapper.soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from src.soundPlayerManager.soundPlayerType import SoundPlayerType


class TestSoundPlayerJsonMapper:

    jsonMapper: SoundPlayerJsonMapperInterface = SoundPlayerJsonMapper()

    def test_parseSoundPlayerType_withAudioPlayerString(self):
        result = self.jsonMapper.parseSoundPlayerType('audio_player')
        assert result is SoundPlayerType.AUDIO_PLAYER

    def test_parseSoundPlayerType_withStubString(self):
        result = self.jsonMapper.parseSoundPlayerType('stub')
        assert result is SoundPlayerType.STUB

    def test_parseSoundPlayerType_withVlcString(self):
        result = self.jsonMapper.parseSoundPlayerType('vlc')
        assert result is SoundPlayerType.VLC

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, SoundPlayerJsonMapper)
        assert isinstance(self.jsonMapper, SoundPlayerJsonMapperInterface)
