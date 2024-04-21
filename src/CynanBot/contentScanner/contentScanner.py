import re
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.bannedPhrase import BannedPhrase
from CynanBot.contentScanner.bannedWord import BannedWord
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.bannedWordType import BannedWordType
from CynanBot.contentScanner.contentCode import ContentCode
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.timber.timberInterface import TimberInterface


class ContentScanner(ContentScannerInterface):

    def __init__(
        self,
        bannedWordsRepository: BannedWordsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise TypeError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__bannedWordsRepository: BannedWordsRepositoryInterface = bannedWordsRepository
        self.__timber: TimberInterface = timber

        self.__phraseRegEx: Pattern = re.compile(r'[a-z]+', re.IGNORECASE)
        self.__wordRegEx: Pattern = re.compile(r'\w', re.IGNORECASE)

    async def scan(self, message: str | None) -> ContentCode:
        if message is None:
            return ContentCode.IS_NONE
        elif not isinstance(message, str):
            raise TypeError(f'string argument is malformed: \"{message}\"')
        elif len(message) == 0:
            return ContentCode.IS_EMPTY
        elif message.isspace():
            return ContentCode.IS_BLANK

        if utils.containsUrl(message):
            self.__timber.log('ContentScanner', f'Content contains a URL: \"{message}\"')
            return ContentCode.CONTAINS_URL

        phrases: set[str] = set()
        await self.updatePhrasesContent(phrases, message)

        words: set[str] = set()
        await self.updateWordsContent(words, message)

        phrasesAndWordsContentCode = await self.__scanPhrasesAndWords(phrases, words)
        if phrasesAndWordsContentCode is not ContentCode.OK:
            return phrasesAndWordsContentCode

        return ContentCode.OK

    async def __scanPhrasesAndWords(
        self,
        phrases: set[str],
        words: set[str]
    ) -> ContentCode:
        if not isinstance(phrases, set):
            raise TypeError(f'phrases argument is malformed: \"{phrases}\"')
        elif not isinstance(words, set):
            raise TypeError(f'words argument is malformed: \"{words}\"')

        absBannedWords = await self.__bannedWordsRepository.getBannedWordsAsync()

        for absBannedWord in absBannedWords:
            if absBannedWord.getType() is BannedWordType.EXACT_WORD and isinstance(absBannedWord, BannedWord):
                bannedWord: BannedWord = absBannedWord

                if bannedWord.getWord() in words:
                    self.__timber.log('ContentScanner', f'Content contains a banned word ({bannedWord=}) ({phrases=}) ({words=})')
                    return ContentCode.CONTAINS_BANNED_CONTENT
            elif absBannedWord.getType() is BannedWordType.PHRASE and isinstance(absBannedWord, BannedPhrase):
                bannedPhrase: BannedPhrase = absBannedWord

                for phrase in phrases:
                    if bannedPhrase.getPhrase() in phrase:
                        self.__timber.log('ContentScanner', f'Content contains a banned phrase ({bannedPhrase=}) ({phrases=}) ({words=})')
                        return ContentCode.CONTAINS_BANNED_CONTENT
            else:
                raise RuntimeError(f'unknown BannedWordType ({absBannedWord}): \"{absBannedWord.getType()}\"')

        return ContentCode.OK

    async def updatePhrasesContent(
        self,
        phrases: set[str],
        string: str | None
    ):
        if not isinstance(phrases, set):
            raise TypeError(f'phrases argument is malformed: \"{phrases}\"')

        if not utils.isValidStr(string):
            return

        string = string.lower()
        words = self.__phraseRegEx.findall(string)

        if not utils.hasItems(words):
            return

        phrase = ' '.join(words)
        phrases.add(phrase)

    async def updateWordsContent(
        self,
        words: set[str],
        string: str | None
    ):
        if not isinstance(words, set):
            raise TypeError(f'words argument is malformed: \"{words}\"')

        if not utils.isValidStr(string):
            return

        splits = string.lower().split()

        if not utils.hasItems(splits):
            return

        for split in splits:
            words.add(split)
            characters = self.__wordRegEx.findall(split)

            if not utils.hasItems(characters):
                continue

            word = ''.join(characters)
            words.add(word)
