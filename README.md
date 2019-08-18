# Quick and dirty cli templating

Create a semi-self-documenting command line interface boilerplate loading configuration
files and enabling env variable overloading in addition to command line arguments
by defining a simple schema of the configuration and a class with your "business logic".

In other words, use this to wrap your scripts as command line commands without
fussing about and maintaining argument parsing and duplicating comments for help or remembering
what the arguments were and did
while still having the typical use experience of a cli program (e.g. --help, subcommands, ...).
This implementation is focused on a premise that for a simple script you have a global configuration which
would be used through out the user code i.e. a context for the program. That configuration
is populated with given arguments falling back on
defaults in the code and some further complimentary options.

Should work for linux, macos and windows.

## Preliminary installations

**Note**:
If you prefer some other tooling, maybe try out [DepHell](https://github.com/dephell/dephell)
to transform this from pipenv to requirements.txt etc.. (or what ever floats you boat)

### pipenv

    # From the beginning...
    pip install -U pip pipenv
    
    # on some mac configurations, when pipenv isn't included in the path..
    sudo -H pip install -U pip pipenv
    
### pipenv environment

    pipenv install --ignore-pipfile
    
    # activate the environment alternative 1
    pipenv shell
    
    # activate the environment alternative 2
    pipenv run <command>
    
**Note**: consecutive steps presume the pipenv environment is being
used/activated

### Dependencies

* fire - python-fire from google does the cli wrapping


## Usage

See the example file in `tester/__main__.py`. Here's a run down of the individual
parts in it.

In your code define the schema as a NamedTuple:

    class Configuration(NamedTuple):
        a: str = 'A'  # a description
        x: int = 1  # x description

"Configuration" is an arbitrary name, no magic there. The inherited NamedTuple
simplifies the schema's templating to defining just the attributes (i.e. `a` and `x` in this
example). Those have a set way:

        # attribute: type = default value  # Description for the --help
        a: str = 'A'  # a description
       
`a` is the attribute which can be called in the code later with `c.a`. It has a type of 'str', default
value of 'A'. The comment after it is parsed for the command line so it's not redundant. All of these
parts will be parsed for the '--help' for the subcommands of the cli, which should be defined as follows:

    class Cli:
        def __init__(self, **cli_args):
            c(**cli_args, Configuration())

        def subcommand_foo(self):
            """This will be shown in --help for subcommand-foo"""
            print('foo')
            print(c.a)
            print(c.x)

        def subcommand_bar(self):
            """This will be shown in --help for subcommand-bar"""
            print('bar')

The `__init__` works as a funnel for the command line arguments baking them into the configuration `c` i.e.
the argument parsing is done here:

    def __init__(self, **cli_args):
        c(cli_args, Configuration())
    
The methods are parsed as subcommands for the cli and their respective doc strings will show in the 
subcommands' help print out. Note the usage of the parsed configuration `c`:

    print(c.a)
    print(c.x)
   
The implicit step to enable this magic is importing c from *clinfig*:

    from clinfig import c
            
Lsstly, the preparation for the command line --help:

    def main():
        prepare(Cli, Configuration())
        
In which the defined class for the command line business logic and the schema class (NamedTuple) is given as the first parameter for the
previously imported prepare function:

    from clinfig import prepare
    
Also, to enable autocompletion in IDEs, this hack is needed for the time being:

    c: Configuration = c

Put it in the "global space" just after defining the template. See the `tester/__main__.py` for a specific example.

When all is complete, the imported `c` variable should have all the bits and pieces for the configuration. It can be
used inside the Cli class as well as imported around the codebase thus encapsulating all the configurations into one
container with quick access with attributes `c.a`, `c.x`, ...

### Running the cli

    # Test the damage (presuming you did the flit step below)
    tester -- -h
    tester subcommand-foo -- -h
    tester subcommand-bar

Output should resemble this:

    $ tester subcommand-foo -- -h
    
    Type:        method
    String form: <bound method Cli.subcommand_foo of <__main__.Cli object at 0x000002995AD74BE0>>
    File:        C:\Users\foobar\code\py\clinfig\tester\__main__.py
    Line:        18
    Docstring:   This will be shown in --help for subcommand-foo
    Args:
        --a (str): a description (Default is 'A')
        --x (int): x description (Default is 1)

    Usage:       __main__.py subcommand-foo [--X ...]

## Configuration file and environment variables

The 'prepare' function chains multiple configuration steps in order of priority (lower number overrides higher number):

1. command line arguments
1. Environment variables
1. configuration file definitions
1. defaults in the schema/template/namedtuple class

The configuration file should be named `test.cfg` (see TODO) and have an ini type formatting with
a 'Default' section:

    # test.cfg
    [Default]
    x = 2

The keys are the same as what you define in the schema. You can define all, some or none of the attributes.
Same applies for the env variables.
    
    # linux example
    X=2 tester subcommand-foo
    
## Installing as command line program i.e. a command

    # Create pyproject.toml
    flit init 
    
    # Install dev version (omit --symlink for more permanent solution):
    flit install --symlink
   
## DONE:

* Show params in help / How to pass namedtuple's signature programmatically to the Cli functions?    
  * Need to do code generation i.e. write the signature into a separate python file and eval that?
  * Any fire-specific tricks to use for this? Cli(C) definition doesn't work..
    * Maybe overwriting the 'usage' portion or generating a docstring
  * Create a companion class which describes the namedtuple fields' functions
  * hardcoded defaults mechanism
* config parser
* decorator or some other wrapper for the cli-class to configure with given parameters without boilerplate
  
## TODO:

* generate man page in a reasonable fashion
* c++ template like behaviour in which you can define the named tuple with the cli class
  * code completion should work in the IDE (DONE: a hack around this..)
  * configure should know to chain config file with params
  * ...
* maybe a logging setup (--dryrun)
  * default debug logging wrapper that would log every function called
* tooling and installation helpers
  * flit is not working on windows at least..
  * dephell or alternative to allow dev with whatever setup
* Configuration file requires copying clinfig in the same directory with the user code
* parsing configuration and help/description require separate steps
  * would be nice to have a single point of access and import requirement
* base level help (<script> -- -h) doesn't printout the subcommands
* look into autocompletion options (iirc, fire might have sth out-of-the-box)