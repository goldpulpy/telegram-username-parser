"""Client session module"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path

from telethon import TelegramClient, errors

logger = logging.getLogger(__name__)


class SessionStorageInterface(ABC):
    """Session storage interface"""

    @property
    @abstractmethod
    def session_path(self) -> Path:
        """Get session path"""


class FileSessionStorage(SessionStorageInterface):
    """File session storage"""

    def __init__(self, session_dir: str, api_id: int) -> None:
        """Initialize session storage

        :param session_dir: Session directory
        :param api_id: API ID
        """
        self._dir = Path(session_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._session_path = self._dir / f"session_{api_id}"

    @property
    def session_path(self) -> Path:
        """Get session path"""
        return self._session_path


class SessionMaker:
    """Telegram client"""

    def __init__(
        self,
        phone_number: str,
        api_id: int,
        api_hash: str,
        session_storage: SessionStorageInterface,
    ) -> None:
        """Initialize client

        :param phone_number: Phone number
        :param api_id: API ID
        :param api_hash: API hash
        :param session_storage: Session storage
        """
        self._phone_number = phone_number
        self._api_id = api_id
        self._api_hash = api_hash
        self._session_storage = session_storage

    async def make_session(self) -> TelegramClient:
        """Make session

        :return: Telegram client
        """
        client = TelegramClient(
            session=self._session_storage.session_path,
            api_id=self._api_id,
            api_hash=self._api_hash,
        )
        try:
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(self._phone_number)
                try:
                    await client.sign_in(
                        self._phone_number,
                        input(
                            ">>> Enter the confirmation code for "
                            f"{self._phone_number}: ",
                        ),
                    )
                except errors.SessionPasswordNeededError:
                    await client.sign_in(
                        password=input(">>> Enter 2FA password: "),
                    )

            logger.info("Account %s authenticated", self._phone_number)
            return client
        except Exception as e:
            logger.error("Authentication error: %s", e)
            raise
