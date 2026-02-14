from .triviaContentCode import TriviaContentCode
from .triviaContentScannerInterface import TriviaContentScannerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ...contentScanner.bannedPhrase import BannedPhrase
from ...contentScanner.bannedWord import BannedWord
from ...contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from ...contentScanner.contentScannerInterface import ContentScannerInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TriviaContentScanner(TriviaContentScannerInterface):

    def __init__(
        self,
        bannedWordsRepository: BannedWordsRepositoryInterface,
        contentScanner: ContentScannerInterface,
        timber: TimberInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        if not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise TypeError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif not isinstance(contentScanner, ContentScannerInterface):
            raise TypeError(f'contentScanner argument is malformed: \"{contentScanner}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')

        self.__bannedWordsRepository: BannedWordsRepositoryInterface = bannedWordsRepository
        self.__contentScanner: ContentScannerInterface = contentScanner
        self.__timber: TimberInterface = timber
        self.__triviaSettings: TriviaSettingsInterface = triviaSettings

    async def __getAllPhrasesFromQuestion(self, question: AbsTriviaQuestion) -> set[str]:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        phrases: set[str] = set()
        await self.__contentScanner.updatePhrasesContent(phrases, question.question)
        await self.__contentScanner.updatePhrasesContent(phrases, question.category)

        for correctAnswer in question.correctAnswers:
            await self.__contentScanner.updatePhrasesContent(phrases, correctAnswer)

        for response in question.responses:
            await self.__contentScanner.updatePhrasesContent(phrases, response)

        return phrases

    async def __getAllWordsFromQuestion(self, question: AbsTriviaQuestion) -> set[str]:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        words: set[str] = set()
        await self.__contentScanner.updateWordsContent(words, question.question)
        await self.__contentScanner.updateWordsContent(words, question.category)

        for correctAnswer in question.correctAnswers:
            await self.__contentScanner.updateWordsContent(words, correctAnswer)

        for response in question.responses:
            await self.__contentScanner.updateWordsContent(words, response)

        return words

    async def verify(self, question: AbsTriviaQuestion | None) -> TriviaContentCode:
        if question is None:
            return TriviaContentCode.IS_NONE
        elif not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

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
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        maxQuestionLength = await self.__triviaSettings.getMaxQuestionLength()

        if len(question.question) >= maxQuestionLength:
            self.__timber.log('TriviaContentScanner', f'Trivia question is too long (max is {maxQuestionLength}): {question.question}')
            return TriviaContentCode.QUESTION_TOO_LONG

        maxPhraseAnswerLength = await self.__triviaSettings.getMaxPhraseAnswerLength()

        if question.triviaType is TriviaQuestionType.QUESTION_ANSWER:
            for correctAnswer in question.correctAnswers:
                if len(correctAnswer) >= maxPhraseAnswerLength:
                    self.__timber.log('TriviaContentScanner', f'Trivia answer is too long (max is {maxPhraseAnswerLength}): {question.correctAnswers}')
                    return TriviaContentCode.ANSWER_TOO_LONG

        maxAnswerLength = await self.__triviaSettings.getMaxAnswerLength()

        for response in question.responses:
            if len(response) >= maxAnswerLength:
                self.__timber.log('TriviaContentScanner', f'Trivia response is too long (max is {maxAnswerLength}): {question.responses}')
                return TriviaContentCode.ANSWER_TOO_LONG

        return TriviaContentCode.OK

    async def __verifyQuestionContentProfanity(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        phrases = await self.__getAllPhrasesFromQuestion(question)
        words = await self.__getAllWordsFromQuestion(question)
        absBannedWords = await self.__bannedWordsRepository.getBannedWordsAsync()

        for absBannedWord in absBannedWords:
            if isinstance(absBannedWord, BannedWord):
                bannedWord: BannedWord = absBannedWord

                if bannedWord.word in words:
                    self.__timber.log('TriviaContentScanner', f'Trivia content contains a banned word ({absBannedWord}) ({question=})')
                    return TriviaContentCode.CONTAINS_BANNED_CONTENT
            elif isinstance(absBannedWord, BannedPhrase):
                bannedPhrase: BannedPhrase = absBannedWord

                for phrase in phrases:
                    if bannedPhrase.phrase in phrase:
                        self.__timber.log('TriviaContentScanner', f'Trivia content contains a banned phrase ({absBannedWord}) ({question=})')
                        return TriviaContentCode.CONTAINS_BANNED_CONTENT
            else:
                raise RuntimeError(f'unknown BannedWordType ({absBannedWord=})')

        return TriviaContentCode.OK

    async def __verifyQuestionCoreContent(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not utils.isValidStr(question.question):
            self.__timber.log('TriviaContentScanner', f'Trivia question ({question}) contains an empty question: \"{question.question}\"')
            return TriviaContentCode.CONTAINS_EMPTY_STR

        if question.triviaType is TriviaQuestionType.QUESTION_ANSWER and not utils.isValidStr(question.category):
            # This means that we are requiring "question-answer" style trivia questions to have
            # a category, which I think is probably fine? (this is an opinion situation)
            self.__timber.log('TriviaContentScanner', f'Trivia question ({question}) contains an empty category: \"{question.category}\"')
            return TriviaContentCode.CONTAINS_EMPTY_STR

        for response in question.responses:
            if not utils.isValidStr(response):
                self.__timber.log('TriviaContentScanner', f'Trivia question ({question}) contains an empty response: \"{response}\"')
                return TriviaContentCode.CONTAINS_EMPTY_STR

        return TriviaContentCode.OK

    async def __verifyQuestionDoesNotContainUrl(self, question: AbsTriviaQuestion):
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if utils.containsUrl(question.question):
            self.__timber.log('TriviaContentScanner', f'Trivia question\'s ({question}) question contains a URL: \"{question.question}\"')
            return TriviaContentCode.CONTAINS_URL

        if utils.containsUrl(question.category):
            self.__timber.log('TriviaContentScanner', f'Trivia question\'s ({question}) category contains a URL: \"{question.category}\"')
            return TriviaContentCode.CONTAINS_URL

        for response in question.responses:
            if utils.containsUrl(response):
                self.__timber.log('TriviaContentScanner', f'Trivia question\'s ({question}) response contains a URL: \"{response}\"')
                return TriviaContentCode.CONTAINS_URL

        return TriviaContentCode.OK

    async def __verifyQuestionResponseCount(self, question: AbsTriviaQuestion) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if question.triviaType is not TriviaQuestionType.MULTIPLE_CHOICE:
            return TriviaContentCode.OK

        responses = question.responses
        minMultipleChoiceResponses = await self.__triviaSettings.getMinMultipleChoiceResponses()

        if responses is None or len(responses) == 0 or len(responses) < minMultipleChoiceResponses:
            self.__timber.log('TriviaContentScanner', f'Trivia question has too few multiple choice responses (min is {minMultipleChoiceResponses}): {responses}')
            return TriviaContentCode.TOO_FEW_MULTIPLE_CHOICE_RESPONSES

        return TriviaContentCode.OK
