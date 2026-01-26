from datetime import datetime
from typing import Any, Final

from .transparentResponse import TransparentResponse
from .transparentXmlMapperInterface import TransparentXmlMapperInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils


class TransparentXmlMapper(TransparentXmlMapperInterface):

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def parseTransparentResponse(
        self,
        xmlContents: dict[str, Any] | Any | None,
    ) -> TransparentResponse | None:
        if not isinstance(xmlContents, dict) or len(xmlContents) == 0:
            return None

        dateStr = utils.getStrFromDict(xmlContents, 'date')
        date = datetime.strptime(dateStr, '%m-%d-%Y')
        date = date.replace(tzinfo = self.__timeZoneRepository.getDefault())

        enPhrase = utils.getStrFromDict(xmlContents, 'enphrase', clean = True)
        fnPhrase = utils.getStrFromDict(xmlContents, 'fnphrase', clean = True)

        langName: str | None = None
        if 'langname' in xmlContents and utils.isValidStr(xmlContents.get('langname')):
            langName = utils.getStrFromDict(
                d = xmlContents,
                key = 'langname',
                clean = True,
            )

        notes: str | None = None
        if 'notes' in xmlContents and utils.isValidStr(xmlContents.get('notes')):
            notes = utils.getStrFromDict(
                d = xmlContents,
                key = 'notes',
                clean = True,
                htmlUnescape = True,
            )

        phraseSoundUrl: str | None = None
        if 'phrasesound' in xmlContents and utils.isValidUrl(xmlContents.get('phrasesound')):
            phraseSoundUrl = utils.getStrFromDict(xmlContents, 'phrasesound')

        translation = utils.getStrFromDict(xmlContents, 'translation')

        transliteratedSentence: str | None = None
        if 'wotd:transliteratedSentence' in xmlContents and utils.isValidStr(xmlContents.get('wotd:transliteratedSentence')):
            transliteratedSentence = utils.getStrFromDict(
                d = xmlContents,
                key = 'wotd:transliteratedSentence',
                clean = True,
            )

        transliteratedWord: str | None = None
        if 'wotd:transliteratedWord' in xmlContents and utils.isValidStr(xmlContents.get('wotd:transliteratedWord')):
            transliteratedWord = utils.getStrFromDict(
                d = xmlContents,
                key = 'wotd:transliteratedWord',
                clean = True,
            )

        wordSoundUrl: str | None = None
        if 'wordsound' in xmlContents and utils.isValidUrl(xmlContents.get('wordsound')):
            wordSoundUrl = utils.getStrFromDict(xmlContents, 'wordsound')

        word = utils.getStrFromDict(xmlContents, 'word', clean = True)
        wordType = utils.getStrFromDict(xmlContents, 'wordtype', clean = True)

        return TransparentResponse(
            date = date,
            enPhrase = enPhrase,
            fnPhrase = fnPhrase,
            langName = langName,
            notes = notes,
            phraseSoundUrl = phraseSoundUrl,
            translation = translation,
            transliteratedSentence = transliteratedSentence,
            transliteratedWord = transliteratedWord,
            word = word,
            wordSoundUrl = wordSoundUrl,
            wordType = wordType,
        )
