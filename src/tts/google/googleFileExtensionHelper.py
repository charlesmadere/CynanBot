from .googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from ...google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class GoogleFileExtensionHelper(GoogleFileExtensionHelperInterface):

    async def getFileExtension(self, audioEncoding: GoogleVoiceAudioEncoding) -> str:
        if not isinstance(audioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'audioEncoding argument is malformed: \"{audioEncoding}\"')

        match audioEncoding:
            case GoogleVoiceAudioEncoding.MP3: return 'mp3'
            case GoogleVoiceAudioEncoding.OGG_OPUS: return 'ogg'
            case _: raise ValueError(f'The given audio encoding (\"{audioEncoding}\") does not have a corresponding file extension!')
