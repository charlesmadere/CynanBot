from typing import Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBot.cheerActions.cheerActionRequirement import CheerActionRequirement
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
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
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface):
            raise ValueError(f'cheerActionIdGenerator argument is malformed: \"{cheerActionIdGenerator}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(maximumPerUser):
            raise ValueError(f'maximumPerUser argument is malformed: \"{maximumPerUser}\"')
        elif maximumPerUser < 1 or maximumPerUser > 16:
            raise ValueError(f'maximumPerUser argument is out of bounds: {maximumPerUser}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__cheerActionIdGenerator: CheerActionIdGeneratorInterface = cheerActionIdGenerator
        self.__timber: TimberInterface = timber
        self.__maximumPerUser: int = maximumPerUser

        self.__isDatabaseReady: bool = False
        self.__cache: Dict[str, Optional[List[CheerAction]]] = dict()

    async def addAction(
        self,
        actionRequirement: CheerActionRequirement,
        actionType: CheerActionType,
        amount: int,
        durationSeconds: int,
        userId: str
    ) -> CheerAction:
        if not isinstance(actionRequirement, CheerActionRequirement):
            raise ValueError(f'actionRequirement argument is malformed: \"{actionRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise ValueError(f'cheerActionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(amount):
            raise ValueError(f'amount argument is malformed: \"{amount}\"')
        elif amount < 1 or amount > utils.getIntMaxSafeSize():
            raise ValueError(f'amount argument is out of bounds: {amount}')
        elif not utils.isValidInt(durationSeconds):
            raise ValueError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1:
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif durationSeconds > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        actions = await self.getActions(userId)

        if len(actions) + 1 > self.__maximumPerUser:
            raise TooManyCheerActionsException(f'Attempted to add new cheer action for {userId=} but they already have the maximum number of cheer actions (actions len: {len(actions)}) ({self.__maximumPerUser=})')

        for action in actions:
            if action.getAmount() == amount:
                raise CheerActionAlreadyExistsException(f'Attempted to add new cheer action for {userId=} but they already have a cheer action that requires the given amount ({amount}): {action=}')

        actionId: Optional[str] = None
        action: Optional[CheerAction] = None

        while actionId is None or action is not None:
            actionId = await self.__cheerActionIdGenerator.generateActionId()
            action = await self.getAction(
                actionId = actionId,
                userId = userId
            )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO cheeractions (actionid, actionrequirement, actiontype, amount, durationseconds, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            actionId, actionRequirement.toStr(), actionType.toStr(), amount, durationSeconds, userId
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

    async def deleteAction(self, actionId: str, userId: str) -> Optional[CheerAction]:
        if not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

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

    async def getAction(self, actionId: str, userId: str) -> Optional[CheerAction]:
        if not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        actions = await self.getActions(userId)

        if not utils.hasItems(actions):
            return None

        for action in actions:
            if action.getActionId() == actionId:
                return action

        return None

    async def getActions(self, userId: str) -> List[CheerAction]:
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        if userId in self.__cache:
            return self.__cache[userId]

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cheeractions.actionid, cheeractions.actionrequirement, cheeractions.actiontype, cheeractions.amount, cheeractions.durationseconds, cheeractions.userid, userids.username FROM cheeractions
                INNER JOIN userids ON cheeractions.userid = userids.userid
                WHERE cheeractions.userid = $1
                ORDER BY cheeractions.amount DESC
            ''',
            userId
        )

        await connection.close()
        actions: List[CheerAction] = list()

        if utils.hasItems(records):
            for record in records:
                actions.append(CheerAction(
                    actionId = record[0],
                    actionRequirement = CheerActionRequirement.fromStr(record[1]),
                    actionType = CheerActionType.fromStr(record[2]),
                    amount = record[3],
                    durationSeconds = record[4],
                    userId = record[5],
                    userName = record[6]
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
                        actionrequirement text NOT NULL,
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
                        actionrequirement TEXT NOT NULL,
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
