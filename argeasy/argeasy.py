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
        self._actions = []

        self.version = version
        self.description = description

    def add_argument(
        self,
        name: str,
        help: str,
        action: str
    ) -> None:
        """Add argument.

        :param name: Argument name
        :type name: str
        :param help: Help to argument
        :type help: str
        :param action: Argument action
        :type action: str
        :raises Exception: Action not recognized
        """

        if action not in self._actions:
            raise Exception('Action not recognized')

        self._commands[name] = {
            'help': help,
            'action': action
        }

    def _print_help(self) -> None:
        print(f'usage: [command] [**optional] [flags]')

        print('\ncommands:')
        for cmd, info in self._commands.items():
            print(f'    {cmd}: {info["help"]}')
