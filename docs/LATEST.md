# ArgEasy (June 08 2023)

Latest version (3.1.0) documentation of ArgEasy project.

## Getting started

First, let's install the latest version of the project using the PIP package manager with the command below:

```bash
pip install argeasy
```

If you prefer, you can install the project directly from the official GitHub repository using Git:

```bash
git clone https://github.com/jaedsonpys/argeasy
cd argeasy/
python3 setup.py install
```

After installation, you are ready to use all the features of the latest version of ArgEasy!

### How it works

To start with, let's use the `ArgEasy` class which contains the necessary methods for creating our command line interface. The instance of this class can receive the name of the application, description and version of your program, this information will be shown when the flags `--help` or `--version` are used. 

Let's get to know the available methods of the `ArgEasy` class:

- The `ArgEasy.add_argument` method adds a new command 
- to the application, like "install", for example.
- The `ArgEasy.add_flag` method adds a new flag to the application, like "--help".
- Finally, we have the `ArgEasy.parse` method, which formats the command typed on the command line and arranges the data using a class

The `add_argument` and `add_flag` methods have the same parameters, they obligatorily require a **name and a description**, the other two parameters are optional, they are where we define *how the command parameters will be obtained*. These parameters are:

- `action`: Defines how the data should be obtained:
    - defaut: Gets the next piece of data as a parameter. Example: `install argeasy`. In the example "install" is the command and "argeasy" is the obtained parameter.
    - store_true: Stores a boolean value if the command is present. Used when you don't want to receive data, but just want to know if it is present or not. Example: `argeasy --help`.
    - append: Stores a list of parameters. Used when we want to get a lot of data with just one command. Example: `install argeasy cookiedb box-vcs`. In this example, "install" is the command that takes 3 parameters that will be returned as a list (`['argeasy', 'cookiedb', 'box-vcs']`) when formatted.
- `max_append`: Sets the maximum number of parameters that can be added to a command (default is "*", ie any number). This parameter is only useful **when you use the "append"** action.