import sys
from typing import Union

from . import exceptions

_ACTIONS = (
    'store_true',
    'store_false',
    'append',
    'default'
)


class Namespace(object):
    def __repr__(self):
        attr = [i for i in self.__dir__() if not i.startswith('__')]
        repr = 'Namespace('

        for c, a in enumerate(attr):
            value = self.__getattribute__(a)

            if isinstance(value, str):
                value = f'"{value}"'

            if c == len(attr) - 1:
                repr += f'{a}={value})'
            else:
                repr += f'{a}={value}, '

        return repr


class ArgEasy(object):
    def __init__(
        self,
        name: str = None,
        description: str = None,
        version: str = None
    ) -> None:
        """Create a new instance of ArgEasy.

        :param name: Application name, defaults to None
        :type name: str, optional
        :param description: Application description, defaults to None
        :type description: str, optional
        :param version: Application version, defaults to None
        :type version: str, optional
        """

        self._commands = {}
        self._flags = {}
        self.namespace = Namespace()

        self.project_name = name
        self.description = description
        self.version = version

        # add default flags
        self.add_flag('--help', 'View the help', action='store_true')
        self.add_flag('--version', 'View the version', action='store_true')

    def add_argument(
        self,
        name: str,
        help: str,
        action: str = 'default',
        max_append: str = '*'
    ) -> None:
        """Adds a new argument.

        The available actions are:
        default (returns the next argument as value),
        store_true, store_false, and append.

        :param name: Argument name
        :type name: str
        :param help: Usage help for the argument
        :type help: str
        :param action: Argument action, defaults to 'default'
        :type action: str, optional
        :param max_append: If the action is "append", this
        parameter sets the maximum number of items, defaults to '*'
        :type max_append: str, optional
        :raises Exception: Action not recognized
        """

        if action not in self._actions:
            raise Exception('Action not recognized')

        self._commands[name] = {
            'help': help,
            'action': action,
            'max_append': max_append
        }

        setattr(self.namespace, name, None)

    def add_flag(
        self,
        name: str,
        help: str,
        action: str = 'default',
        max_append: str = '*'
    ) -> None:
        """Adds a new flag.

        The available actions are:
        default (returns the next argument as value),
        store_true, store_false, and append.

        The flag name can have only
        one hyphen if the flag has
        only one letter (-h), or two
        hyphens if it is a word
        (--help).

        :param name: Flag name
        :type name: str
        :param help: Help text
        :type help: str
        :param action: Flag action, defaults to 'default'
        :type action: str, optional
        :param required: If flag is required, defaults to False
        :type required: bool, optional
        """

        if action not in self._actions:
            raise Exception('Action not recognized')

        self._flags[name] = {
            'help': help,
            'action': action,
            'max_append': max_append
        }

        name = name.strip('-')
        name = name.replace('-', '_')

        setattr(self.namespace, name, None)
