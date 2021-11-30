from abc import ABC, abstractmethod

import logging


class AbstractFancyLog(ABC):
    """Abstract class of the FancyLog package"""
    __slots__ = ('_logger',)

    _log: logging.Logger

    @abstractmethod
    def __init__(self, logger, *args, **kwargs) -> None:
        """The basic constructor. Creates a new instance of FancyLog using the
        specified arguments

        Args:
            logger:
            *args:
            **kwargs:
        """

        self._logger = logger
