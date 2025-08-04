"""Username parser for telegram."""

import asyncio
import logging
from argparse import ArgumentParser, Namespace

from app.config import JsonConfigLoader
from app.parser import BaseParser, ChannelParser, MessageHistoryParser
from app.result import FileStorage, UserResult
from app.session import FileSessionStorage, SessionMaker

logging.getLogger("telethon").setLevel(level=logging.ERROR)
logger = logging.getLogger("unparser")


async def parse(result: UserResult, strategy: BaseParser) -> None:
    """Parse the target entity.

    :param result: result storage
    :param strategy: parsing strategy
    """
    added = 0
    async for username in strategy.parse():
        added += result.add_user(username)

    logger.info(
        "Finished parsing: parsed %s elements, %s users added",
        strategy.parsed,
        added,
    )


async def main(args: Namespace) -> None:
    """Entry point.

    :param args: arguments from the command line
    :param target_username: target username
    """
    config = JsonConfigLoader.load(args.config)
    result = UserResult(FileStorage(args.result_directory))

    session_storage = FileSessionStorage(args.session_directory, config.api_id)
    sessionmaker = SessionMaker(
        phone_number=config.phone,
        api_id=config.api_id,
        api_hash=config.api_hash,
        session_storage=session_storage,
    )
    session = await sessionmaker.make_session()
    target_username = input(">>> Enter the target channel/chat username: ")

    await parse(result, ChannelParser(session, target_username))

    logger.info("Start message history parsing...")
    await parse(result, MessageHistoryParser(session, target_username))

    logger.info(
        "Result file: %s, users: %s, dublicates: %s",
        result.result_path,
        len(result),
        result.dublicates,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the config file",
        default="config.json",
    )
    parser.add_argument(
        "--result_directory",
        type=str,
        help="Path to the result directory",
        default="result",
    )
    parser.add_argument(
        "--session_directory",
        type=str,
        help="Path to the session directory",
        default="sessions",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s - %(levelname)s:%(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger.info("Debug mode is %s", args.debug)
    logger.debug("Args: %s", args)
    try:
        asyncio.run(main(args))

    except (KeyboardInterrupt, SystemExit):
        logger.info("Exiting...")

    except Exception:
        logger.exception("Unexpected error")

    finally:
        input("Press Enter to exit...")
