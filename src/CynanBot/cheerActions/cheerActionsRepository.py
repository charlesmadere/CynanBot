import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.exceptions import (
    CheerActionAlreadyExistsException, TimeoutDurationSecondsTooLongException,
    TooManyCheerActionsException)
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface


class CheerActionsRepository(CheerActionsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        cheerActionIdGenerator: CheerActionIdGeneratorInterface,
        timber: TimberInterface,
        maximumPerUser: int = 5
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface):
            raise TypeError(f'cheerActionIdGenerator argument is malformed: \"{cheerActionIdGenerator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(maximumPerUser):
            raise TypeError(f'maximumPerUser argument is malformed: \"{maximumPerUser}\"')
        elif maximumPerUser < 1 or maximumPerUser > 16:
            raise ValueError(f'maximumPerUser argument is out of bounds: {maximumPerUser}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__cheerActionIdGenerator: CheerActionIdGeneratorInterface = cheerActionIdGenerator
        self.__timber: TimberInterface = timber
        self.__maximumPerUser: int = maximumPerUser

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, list[CheerAction] | None] = dict()

    async def addAction(
        self,
        bitRequirement: CheerActionBitRequirement,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: int,
        userId: str
    ) -> CheerAction:
        if not isinstance(bitRequirement, CheerActionBitRequirement):
            raise TypeError(f'actionRequirement argument is malformed: \"{bitRequirement}\"')
        elif not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise TypeError(f'cheerActionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(amount):
            raise TypeError(f'amount argument is malformed: \"{amount}\"')
        elif amount < 1 or amount > utils.getIntMaxSafeSize():
            raise ValueError(f'amount argument is out of bounds: {amount}')
        elif not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1:
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif durationSeconds > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        actions = await self.getActions(userId)

        if len(actions) + 1 > self.__maximumPerUser:
            raise TooManyCheerActionsException(f'Attempted to add new cheer action for {userId=} but they already have the maximum number of cheer actions (actions len: {len(actions)}) ({self.__maximumPerUser=})')

        for action in actions:
            if action.getAmount() == amount:
                raise CheerActionAlreadyExistsException(f'Attempted to add new cheer action for {userId=} but they already have a cheer action that requires the given amount ({amount}): {action=}')

        actionId: str | None = None
        action: CheerAction | None = None

        while actionId is None or action is not None:
            actionId = await self.__cheerActionIdGenerator.generateActionId()
            action = await self.getAction(
                actionId = actionId,
                userId = userId
            )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO cheeractions (actionid, bitrequirement, streamstatusrequirement, actiontype, amount, durationseconds, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            actionId, bitRequirement.toStr(), streamStatusRequirement.getDatabaseString(), actionType.toStr(), amount, durationSeconds, userId
        )

        await connection.close()
        self.__cache.pop(userId, None)

        action = await self.getAction(
            actionId = actionId,
            userId = userId
        )

        if action is None:
            raise RuntimeError(f'Just finished creating a new action for user ID \"{userId}\", but it seems to not exist ({actionId})')

        self.__timber.log('CheerActionsRepository', f'Added new cheer action ({action=})')
        return action

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('CheerActionsRepository', 'Caches cleared')

    async def deleteAction(self, actionId: str, userId: str) -> CheerAction | None:
        if not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        action = await self.getAction(
            actionId = actionId,
            userId = userId
        )

        if action is None:
            self.__timber.log('CheerActionsRepository', f'Attempted to delete cheer action ID \"{actionId}\", but it does not exist in the database')
            return None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM cheeractions
                WHERE actionid = $1 AND userid = $2
            ''',
            actionId, userId
        )

        await connection.close()
        self.__cache.pop(action.getUserId(), None)
        self.__timber.log('CheerActionsRepository', f'Deleted cheer action ({actionId=}) ({userId=}) ({action=})')

        return action

    async def getAction(self, actionId: str, userId: str) -> CheerAction | None:
        if not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        actions = await self.getActions(userId)

        if actions is None or len(actions) == 0:
            return None

        for action in actions:
            if action.getActionId() == actionId:
                return action

        return None

    async def getActions(self, userId: str) -> list[CheerAction]:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        actions = self.__cache.get(userId, None)

        if actions is not None:
            return actions

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cheeractions.actionid, cheeractions.bitrequirement, cheeractions.streamstatusrequirement, cheeractions.actiontype, cheeractions.amount, cheeractions.durationseconds, cheeractions.userid, userids.username FROM cheeractions
                INNER JOIN userids ON cheeractions.userid = userids.userid
                WHERE cheeractions.userid = $1
                ORDER BY cheeractions.amount DESC
            ''',
            userId
        )

        await connection.close()
        actions = list()

        if records is not None and len(records) >= 1:
            for record in records:
                actions.append(CheerAction(
                    actionId = record[0],
                    bitRequirement = CheerActionBitRequirement.fromStr(record[1]),
                    streamStatusRequirement = CheerActionStreamStatusRequirement.fromStr(record[2]),
                    actionType = CheerActionType.fromStr(record[3]),
                    amount = record[4],
                    durationSeconds = record[5],
                    userId = record[6],
                    userName = record[7]
                ))

        self.__cache[userId] = actions
        return actions

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS cheeractions (
                        actionid public.citext NOT NULL,
                        bitrequirement text NOT NULL,
                        streamstatusrequirement text NOT NULL,
                        actiontype text NOT NULL,
                        amount integer NOT NULL,
                        durationseconds integer NOT NULL,
                        userid public.citext NOT NULL,
                        PRIMARY KEY (actionid, userid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS cheeractions (
                        actionid TEXT NOT NULL COLLATE NOCASE,
                        bitrequirement TEXT NOT NULL,
                        streamstatusrequirement TEXT NOT NULL,
                        actiontype TEXT NOT NULL,
                        amount INTEGER NOT NULL,
                        durationseconds INTEGER NOT NULL,
                        userid TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (actionid, userid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
