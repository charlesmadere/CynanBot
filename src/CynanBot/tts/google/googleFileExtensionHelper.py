from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.tts.google.googleFileExtensionHelperInterface import \
    GoogleFileExtensionHelperInterface


class GoogleFileExtensionHelper(GoogleFileExtensionHelperInterface):

    async def getFileExtension(self, audioEncoding: GoogleVoiceAudioEncoding) -> str:
        if not isinstance(audioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'audioEncoding argument is malformed: \"{audioEncoding}\"')

        match audioEncoding:
            case GoogleVoiceAudioEncoding.MP3: return 'mp3'
            case GoogleVoiceAudioEncoding.OGG_OPUS: return 'ogg'
            case _:
                raise RuntimeError(f'The given audio encoding (\"{audioEncoding}\") does not have a corresponding file extension!')
