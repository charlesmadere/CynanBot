import random

from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams
from CynanBot.tts.google.googleTtsVoiceChooserInterface import \
    GoogleTtsVoiceChooserInterface


class GoogleTtsVoiceChooser(GoogleTtsVoiceChooserInterface):

    def __init__(
        self,
        languageCodeToNames: dict[str, set[str]] = {
            'en-AU': { 'en-AU-Neural2-A', 'en-AU-Neural2-B', 'en-AU-Neural2-C', 'en-AU-Neural2-D', 'en-AU-Neural2-A', 'en-AU-Neural2-B', 'en-AU-Neural2-C', 'en-AU-Neural2-D' },
            'en-GB': { 'en-GB-Neural2-A', 'en-GB-Neural2-B', 'en-GB-Neural2-C', 'en-GB-Neural2-D', 'en-GB-Neural2-F', 'en-GB-Wavenet-A', 'en-GB-Wavenet-B', 'en-GB-Wavenet-C', 'en-GB-Wavenet-D', 'en-GB-Wavenet-F' },
            'en-US': { 'en-US-Casual-K', 'en-US-Journey-D', 'en-US-Journey-F' },
            'fr-CA': { 'fr-CA-Wavenet-A', 'fr-CA-Wavenet-B', 'fr-CA-Wavenet-C', 'fr-CA-Wavenet-D' },
            'ja-JP': { 'ja-JP-Neural2-B', 'ja-JP-Neural2-C', 'ja-JP-Neural2-D' },
            'sv-SE': { 'sv-SE-Wavenet-A', 'sv-SE-Wavenet-B', 'sv-SE-Wavenet-C', 'sv-SE-Wavenet-D', 'sv-SE-Wavenet-E' }
        }
    ):
        if not isinstance(languageCodeToNames, dict):
            raise TypeError(f'languageCodeToVoiceNames argument is malformed: \"{languageCodeToNames}\"')
        elif len(languageCodeToNames) == 0:
            raise ValueError(f'languageCodeToNames argument is empty: \"{languageCodeToNames}\"')

        self.__languageCodeToNames: dict[str, set[str]] = languageCodeToNames

    async def choose(self) -> GoogleVoiceSelectionParams:
        languageCodes = self.__languageCodeToNames.keys()
        languageCode = random.choice(list(languageCodes))

        names = self.__languageCodeToNames[languageCode]
        name = random.choice(list(names))

        return GoogleVoiceSelectionParams(
            gender = None,
            languageCode = languageCode,
            name = name
        )
