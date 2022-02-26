from ctypes import Union
import sys


class ArgEasy(object):
    def __init__(
        self,
        description: str = None,
        version: str = None,
    ) -> None:
        """Inicializes the ArgEasy.

        :param description: Description of CLI, defaults to None
        :type description: str, optional
        :param version: Version of App, defaults to None
        :type version: str, optional
        """

        self._commands = {}
        self._modes = []

        self.version = version
        self.description = description

    def add_argument(
        self,
        name: str,
        help: str,
        mode: str
    ) -> None:
        if mode not in self._modes:
            raise Exception('Mode not recognized')

        self._commands[name] = {
            'help': help,
            'mode': mode
        }
