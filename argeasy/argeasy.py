import sys


class Namespace(object):
    def __repr__(self):
        def get_attr():
            attr = []
            for i in self.__dir__():
                if not i.startswith('__'): attr.append(i)
            return attr

        attr = get_attr()
        repr = 'Namespace('

        for c, a in enumerate(attr):
            if c == len(attr) - 1:
                repr += f'{a}={self.__getattribute__(a)})'
            else:
                repr += f'{a}={self.__getattribute__(a)}, '

        return repr


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
        self._actions = [
            'store_true',
            'store_false',
            'default'
        ]

        self._default_namespace = Namespace()

        self.version = version
        self.description = description

    def add_argument(
        self,
        name: str,
        help: str,
        action: str = 'default'
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

        setattr(self._default_namespace, name, None)

    def _print_help(self) -> None:
        print(f'usage: [command] [**optional] [flags]')

        print('\ncommands:')
        for cmd, info in self._commands.items():
            print(f'    {cmd}: {info["help"]}')

    def get_args(self) -> Namespace:
        """Get args.
        
        Checks the obtained arguments 
        and determines the value of them
        by returning a Namespace object.

        If the argument has the value of
        "None", it means that it was not
        called by the command line.
        """

        namespace = Namespace()
        args = sys.argv[1:]

        if len(args) == 0:
            self._print_help()
            return self._default_namespace

        command = args[0]

        for cmd, info in self._commands.items():
            value = None

            if cmd == command:
                action = info['action']

                if action == 'store_true':
                    value = True
                elif action == 'store_false':
                    value = False
                elif action == 'default':
                    if len(args) < 2:
                        # invalid argument use
                        print(f'Invalid use of the command "{cmd}":')
                        print(f'    help: {info["help"]}')
                    
                    value = args[1]

            setattr(namespace, cmd, value)

        return namespace
