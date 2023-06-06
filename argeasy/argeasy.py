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
        version: str = None,
        usage: str = None
    ) -> None:
        """Create a new instance of ArgEasy.

        :param name: Application name, defaults to None
        :type name: str, optional
        :param description: Application description, defaults to None
        :type description: str, optional
        :param version: Application version, defaults to None
        :type version: str, optional
        :param usage: Application usage format, defaults to none
        :type usage: str, optional
        """

        self._flags = {}
        self._arguments = {}
        self.namespace = Namespace()

        self._project_name = name
        self._description = description
        self._version = version
        self._usage = usage

        self._args = sys.argv[1:]

        self.add_flag('--help', 'Show program help message', action='store_true')
        self.add_flag('--version', 'Show program version', action='store_true')

    def _help(self) -> None:
        print(f'{self._project_name} ({self._version})')
        print(f'usage: {self._usage}\n')

        if self._description:
            print(self._description)

        print(f'\nCommands and flags help:')

        for cmd, info in self._arguments.items():
            print(f'    \033[1m{cmd}\033[m: \033[33m{info["help"]}\033[m')

        print()

        for flag, info in self._flags.items():
            print(f'    \033[1m{flag}\033[m: \033[33m{info["help"]}\033[m')

    def _show_version(self) -> None:
        print(f'{self._project_name} (\033[33m{self._version}\033[m)')

    def add_argument(
        self,
        name: str,
        help: str,
        action: str = 'default',
        max_append: str = '*'
    ) -> None:
        """Adds a new argument.

        The available actions are:
        `default` (returns the next argument as value),
        `store_true`, `store_false`, and `append`.

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

        if action not in _ACTIONS:
            raise exceptions.InvalidActionError(f'Action {repr(action)} invalid')

        self._arguments[name] = {
            'help': help,
            'action': action,
            'max_append': max_append
        }

        name = name.replace('-', '_')
        setattr(self.namespace, name, None)

    def add_flag(
        self,
        name: str,
        help: str,
        action: str = 'default',
        max_append: str = '*'
    ) -> None:
        """Adds a new flag. The flag name can have
        one or two hyphens.

        The available actions are:
        `default` (returns the next argument as value),
        `store_true`, `store_false`, and `append`.

        :param name: Flag name
        :type name: str
        :param help: Help text
        :type help: str
        :param action: Flag action, defaults to 'default'
        :type action: str, optional
        :param required: If flag is required, defaults to False
        :type required: bool, optional
        """

        if action not in _ACTIONS:
            raise exceptions.InvalidActionError(f'Action {repr(action)} invalid')

        self._flags[name] = {
            'help': help,
            'action': action,
            'max_append': max_append
        }

        name = name.strip('-')
        name = name.replace('-', '_')

        setattr(self.namespace, name, None)

    def _parse_cmd(self, cmd: str, params: list) -> list:
        _full_args = {}
        _full_args.update(self._arguments)
        _full_args.update(self._flags)

        cmd_action = _full_args[cmd]['action']

        if cmd_action == 'store_true':
            param = True
        elif cmd_action == 'store_false':
            param = False
        elif cmd_action == 'default':
            try:
                param = params[0]
            except IndexError:
                print(f'\033[31minvalid use from {repr(cmd)} command\033[m')
                print(f'\033[33muse "--help" flag to see all commands\033[m')
                sys.exit(1)

            if param.startswith('-') or len(params) > 1:
                print(f'\033[31minvalid use from {repr(cmd)} command\033[m')
                print(f'\033[33muse "--help" flag to see all commands\033[m')
                sys.exit(1)

        cmd = cmd.strip('-')
        cmd = cmd.replace('-', '_')
        setattr(self.namespace, cmd, param)

    def parse(self) -> None:
        if not self._args:
            self._help()
            sys.exit(1)

        _full_args = {}
        _full_args.update(self._arguments)
        _full_args.update(self._flags)

        _args = self._args
        recognized_cmd = []
        commands = {}

        for index, cmd in enumerate(_args):
            if cmd in _full_args:
                recognized_cmd.append(index)

        recognized_cmd.append(len(_args))

        for i, cmd_index in enumerate(recognized_cmd):
            if (i + 1) > (len(recognized_cmd) - 1):
                break

            next_cmd_i = recognized_cmd[i + 1]
            cmd_params = _args[cmd_index + 1:next_cmd_i]
            cmd_name = _args[cmd_index]
            commands[cmd_name] = cmd_params

        for cmd, params in commands.items():
            self._parse_cmd(cmd, params)

        return self.namespace
