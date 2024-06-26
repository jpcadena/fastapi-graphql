"""
This script sets up different logging handlers for the Core module.
It provides console, file, and mail logging capabilities based on the
 provided settings.
"""

import logging
import os
from datetime import datetime
from logging.handlers import SMTPHandler

from pydantic import PositiveInt

from app.config.config import get_init_settings, get_settings
from app.config.init_settings import InitSettings
from app.config.settings import Settings


def _setup_console_handler(
    logger: logging.Logger, log_level: PositiveInt
) -> None:
    """
    Configure a console handler for the given logger
    :param logger: The logger instance to set up a console handler for
    :type logger: logging.Logger
    :param log_level: The log level for the console handler
    :type log_level: PositiveInt
    :return: None
    :rtype: NoneType
    """
    stream: logging.StreamHandler = logging.StreamHandler()  # type: ignore
    stream.setLevel(log_level)
    logger.addHandler(stream)


def _setup_mail_handler(
    logger: logging.Logger,
    log_level: PositiveInt,
    settings: Settings = get_settings(),
) -> None:
    """
    Configure a mail handler for the given logger
    :param logger: The logger instance to set up a mail handler for
    :type logger: logging.Logger
    :param log_level: The log level for the mail handler
    :type log_level: PositiveInt
    :return: None
    :rtype: NoneType
    """
    if not settings.SMTP_USER:
        raise AttributeError("Mail server is not set.")
    if not settings.EMAILS_FROM_EMAIL:
        raise AttributeError("Mail from address is not set.")
    if not settings.SMTP_USER:
        raise AttributeError("Mail to address is not set.")
    if not settings.MAIL_SUBJECT:
        raise AttributeError("Mail subject is not set.")
    if not settings.MAIL_TIMEOUT:
        raise AttributeError("Mail timeout is not set.")
    if log_level == logging.CRITICAL:
        credentials: tuple[str, str] = (
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
        )
        mail_handler = SMTPHandler(
            mailhost=settings.SMTP_USER,
            fromaddr=settings.EMAILS_FROM_EMAIL,
            toaddrs=settings.SMTP_USER,
            subject=settings.MAIL_SUBJECT,
            credentials=credentials,
            timeout=settings.MAIL_TIMEOUT,
        )
        mail_handler.setLevel(log_level)
        logger.addHandler(mail_handler)


def _create_logs_folder(init_settings: InitSettings) -> str:
    """
    Create a logs folder if it doesn't already exist
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :return: The path to the logs folder
    :rtype: str
    """
    project_root: str = os.path.dirname(os.path.abspath(__file__))
    while os.path.basename(project_root) != init_settings.PROJECT_NAME:
        project_root = os.path.dirname(project_root)
    logs_folder_path: str = f"{project_root}/logs"
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path, exist_ok=True)
    return logs_folder_path


def _build_log_filename(init_settings: InitSettings) -> str:
    """
    Create a log filename using the current date and configured date
     format.
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :return: The filename for the log file
    :rtype: str
    """
    return f"log-{datetime.now().strftime(init_settings.FILE_DATE_FORMAT)}.log"


def _configure_file_handler(
    log_filename: str, log_level: PositiveInt, init_settings: InitSettings
) -> logging.FileHandler:
    """
    Configure a file handler with the given filename and log level
    :param log_filename: The filename for the log file
    :type log_filename: str
    :param log_level: The log level for the file handler
    :type log_level: PositiveInt
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :return: A configured file handler
    :rtype: logging.FileHandle
    """
    formatter: logging.Formatter = logging.Formatter(
        init_settings.LOG_FORMAT, init_settings.DATE_FORMAT
    )
    file_handler: logging.FileHandler = logging.FileHandler(log_filename)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    return file_handler


def _setup_file_handler(
    logger: logging.Logger,
    log_level: PositiveInt,
    init_settings: InitSettings = get_init_settings(),
) -> None:
    """
    Configure a file handler for the given logger
    :param logger: The logger instance to set up a file handler for
    :type logger: logging.Logger
    :param log_level: The log level for the file handler
    :type log_level: PositiveInt
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :return: None
    :rtype: NoneType
    """
    logs_folder_path = _create_logs_folder(init_settings)
    log_filename = _build_log_filename(init_settings)
    filename_path: str = f"{logs_folder_path}/{log_filename}"
    file_handler = _configure_file_handler(
        filename_path, log_level, init_settings
    )
    logger.addHandler(file_handler)
    file_handler.flush()


def setup_logging(
    log_level: PositiveInt = logging.DEBUG,
    init_settings: InitSettings = get_init_settings(),
    settings: Settings = get_settings(),
) -> None:
    """
    Initialize logging for the application
    :param log_level: The log level to use for the application.
     Defaults to DEBUG
    :type log_level: PositiveInt
    :param init_settings: Dependency method for cached init setting object
    :type init_settings: InitSettings
    :param settings: Dependency method for cached setting object
    :type settings: Settings
    :return: None
    :rtype: NoneType
    """
    logger: logging.Logger = logging.getLogger()
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(log_level)
    _setup_console_handler(logger, log_level)
    _setup_mail_handler(logger, log_level, settings)
    _setup_file_handler(logger, log_level, init_settings)
