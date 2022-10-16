import asyncio
import queue
from asyncio import AbstractEventLoop
from collections import defaultdict
from queue import SimpleQueue
from typing import Dict, List

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.twitch.twitchAccessTokenMissingException import \
    TwitchAccessTokenMissingException
from CynanBotCommon.twitch.twitchCredentialsProviderInterface import \
    TwitchCredentialsProviderInterface
from CynanBotCommon.twitch.twitchExpiresInMissingException import \
    TwitchExpiresInMissingException
from CynanBotCommon.twitch.twitchJsonException import TwitchJsonException
from CynanBotCommon.twitch.twitchNetworkException import TwitchNetworkException
from CynanBotCommon.twitch.twitchRefreshTokenMissingException import \
    TwitchRefreshTokenMissingException
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.users.userInterface import UserInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository
from twitchio import Client
from twitchio.ext import pubsub
from twitchio.ext.pubsub import PubSubPool
from twitchio.ext.pubsub.topics import Topic

from twitch.pubSubEntry import PubSubEntry


class PubSubUtils():

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        client: Client,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchCredentialsProviderInterface: TwitchCredentialsProviderInterface,
        twitchTokensRepository: TwitchTokensRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepositoryInterface,
        maxConnectionsPerTwitchChannel: int = 8,
        queueTimeoutSeconds: int = 3
    ):
        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif client is None:
            raise ValueError(f'client argument is malformed: \"{client}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif twitchCredentialsProviderInterface is None:
            raise ValueError(f'twitchCredentialsProviderInterface argument is malformed: \"{twitchCredentialsProviderInterface}\"')
        elif twitchTokensRepository is None:
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(maxConnectionsPerTwitchChannel):
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is malformed: \"{maxConnectionsPerTwitchChannel}\"')
        elif maxConnectionsPerTwitchChannel < 2 or maxConnectionsPerTwitchChannel > 16:
            raise ValueError(f'maxConnectionsPerTwitchChannel argument is out of bounds: {maxConnectionsPerTwitchChannel}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 2 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchCredentialsProviderInterface: TwitchCredentialsProviderInterface = twitchCredentialsProviderInterface
        self.__twitchTokensRepository: TwitchTokensRepository = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__maxConnectionsPerTwitchChannel: int = maxConnectionsPerTwitchChannel
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__isManagingPubSub: bool = False
        self.__isStarted: bool = False
        self.__pubSubEntries: Dict[str, SimpleQueue[Topic]] = defaultdict(lambda: SimpleQueue())

        self.__pubSubPool: PubSubPool = PubSubPool(
            client = client,
            max_pool_size = max(32, maxConnectionsPerTwitchChannel * 4),
            max_connection_topics = max(128, maxConnectionsPerTwitchChannel * 16)
        )

    async def __getSubscribeReadyPubSubEntries(self) -> List[PubSubEntry]:
        twitchHandles = await self.__twitchTokensRepository.getExpiringTwitchHandles()
        users: List[UserInterface] = None

        if twitchHandles is None:
            # if twitchHandles is None, then we must do a full validate and refresh
            users = await self.__usersRepository.getUsersAsync()
        elif len(twitchHandles) == 0:
            # if twitchHandles is empty, then there is no need to do a validate or refresh of anyone
            return None
        else:
            # if twitchHandles has entries, then we will validate and refresh those specific users
            users = list()

            for twitchHandle in twitchHandles:
                users.append(await self.__usersRepository.getUserAsync(twitchHandle))

        usersAndTwitchTokens: Dict[UserInterface, str] = dict()

        for user in users:
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(user.getHandle())

            if utils.isValidStr(twitchAccessToken):
                usersAndTwitchTokens[user] = twitchAccessToken

        if not utils.hasItems(usersAndTwitchTokens):
            return None

        twitchClientId = await self.__twitchCredentialsProviderInterface.getTwitchClientId()
        twitchClientSecret = await self.__twitchCredentialsProviderInterface.getTwitchClientSecret()

        if not utils.isValidStr(twitchClientId) or not utils.isValidStr(twitchClientSecret):
            raise RuntimeError(f'twitchClientId ({twitchClientId}) and/or twitchClientSecret ({twitchClientSecret}) is malformed!')

        usersToRemove: List[UserInterface] = list()

        for user in usersAndTwitchTokens:
            try:
                await self.__twitchTokensRepository.validateAndRefreshAccessToken(
                    twitchClientId = twitchClientId,
                    twitchClientSecret = twitchClientSecret,
                    twitchHandle = user.getHandle()
                )

                usersAndTwitchTokens[user] = await self.__twitchTokensRepository.getAccessToken(user.getHandle())
            except (TwitchAccessTokenMissingException, TwitchExpiresInMissingException, TwitchJsonException, TwitchNetworkException, TwitchRefreshTokenMissingException) as e:
                # if we run into this error, that most likely means that this user changed
                # their password
                usersToRemove.append(user)
                self.__timber.log('PubSubUtils', f'Failed to validate and refresh access Twitch token for \"{user.getHandle()}\": {e}')

        if utils.hasItems(usersToRemove):
            for user in usersToRemove:
                del usersAndTwitchTokens[user]

        pubSubEntries: List[PubSubEntry] = list()

        for user in usersAndTwitchTokens:
            twitchAccessToken = usersAndTwitchTokens[user]

            userId = await self.__userIdsRepository.fetchUserIdAsInt(
                userName = user.getHandle(),
                twitchAccessToken = twitchAccessToken,
                twitchClientId = twitchClientId
            )

            pubSubEntries.append(PubSubEntry(
                userId = userId,
                userName = user.getHandle().lower(),
                topic = pubsub.channel_points(twitchAccessToken)[userId]
            ))

        return pubSubEntries

    def startPubSub(self):
        if self.__isStarted:
            self.__timber.log('PubSubUtils', 'Not starting PubSub as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('PubSubUtils', 'Starting PubSub...')
        self.__eventLoop.create_task(self.__startPubSubUpdateLoop())

    async def __startPubSubUpdateLoop(self):
        while True:
            self.__timber.log('PubSubUtils', 'Refreshing...')
            await self.__updatePubSubSubscriptions()
            generalSettings = await self.__generalSettingsRepository.getAllAsync()
            await asyncio.sleep(generalSettings.getRefreshPubSubTokensSeconds())

    async def __updatePubSubSubscriptions(self):
        if self.__isManagingPubSub:
            self.__timber('PubSubUtils', f'Unable to update PubSub subscriptions because it is currently working!')
            return

        self.__isManagingPubSub = True

        pubSubTopicsToAdd: List[Topic] = list()
        pubSubTopicsToRemove: List[Topic] = list()
        newPubSubEntries = await self.__getSubscribeReadyPubSubEntries()

        if utils.hasItems(newPubSubEntries):
            for newPubSubEntry in newPubSubEntries:
                pubSubTopicsToAdd.append(newPubSubEntry.getTopic())
                self.__pubSubEntries[newPubSubEntry.getUserName()].put(newPubSubEntry.getTopic())

        for userName, topicQueue in self.__pubSubEntries.items():
            try:
                while topicQueue.qsize() > self.__maxConnectionsPerTwitchChannel:
                    pubSubTopicsToRemove.append(topicQueue.get(block = True, timeout = self.__queueTimeoutSeconds))
            except queue.Empty as e:
                self.__timber.log('PubSubUtils', f'Encountered queue.Empty when attempting to fetch PubSub topic from \"{userName}\"\'s queue: {e}')

        if utils.hasItems(pubSubTopicsToAdd):
            self.__timber.log('PubSubUtils', f'Subscribing to {len(newPubSubEntries)} PubSub user(s)...')
            await self.__pubSubPool.subscribe_topics(pubSubTopicsToAdd)
            self.__timber.log('PubSubUtils', f'Finished subscribing to {len(newPubSubEntries)} PubSub user(s)')

        if utils.hasItems(pubSubTopicsToRemove):
            self.__timber.log('PubSubUtils', f'Unsubscribing from {len(pubSubTopicsToRemove)} PubSub user(s)...')
            await self.__pubSubPool.unsubscribe_topics(pubSubTopicsToRemove)
            self.__timber.log('PubSubUtils', f'Finished unsubscribing from {len(pubSubTopicsToRemove)} PubSub user(s)')

        self.__isManagingPubSub = False
