# ArgEasy

Argeasy is a *simple and intuitive* command line argument parser for any user, making it easy to build **CLI** applications. With it, you can:

- Set arguments;
- Set flags;
- Set application name, description and version;
- Define the action to be taken when an argument or flag is called.

In addition to having well-structured **user help messages** with all the necessary information. To install this library, use `pip`:

```
pip install argeasy
```

## Example of use

Here is a simple usage example:

```python
import argeasy

parser = argeasy.ArgEasy()

parser.add_argument('foo', 'print foo', action='store_true')
parser.add_flag('--bar', 'print a text')

args = parser.parse()

if args.foo:
    print('foo')
```

In this code, we add an argument called `foo` and set the action (in the `action` argument) to be taken as `store_true`, that is, when this argument is called, its value will be `True`. Otherwise, the value will be `None`. Flags named with separate words like `--add-email` will be changed and can be obtained with `args.add_email`.

You can also define information about your application, such as version, description and project name. Do this in the instance of the `ArgEasy` class:

```python
argeasy.ArgEasy(
    name='My App',
    description='Description of my App',
    version='1.0.0'
)
```

### Actions

Action is the action that `argeasy` should take when it perceives an argument. See available actions:

- `default`: get the next argument as a value;
- `store_true`: if the argument is detected, its value will be `True`;
- `store_false`: if the argument is detected, its value will be `False`;
- `append`: if the argument is detected, it will get all other arguments present in front of it.

## License

```
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
```

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
