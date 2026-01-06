from typing import Final

from .banned.triviaBanHelperInterface import TriviaBanHelperInterface
from .content.triviaContentCode import TriviaContentCode
from .content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from .history.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from .questions.absTriviaQuestion import AbsTriviaQuestion
from .questions.triviaQuestionType import TriviaQuestionType
from .triviaFetchOptions import TriviaFetchOptions
from .triviaVerifierInterface import TriviaVerifierInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class TriviaVerifier(TriviaVerifierInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaContentScanner: TriviaContentScannerInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise TypeError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaContentScanner, TriviaContentScannerInterface):
            raise TypeError(f'triviaContentScanner argument is malformed: \"{triviaContentScanner}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaBanHelper: Final[TriviaBanHelperInterface] = triviaBanHelper
        self.__triviaContentScanner: Final[TriviaContentScannerInterface] = triviaContentScanner
        self.__triviaHistoryRepository: Final[TriviaHistoryRepositoryInterface] = triviaHistoryRepository

    async def checkContent(
        self,
        question: AbsTriviaQuestion | None,
        triviaFetchOptions: TriviaFetchOptions,
    ) -> TriviaContentCode:
        if question is None:
            return TriviaContentCode.IS_NONE
        elif not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        if not triviaFetchOptions.areQuestionAnswerTriviaQuestionsEnabled() and question.triviaType is TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.triviaType} ({triviaFetchOptions=})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE
        elif triviaFetchOptions.requireQuestionAnswerTriviaQuestion() and question.triviaType is not TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.triviaType} ({triviaFetchOptions=})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE

        if await self.__triviaBanHelper.isBanned(
            triviaId = question.triviaId,
            triviaSource = question.triviaSource,
        ):
            return TriviaContentCode.IS_BANNED

        contentScannerCode = await self.__triviaContentScanner.verify(question)
        if contentScannerCode is not TriviaContentCode.OK:
            return contentScannerCode

        return TriviaContentCode.OK

    async def checkHistory(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions,
    ) -> TriviaContentCode:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        contentCode = await self.__triviaHistoryRepository.verify(
            question = question,
            emote = emote,
            twitchChannel = triviaFetchOptions.twitchChannel,
            twitchChannelId = triviaFetchOptions.twitchChannelId,
        )

        if contentCode is not TriviaContentCode.OK:
            return contentCode

        return TriviaContentCode.OK
