#!/bin/python3.7
"""
This file contains everything related to the command line interface
"""

import logging

import coloredlogs

from bird_image_classification_mva.config.config import LOG_LEVEL

FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='black', bold=True),
    name=dict(color='blue'),
    lineno=dict(color='blue'),
    message=dict(color='white'),
)


def get_logger(name: str, level: str = LOG_LEVEL) -> logging.Logger:
    """
    Returns the logger we use for output
    :param name: the name of your logger, usually __name__
    :param level: the level to which your logger logs
    :return: the logger
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    coloredlogs.install(
        level=level, logger=logger, fmt='%(asctime)s %(name)s: %(lineno)s %(levelname)s: %(message)s', field_styles=FIELD_STYLES
    )
    return logger

