"""Parser for telegram"""
import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser

logger = logging.getLogger(__name__)


class ParsedCounter:
    """Counter for parsed elements"""

    def __init__(self) -> None:
        self._parsed = 0

    @property
    def parsed(self) -> int:
        """Count of parsed elements"""
        return self._parsed


class BaseParser(ABC, ParsedCounter):
    """Parser for telegram"""

    def __init__(
        self,
        client: TelegramClient,
        target_entity: str,
    ) -> None:
        """
        Initialize parser

        :param client: Telegram client
        :param target_entity: Target entity
        """
        self._client = client
        self._target_entity = target_entity
        ParsedCounter.__init__(self)

    @abstractmethod
    async def parse(self) -> AsyncGenerator[str, None]:
        """
        Parse method
        """
        pass


class ChannelParser(BaseParser, ParsedCounter):
    """Parser for telegram channel"""

    def __init__(
        self,
        client: TelegramClient,
        target_entity: str,
    ) -> None:
        """
        Initialize channel parser

        :param client: Telegram client
        :param target_entity: Target entity
        """
        super().__init__(client, target_entity)
        ParsedCounter.__init__(self)

    async def parse(self) -> AsyncGenerator[str, None]:
        """
        Get participants

        :param limit: Limit of participants
        :return: Async generator of participants
        """

        while True:
            participants = await self._client(
                GetParticipantsRequest(
                    channel=self._target_entity,
                    offset=self._parsed,
                    limit=200,
                    filter=ChannelParticipantsSearch(""),
                    hash=0,
                )
            )
            if not participants.users:
                break

            with_username = 0
            for participant in participants.users:
                if participant.username:
                    with_username += 1
                    yield participant.username

            logger.info(
                "Get participants: %s, with username: %s",
                len(participants.users), with_username
            )
            self._parsed += len(participants.users)


class MessageHistoryParser(BaseParser, ParsedCounter):
    """Parser for telegram message"""

    def __init__(
        self,
        client: TelegramClient,
        target_entity: str,
    ) -> None:
        """
        Initialize message parser

        :param client: Telegram client
        :param target_entity: Target entity
        """
        super().__init__(client, target_entity)
        ParsedCounter.__init__(self)

    async def parse(self) -> AsyncGenerator[str, None]:
        """
        Get messages

        :param limit: Limit of messages
        :return: Async generator of messages
        """
        while True:
            messages = await self._client(
                GetHistoryRequest(
                    peer=self._target_entity,
                    offset_id=0,
                    offset_date=None,
                    add_offset=self._parsed,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
            if not messages.messages:
                break

            with_username = 0
            for message in messages.messages:
                if isinstance(message.from_id, PeerUser):
                    user = await self._client.get_entity(
                        message.from_id.user_id
                    )
                    if user.username:
                        with_username += 1
                        yield user.username

            logger.info(
                "Get messages: %s, with username: %s",
                len(messages.messages), with_username
            )
            self._parsed += len(messages.messages)
