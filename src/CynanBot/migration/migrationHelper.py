import json
from typing import Any, Dict, List, Optional

import aiofiles
import aiofiles.ospath
import misc.utils as utils
from storage.backingDatabase import BackingDatabase
from timber.timberInterface import TimberInterface


class MigrationHelper():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        migrationsFile: str = 'CynanBotCommon/migration/migrations.json'
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(migrationsFile):
            raise ValueError(f'migrationsFile argument is malformed: \"{migrationsFile}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__migrationsFile: str = migrationsFile

        self.__migrationsPerformed: bool = False

    async def performMigrations(self):
        if self.__migrationsPerformed:
            self.__timber.log('MigrationHelper', 'Attempted to run migrations, but they have already been performed!')
            return

        self.__migrationsPerformed = True
        self.__timber.log('MigrationHelper', 'Performing migrations...')

        jsonContents = await self.__readJson()
        await self.__performUserNameChangeMigrations(jsonContents.get('userNameChanges'))

        self.__timber.log('MigrationHelper', 'Migrations complete')

    async def __performUserNameChangeMigrations(self, jsonContents: Optional[List[Dict[str, str]]]):
        if not utils.hasItems(jsonContents):
            return

        self.__timber.log('MigrationHelper', 'Performing user name change migrations...')

        for entry in jsonContents:
            newUserName = utils.getStrFromDict(entry, 'newUserName')
            oldUserName = utils.getStrFromDict(entry, 'oldUserName')

            await self.__performUserNameChangeMigration(
                newUserName = newUserName,
                oldUserName = oldUserName
            )

        self.__timber.log('MigrationHelper', 'User name change migrations complete')

    async def __performUserNameChangeMigration(self, newUserName: str, oldUserName: str):
        if not utils.isValidStr(newUserName):
            raise ValueError(f'newUserName argument is malformed: \"{newUserName}\"')
        elif not utils.isValidStr(oldUserName):
            raise ValueError(f'oldUserName argument is malformed: \"{oldUserName}\"')

        self.__timber.log('MigrationHelper', f'Performing user name change migration of \"{oldUserName}\" to \"{newUserName}\"...')

        # TODO
        # rename in users repository file
        # correct cuteness column names
        # correct shiny trivia column names
        # correct trivia emote column names
        # correct trivia game controller column names
        # correct trivia history column names
        # correct trivia score column names

        self.__timber.log('MigrationHelper', f'User name change migration of \"{oldUserName}\" to \"{newUserName}\" complete')

    async def __readJson(self) -> Dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__migrationsFile):
            raise FileNotFoundError(f'Migrations file not found: \"{self.__migrationsFile}\"')

        async with aiofiles.open(self.__migrationsFile, mode = 'r', encoding = 'utf-8') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from migrations file: \"{self.__migrationsFile}\"')

        return jsonContents
