import random
import re
import traceback
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Collection, Final, Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from .googleTtsApiHelperInterface import GoogleTtsApiHelperInterface
from .googleTtsHelperInterface import GoogleTtsHelperInterface
from .googleTtsVoicesHelperInterface import GoogleTtsVoicesHelperInterface
from ..exceptions import GoogleFailedToCreateDirectoriesException
from ..jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from ..models.absGoogleVoicePreset import AbsGoogleVoicePreset
from ..models.googleMultiSpeakerMarkup import GoogleMultiSpeakerMarkup
from ..models.googleMultiSpeakerMarkupTurn import GoogleMultiSpeakerMarkupTurn
from ..models.googleMultiSpeakerTextSynthesisInput import GoogleMultiSpeakerTextSynthesisInput
from ..models.googleMultiSpeakerVoicePreset import GoogleMultiSpeakerVoicePreset
from ..models.googleTextSynthesisInput import GoogleTextSynthesisInput
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTtsFileReference import GoogleTtsFileReference
from ..models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ..models.googleVoicePreset import GoogleVoicePreset
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams
from ..settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...glacialTtsStorage.fileRetriever.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsProvider import TtsProvider


class GoogleTtsHelper(GoogleTtsHelperInterface):

    @dataclass(frozen = True)
    class GoogleSpeechRequestData:
        voicePreset: AbsGoogleVoicePreset
        messageSentences: FrozenList[str]
        synthesizeRequest: GoogleTextSynthesizeRequest
        fullMessage: str

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        googleFileExtensionHelper: GoogleFileExtensionHelperInterface,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsApiHelper: GoogleTtsApiHelperInterface,
        googleTtsVoicesHelper: GoogleTtsVoicesHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(googleFileExtensionHelper, GoogleFileExtensionHelperInterface):
            raise TypeError(f'googleFileExtensionHelper argument is malformed: \"{googleFileExtensionHelper}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsApiHelper, GoogleTtsApiHelperInterface):
            raise TypeError(f'googleTtsApiHelper argument is malformed: \"{googleTtsApiHelper}\"')
        elif not isinstance(googleTtsVoicesHelper, GoogleTtsVoicesHelperInterface):
            raise TypeError(f'googleTtsVoicesHelper argument is malformed: \"{googleTtsVoicesHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__glacialTtsFileRetriever: Final[GlacialTtsFileRetrieverInterface] = glacialTtsFileRetriever
        self.__googleFileExtensionHelper: Final[GoogleFileExtensionHelperInterface] = googleFileExtensionHelper
        self.__googleJsonMapper: Final[GoogleJsonMapperInterface] = googleJsonMapper
        self.__googleSettingsRepository: Final[GoogleSettingsRepositoryInterface] = googleSettingsRepository
        self.__googleTtsApiHelper: Final[GoogleTtsApiHelperInterface] = googleTtsApiHelper
        self.__googleTtsVoicesHelper: Final[GoogleTtsVoicesHelperInterface] = googleTtsVoicesHelper
        self.__timber: Final[TimberInterface] = timber

        self.__directoryTreeRegEx: Final[Pattern] = re.compile(r'^((\.{1,2})?[\w+|\/]+)\/\w+\.\w+$', re.IGNORECASE)

    async def __createDirectories(self, filePath: str):
        # this logic removes the file name from the file path, leaving us with just a directory tree
        directoryMatch = self.__directoryTreeRegEx.fullmatch(filePath)

        if directoryMatch is None or not utils.isValidStr(directoryMatch.group(1)):
            raise GoogleFailedToCreateDirectoriesException(f'Failed to create Google TTS file directories ({filePath=}) ({directoryMatch=})')

        directory = directoryMatch.group(1)

        if await aiofiles.ospath.exists(
            path = directory,
            loop = self.__eventLoop
        ):
            return

        await aiofiles.os.makedirs(
            name = directory,
            loop = self.__eventLoop
        )

        self.__timber.log('GoogleTtsHelper', f'Created new directories ({filePath=}) ({directory=})')

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None
    ) -> str | None:
        if not await self.__googleSettingsRepository.useDonationPrefix():
            return message
        elif utils.isValidStr(donationPrefix) and utils.isValidStr(message):
            return f'{donationPrefix} {message}'
        elif utils.isValidStr(donationPrefix):
            return donationPrefix
        elif utils.isValidStr(message):
            return message
        else:
            return None

    async def __createGoogleMultiSpeakerRequestData(
        self,
        sentences: Collection[str],
        fullMessage: str,
    ) -> GoogleSpeechRequestData:
        frozenSentences: FrozenList[str] = FrozenList(sentences)
        frozenSentences.freeze()

        voicePreset = await self.__googleTtsVoicesHelper.getEnglishMultiSpeakerVoice()

        speakerCharacters = await self.__determineMultiSpeakerCharacters(
            voicePreset = voicePreset,
        )

        markupTurns: FrozenList[GoogleMultiSpeakerMarkupTurn] = FrozenList()

        for index, sentence in enumerate(frozenSentences):
            markupTurns.append(GoogleMultiSpeakerMarkupTurn(
                speaker = speakerCharacters[index % len(speakerCharacters)],
                text = sentence,
            ))

        markupTurns.freeze()

        multiSpeakerMarkup = GoogleMultiSpeakerMarkup(
            turns = markupTurns,
        )

        synthesisInput = GoogleMultiSpeakerTextSynthesisInput(
            multiSpeakerMarkup = multiSpeakerMarkup,
        )

        voiceAudioConfig = await self.__createGoogleVoiceAudioConfig()

        voiceSelectionParams = await self.__createGoogleVoiceSelectionParams(
            voicePreset = voicePreset,
        )

        synthesizeRequest = GoogleTextSynthesizeRequest(
            synthesisInput = synthesisInput,
            audioConfig = voiceAudioConfig,
            voice = voiceSelectionParams,
        )

        return GoogleTtsHelper.GoogleSpeechRequestData(
            voicePreset = voicePreset,
            messageSentences = frozenSentences,
            synthesizeRequest = synthesizeRequest,
            fullMessage = fullMessage,
        )

    async def __createGoogleSpeechRequestData(
        self,
        voicePreset: AbsGoogleVoicePreset | None,
        allowMultiSpeaker: bool,
        fullMessage: str,
    ) -> GoogleSpeechRequestData:
        if (voicePreset is None or isinstance(voicePreset, GoogleMultiSpeakerVoicePreset)) and allowMultiSpeaker and await self.__googleSettingsRepository.isMultiSpeakerEnabled():
            sentences = utils.splitStringIntoSentences(fullMessage)

            if len(sentences) >= 2:
                return await self.__createGoogleMultiSpeakerRequestData(
                    sentences = sentences,
                    fullMessage = fullMessage,
                )

        if voicePreset is None or not isinstance(voicePreset, GoogleVoicePreset):
            voicePreset = await self.__googleTtsVoicesHelper.getEnglishVoice()

        messageSentences: FrozenList[str] = FrozenList()
        messageSentences.freeze()

        synthesisInput = GoogleTextSynthesisInput(
            text = fullMessage,
        )

        voiceAudioConfig = await self.__createGoogleVoiceAudioConfig()

        voiceSelectionParams = await self.__createGoogleVoiceSelectionParams(
            voicePreset = voicePreset,
        )

        synthesizeRequest = GoogleTextSynthesizeRequest(
            synthesisInput = synthesisInput,
            audioConfig = voiceAudioConfig,
            voice = voiceSelectionParams,
        )

        return GoogleTtsHelper.GoogleSpeechRequestData(
            voicePreset = voicePreset,
            messageSentences = messageSentences,
            synthesizeRequest = synthesizeRequest,
            fullMessage = fullMessage,
        )

    async def __createGoogleVoiceAudioConfig(self) -> GoogleVoiceAudioConfig:
        return GoogleVoiceAudioConfig(
            pitch = None,
            speakingRate = None,
            volumeGainDb = await self.__googleSettingsRepository.getVolumeGainDb(),
            sampleRateHertz = None,
            audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding(),
        )

    async def __createGoogleVoiceSelectionParams(
        self,
        voicePreset: AbsGoogleVoicePreset,
    ) -> GoogleVoiceSelectionParams:
        return GoogleVoiceSelectionParams(
            gender = None,
            languageCode = voicePreset.languageCode,
            name = voicePreset.fullName,
        )

    async def __determineMultiSpeakerCharacters(
        self,
        voicePreset: GoogleMultiSpeakerVoicePreset,
    ) -> FrozenList[str]:
        allSpeakerCharacters: FrozenList[str] = FrozenList(voicePreset.speakerCharacters)
        allSpeakerCharacters.freeze()

        chosenSpeakerCharacters: FrozenList[str] = FrozenList()

        # multi speaker characters are limited to 2
        while len(chosenSpeakerCharacters) < 2:
            randomSpeakerCharacter = random.choice(allSpeakerCharacters)

            if randomSpeakerCharacter not in chosenSpeakerCharacters:
                chosenSpeakerCharacters.append(randomSpeakerCharacter)

        chosenSpeakerCharacters.freeze()
        return chosenSpeakerCharacters

    async def generateTts(
        self,
        voicePreset: AbsGoogleVoicePreset | None,
        allowMultiSpeaker: bool,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> GoogleTtsFileReference | None:
        if voicePreset is not None and not isinstance(voicePreset, AbsGoogleVoicePreset):
            raise TypeError(f'voicePreset argument is malformed: \"{voicePreset}\"')
        elif not utils.isValidBool(allowMultiSpeaker):
            raise TypeError(f'allowMultiSpeaker argument is malformed: \"{allowMultiSpeaker}\"')
        elif donationPrefix is not None and not isinstance(donationPrefix, str):
            raise TypeError(f'donationPrefix argument is malformed: \"{donationPrefix}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(donationPrefix) and not utils.isValidStr(message):
            return None

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message,
        )

        if not utils.isValidStr(fullMessage):
            return None

        googleSpeechRequest = await self.__createGoogleSpeechRequestData(
            voicePreset = voicePreset,
            allowMultiSpeaker = allowMultiSpeaker,
            fullMessage = fullMessage,
        )

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = fullMessage,
            voice = googleSpeechRequest.voicePreset.fullName,
            provider = TtsProvider.GOOGLE,
        )

        if glacialFile is not None:
            return GoogleTtsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                filePath = glacialFile.filePath,
                voicePreset = await self.__googleJsonMapper.requireVoicePreset(glacialFile.voice),
            )

        speechBytes = await self.__googleTtsApiHelper.getSpeech(
            request = googleSpeechRequest.synthesizeRequest,
        )

        if speechBytes is None:
            return None

        audioEncoding = await self.__googleSettingsRepository.getVoiceAudioEncoding()
        fileExtension = await self.__googleFileExtensionHelper.getFileExtension(audioEncoding)

        glacialFile = await self.__glacialTtsFileRetriever.saveFile(
            fileExtension = fileExtension,
            message = fullMessage,
            voice = await self.__googleJsonMapper.serializeVoicePreset(googleSpeechRequest.voicePreset),
            provider = TtsProvider.GOOGLE,
        )

        if await self.__saveSpeechBytes(
            speechBytes = speechBytes,
            fileName = glacialFile.fileName,
            filePath = glacialFile.filePath,
        ):
            return GoogleTtsFileReference(
                storeDateTime = glacialFile.storeDateTime,
                voicePreset = googleSpeechRequest.voicePreset,
                filePath = glacialFile.filePath,
            )
        else:
            self.__timber.log('GoogleTtsHelper', f'Failed to write Google TTS speechBytes to file ({googleSpeechRequest=})')
            return None

    async def __saveSpeechBytes(
        self,
        speechBytes: bytes,
        fileName: str,
        filePath: str
    ) -> bool:
        if not isinstance(speechBytes, bytes):
            raise TypeError(f'speechBytes argument is malformed: \"{speechBytes}\"')
        elif not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')
        elif not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        await self.__createDirectories(filePath)

        try:
            async with aiofiles.open(
                file = filePath,
                mode = 'wb',
                loop = self.__eventLoop
            ) as file:
                await file.write(speechBytes)
                await file.flush()
        except Exception as e:
            self.__timber.log('GoogleTtsHelper', f'Encountered exception when trying to write Google TTS speechBytes to file ({fileName=}) ({filePath=}): {e}', e, traceback.format_exc())
            return False

        return True
