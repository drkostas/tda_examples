from typing import List
import logging
from termcolor import colored

from .abstract_fancy_log import AbstractFancyLog


class ColorizedLog(AbstractFancyLog):
    """ColorizedLog class of the FancyLog package"""

    __slots__ = ('_color', '_attrs', 'debug', 'info', 'warn', 'warning',
                 'error', 'exception', 'critical')

    _color: str
    _attrs: List

    def __init__(self, logger: logging.Logger, color: str = None, attrs: List = None):
        """
        Args:
            logger (logging.Logger):
            color (str):
            attrs (List):
        """

        self._color = color if color else 'white'
        self._attrs = attrs if attrs else ['bold']
        super().__init__(logger=logger)

    def __getattr__(self, name: str):
        """
        Args:
            name (str):
        """
        if name in ['debug', 'info', 'warn', 'warning',
                    'error', 'exception', 'critical']:
            return lambda s, *args: getattr(self._logger, name)(
                colored(s, color=self._color, attrs=self._attrs), *args)

        return getattr(self._logger, name)


# log = ColorizedLog(logging.getLogger(__name__))
