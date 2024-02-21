from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.banned.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaVerifierInterface import TriviaVerifierInterface


class TriviaVerifier(TriviaVerifierInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaContentScanner: TriviaContentScannerInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaBanHelper, TriviaBanHelperInterface), f"malformed {triviaBanHelper=}"
        assert isinstance(triviaContentScanner, TriviaContentScannerInterface), f"malformed {triviaContentScanner=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"

        self.__timber: TimberInterface = timber
        self.__triviaBanHelper: TriviaBanHelperInterface = triviaBanHelper
        self.__triviaContentScanner: TriviaContentScannerInterface = triviaContentScanner
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository

    async def checkContent(
        self,
        question: Optional[AbsTriviaQuestion],
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaContentCode:
        if question is None:
            return TriviaContentCode.IS_NONE

        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"
        assert isinstance(triviaFetchOptions, TriviaFetchOptions), f"malformed {triviaFetchOptions=}"

        if not triviaFetchOptions.areQuestionAnswerTriviaQuestionsEnabled() and question.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.getTriviaType()} (triviaFetchOptions: {triviaFetchOptions})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE
        elif triviaFetchOptions.requireQuestionAnswerTriviaQuestion() and question.getTriviaType() is not TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaVerifier', f'The given TriviaType is illegal: {question.getTriviaType()} (triviaFetchOptions: {triviaFetchOptions})')
            return TriviaContentCode.ILLEGAL_TRIVIA_TYPE

        if await self.__triviaBanHelper.isBanned(
            triviaId = question.getTriviaId(),
            triviaSource = question.getTriviaSource()
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
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaContentCode:
        assert isinstance(question, AbsTriviaQuestion), f"malformed {question=}"
        if not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        assert isinstance(triviaFetchOptions, TriviaFetchOptions), f"malformed {triviaFetchOptions=}"

        contentCode = await self.__triviaHistoryRepository.verify(
            question = question, 
            emote = emote,
            twitchChannel = triviaFetchOptions.getTwitchChannel()
        )

        if contentCode is not TriviaContentCode.OK:
            return contentCode

        return TriviaContentCode.OK
