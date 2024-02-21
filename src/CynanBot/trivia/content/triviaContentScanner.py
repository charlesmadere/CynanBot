from typing import Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.bannedPhrase import BannedPhrase
from CynanBot.contentScanner.bannedWord import BannedWord
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.bannedWordType import BannedWordType
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaContentScanner(TriviaContentScannerInterface):

    def __init__(
        self,
        bannedWordsRepository: BannedWordsRepositoryInterface,
        contentScanner: ContentScannerInterface,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        assert isinstance(bannedWordsRepository, BannedWordsRepositoryInterface), f"malformed {bannedWordsRepository=}"
        assert isinstance(contentScanner, ContentScannerInterface), f"malformed {contentScanner=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"

        self.__bannedWordsRepository: BannedWordsRepositoryInterface = bannedWordsRepository
        self.__contentScanner: ContentScannerInterface = contentScanner
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository

    async def __getAllPhrasesFromQuestion(self, question: AbsTriviaQuestion) -> Set[Optional[str]]:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        phrases: Set[Optional[str]] = set()
        await self.__contentScanner.updatePhrasesContent(phrases, question.getQuestion())
        await self.__contentScanner.updatePhrasesContent(phrases, question.getPrompt())

        if question.hasCategory():
            await self.__contentScanner.updatePhrasesContent(phrases, question.getCategory())

        for correctAnswer in question.getCorrectAnswers():
            await self.__contentScanner.updatePhrasesContent(phrases, correctAnswer)

        for response in question.getResponses():
            await self.__contentScanner.updatePhrasesContent(phrases, response)

        return phrases

    async def __getAllWordsFromQuestion(self, question: AbsTriviaQuestion) -> Set[Optional[str]]:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        words: Set[Optional[str]] = set()
        await self.__contentScanner.updateWordsContent(words, question.getQuestion())
        await self.__contentScanner.updateWordsContent(words, question.getPrompt())

        if question.hasCategory():
            await self.__contentScanner.updateWordsContent(words, question.getCategory())

        for correctAnswer in question.getCorrectAnswers():
            await self.__contentScanner.updateWordsContent(words, correctAnswer)

        for response in question.getResponses():
            await self.__contentScanner.updateWordsContent(words, response)

        return words

    async def verify(self, question: Optional[AbsTriviaQuestion]) -> TriviaContentCode:
        if question is None:
            return TriviaContentCode.IS_NONE

        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        coreContentCode = await self.__verifyQuestionCoreContent(question)
        if coreContentCode is not TriviaContentCode.OK:
            return coreContentCode

        responsesContentCode = await self.__verifyQuestionResponseCount(question)
        if responsesContentCode is not TriviaContentCode.OK:
            return responsesContentCode

        lengthsContentCode = await self.__verifyQuestionContentLengths(question)
        if lengthsContentCode is not TriviaContentCode.OK:
            return lengthsContentCode

        urlContentCode = await self.__verifyQuestionDoesNotContainUrl(question)
        if urlContentCode is not TriviaContentCode.OK:
            return urlContentCode

        contentSanityCode = await self.__verifyQuestionContentProfanity(question)
        if contentSanityCode is not TriviaContentCode.OK:
            return contentSanityCode

        return TriviaContentCode.OK

    async def __verifyQuestionContentLengths(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        maxQuestionLength = await self.__triviaSettingsRepository.getMaxQuestionLength()

        if len(question.getQuestion()) >= maxQuestionLength:
            self.__timber.log('TriviaContentScanner', f'Trivia question is too long (max is {maxQuestionLength}): {question.getQuestion()}')
            return TriviaContentCode.QUESTION_TOO_LONG

        maxPhraseAnswerLength = await self.__triviaSettingsRepository.getMaxPhraseAnswerLength()

        if question.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER:
            for correctAnswer in question.getCorrectAnswers():
                if len(correctAnswer) >= maxPhraseAnswerLength:
                    self.__timber.log('TriviaContentScanner', f'Trivia answer is too long (max is {maxPhraseAnswerLength}): {question.getCorrectAnswers()}')
                    return TriviaContentCode.ANSWER_TOO_LONG

        maxAnswerLength = await self.__triviaSettingsRepository.getMaxAnswerLength()

        for response in question.getResponses():
            if len(response) >= maxAnswerLength:
                self.__timber.log('TriviaContentScanner', f'Trivia response is too long (max is {maxAnswerLength}): {question.getResponses()}')
                return TriviaContentCode.ANSWER_TOO_LONG

        return TriviaContentCode.OK

    async def __verifyQuestionContentProfanity(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        phrases = await self.__getAllPhrasesFromQuestion(question)
        words = await self.__getAllWordsFromQuestion(question)
        absBannedWords = await self.__bannedWordsRepository.getBannedWordsAsync()

        for absBannedWord in absBannedWords:
            if absBannedWord.getType() is BannedWordType.EXACT_WORD:
                bannedWord: BannedWord = absBannedWord

                if bannedWord.getWord() in words:
                    self.__timber.log('TriviaContentScanner', f'Trivia content contains a banned word ({absBannedWord}): \"{bannedWord.getWord()}\"')
                    return TriviaContentCode.CONTAINS_BANNED_CONTENT
            elif absBannedWord.getType() is BannedWordType.PHRASE:
                bannedPhrase: BannedPhrase = absBannedWord

                for phrase in phrases:
                    if bannedPhrase.getPhrase() in phrase:
                        self.__timber.log('TriviaContentScanner', f'Trivia content contains a banned phrase ({absBannedWord}): \"{phrase}\"')
                        return TriviaContentCode.CONTAINS_BANNED_CONTENT
            else:
                raise RuntimeError(f'unknown BannedWordType ({absBannedWord}): \"{absBannedWord.getType()}\"')

        return TriviaContentCode.OK

    async def __verifyQuestionCoreContent(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        if not utils.isValidStr(question.getQuestion()):
            self.__timber.log('TriviaContentScanner', f'Trivia question ({question}) contains an empty question: \"{question.getQuestion()}\"')
            return TriviaContentCode.CONTAINS_EMPTY_STR

        if question.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER and not question.hasCategory():
            # This means that we are requiring "question-answer" style trivia questions to have
            # a category, which I think is probably fine? (this is an opinion situation)
            self.__timber.log('TriviaContentScanner', f'Trivia question ({question}) contains an empty category: \"{question.getCategory()}\"')
            return TriviaContentCode.CONTAINS_EMPTY_STR

        for response in question.getResponses():
            if not utils.isValidStr(response):
                self.__timber.log('TriviaContentScanner', f'Trivia question ({question}) contains an empty response: \"{response}\"')
                return TriviaContentCode.CONTAINS_EMPTY_STR

        return TriviaContentCode.OK

    async def __verifyQuestionDoesNotContainUrl(self, question: AbsTriviaQuestion):
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        if utils.containsUrl(question.getQuestion()):
            self.__timber.log('TriviaContentScanner', f'Trivia question\'s ({question}) question contains a URL: \"{question.getQuestion()}\"')
            return TriviaContentCode.CONTAINS_URL

        if utils.containsUrl(question.getCategory()):
            self.__timber.log('TriviaContentScanner', f'Trivia question\'s ({question}) category contains a URL: \"{question.getCategory()}\"')
            return TriviaContentCode.CONTAINS_URL

        for response in question.getResponses():
            if utils.containsUrl(response):
                self.__timber.log('TriviaContentScanner', f'Trivia question\'s ({question}) response contains a URL: \"{response}\"')
                return TriviaContentCode.CONTAINS_URL

        return TriviaContentCode.OK

    async def __verifyQuestionResponseCount(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"

        if question.getTriviaType() is not TriviaQuestionType.MULTIPLE_CHOICE:
            return TriviaContentCode.OK

        responses = question.getResponses()
        minMultipleChoiceResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()

        if not utils.hasItems(responses) or len(responses) < minMultipleChoiceResponses:
            self.__timber.log('TriviaContentScanner', f'Trivia question has too few multiple choice responses (min is {minMultipleChoiceResponses}): {responses}')
            return TriviaContentCode.TOO_FEW_MULTIPLE_CHOICE_RESPONSES

        return TriviaContentCode.OK
