import sys


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

        self._actions = [
            'store_true',
            'store_false',
            'append',
            'default'
        ]

        self._default_namespace = Namespace()

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
            'action': action,
            'max_append': max_append
        }

        setattr(self._default_namespace, name, None)

    def add_flag(
        self,
        name: str,
        help: str,
        action: str = 'default',
        max_append: str = '*'
    ) -> None:
        """Create a new flag.

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

        name = name.replace('-', '')
        name = name.replace('--', '')
            
        setattr(self._default_namespace, name, None)

    def _print_help(self) -> None:
        print(f'usage: [command] [**optional] [flags]')
        if self.description:
            print(f'\n{self.description}')

        if self._commands:
            print('\ncommands:')
            for cmd, info in self._commands.items():
                print(f'    {cmd}: {info["help"]}')

        if self._flags:
            print('\nflags:')
            for flag, info in self._flags.items():
                print(f'    {flag}: {info["help"]}')

        sys.exit(0)

    def _print_version(self) -> None:
        if not self.project_name:
            print(f'Project: {self.version}')
        else:
            print(f'{self.project_name}: {self.version}')

        sys.exit(0)

    def _get_args(self) -> tuple:
        args = sys.argv[1:]
        arg_flags = [a for a in args if a.startswith('-')]

        return args, arg_flags

    def _get_flags(self, args: list, arg_flags: list) -> dict:
        for flag, info in self._flags.items():
            value = None

            if flag in arg_flags:
                action = info['action']
                flag_index = args.index(flag)
                max_append = info['max_append']

                if action == 'store_true':
                    value = True
                elif action == 'store_false':
                    value = False
                elif action == 'append':
                    if len(args[flag_index:]) == 1:
                        # invalid argument use
                        print(f'Invalid use of the flag "{flag}":')
                        print(f'    {flag}: {info["help"]}')
                        return self._default_namespace
                    else:
                        if max_append == '*':
                            arg_list = args[flag_index + 1:]
                        else:
                            max_append = int(max_append) + (flag_index + 1)

                            if len(args[flag_index + 1:]) > max_append:
                                print(f'Invalid use of the flag "{flag}":')
                                print(f'    {flag}: {info["help"]}')
                                return self._default_namespace

                            arg_list = args[flag_index + 1:max_append]

                        value = []

                        # filtrando flags da lista
                        # de argumentos
                        for a in arg_list:
                            if a.startswith('-'):
                                break
                            value.append(a)
                elif action == 'default':
                    if len(args[flag_index:]) < 2:
                        # invalid argument use
                        print(f'Invalid use of the flag "{flag}":')
                        print(f'    {flag}: {info["help"]}')
                        return self._default_namespace
                    else:
                        next_arg = flag_index + 1
                        value = args[next_arg]

            flag = flag.replace('-', '')
            flag = flag.replace('--', '')

            setattr(self.namespace, flag, value)

    def parse(self) -> Namespace:
        """Formats the command line arguments
        and returns them in an object.
        
        Checks the obtained arguments 
        and determines the value of them
        by returning a Namespace object.

        If the argument has the value of
        "None", it means that it was not
        called by the command line.
        """

        self.namespace = Namespace()
        args, args_flags = self._get_args()

        if len(args) == 0:
            self._print_help()
            return self._default_namespace

        command = args[0]

        if command not in self._commands and command not in self._flags:
            print(f'unrecognized command or flag: {command}')
            print('use --help to see commands')

            return self._default_namespace

        self._get_flags(args, args_flags)

        # check default flags
        if self.namespace.help:
            self._print_help()
        elif self.namespace.version:
            self._print_version()

        for cmd, info in self._commands.items():
            value = None

            if cmd == command:
                action = info['action']
                max_append = info['max_append']

                if action == 'store_true':
                    value = True
                elif action == 'store_false':
                    value = False
                elif action == 'append':
                    if len(args[0:]) == 1:
                        # invalid argument use
                        print(f'Invalid use of the argument "{cmd}":')
                        print(f'    {cmd}: {info["help"]}')
                        return self._default_namespace
                    else:
                        if max_append == '*':
                            arg_list = args[1:]
                        else:
                            max_append = int(max_append) + 1

                            if len(args[1:]) > max_append:
                                print(f'Invalid use of the argument "{cmd}":')
                                print(f'    {cmd}: {info["help"]}')
                                return None

                            arg_list = args[1:max_append]

                        value = []

                        # filtrando flags da lista
                        # de argumentos
                        for a in arg_list:
                            if a.startswith('-'):
                                break
                            value.append(a)
                elif action == 'default':
                    if len(args) < 2:
                        # invalid argument use
                        print(f'Invalid use of the argument "{cmd}":')
                        print(f'    {cmd}: {info["help"]}')
                        return self._default_namespace
                    else:
                        value = args[1]

            setattr(self.namespace, cmd, value)

        return self.namespace
