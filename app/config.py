"""Config for the app"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Config for the app"""

    api_id: int
    api_hash: str
    phone: str


class ConfigLoader(ABC):
    """Loader for the config"""

    @staticmethod
    @abstractmethod
    def load(path: str) -> Config:
        """Load the config

        :param path: path to the config file
        :return: Config
        """

    @staticmethod
    def validate_path(path: str) -> None:
        """Validate file path

        :param path: path to the config file
        """
        if not Path(path).exists():
            raise FileNotFoundError(f"Config file not found: {path}")


class JsonConfigLoader(ConfigLoader):
    """Config loader"""

    @staticmethod
    def load(path: str) -> Config:
        """Load the config

        :param path: path to the config file
        :return: Config
        """
        JsonConfigLoader.validate_path(path)

        with open(path, encoding="utf-8") as file:
            config = json.load(file)

        logger.info("Loaded config from %s", path)
        return Config(**config)
