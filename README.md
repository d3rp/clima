# Quick and dirty cli templating

Create command line interface boilerplate enabling configuration
files and env variable overloading in addition to command line arguments
by defining a simple schema of the
configuration and a class with your "business logic".

In other words, use this to wrap your scripts as command line commands without
fussing about and maintaining argument parsing
while still having the typical usage options available.
This idea is centred around a premise of a global configuration which
would be used through out the user code. That configuration
is populated with given arguments falling back on
defaults in the code and an optional configuration file.

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

## Installing as command line program i.e. a command

    # Create pyproject.toml
    flit init 
    
    # Install dev version (omit --symlink for more permanent solution):
    flit install --symlink

## Usage

See the example file in tester/__main__.py. Here's a run down of the individual
parts in it.

In your code define the schema as a NamedTuple:

    class Configuration(NamedTuple):
        a: str = 'A'  # a description
        x: int = 1  # x description

"Configuration" is an arbitrary name, no magic there. The inherited NamedTuple does the
heavy lifting for it simplifying the schemas templating to defining just the attributes. Those
have a set way:

        a: str = 'A'  # a description
       
'a' is the attribute which can be called in the code later with 'c.a'. It has a type of 'str', default
value of 'A'. The comment after it is parsed for the command line so it's not redundant. All of these
parts will be parsed for the '--help' for the subcommands of the cli, which should be defined as follows:

    class Cli:
        def __init__(self, **ps):
            c(ps, Configuration())

        def subcommand_foo(self):
            """This will be shown in --help for subcommand-foo"""
            print('foo')
            print(repr(c))

        def subcommand_bar(self):
            """This will be shown in --help for subcommand-bar"""
            print('bar')

The methods are parsed as subcommands for the cli and their respective doc strings will show in the 
subcommands' help print out. Note the usage of the parsed configuration 'c':

    print(repr(c))
   
The implicit step to enable this magic is importing c from configz:

    from clinfig import c
            
          
The parameter parsing is done here:

    c(ps, Configuration())

Lsstly, the preparation for all of the above:


    def main():
        prepare(Cli, Configuration())
        
In which the defined class for the command line business logic is given as the first parameter for the
prepare function imported:

    from clinfig import prepare
    
The schema/template class is also given to it so it can do its magic mangling for the configuration.
When all is complete, the imported 'c' variable should have all the bits and pieces for the configuration.

    # Test the damage (presuming you did the flit step above)
    tester -- -h
    tester subcommand-foo -- -h
    tester subcommand-bar

Also, to enable autocompletion in IDEs, this hack is needed for the time being:

    c: Configuration = c

Put it in the "global space". See the tester/__main__.py for an example.

## Configuration file and environment variables

The 'prepare' function chains multiple configuration steps in order of priority:

1. command line arguments
1. Environment variables
1. configuration file definitions
1. defaults in the schema/template/namedtuple class

The configuration file should be named 'test.cfg' (see TODO) and have an ini type formatting with
a 'Default' section:

    # test.cfg
    [Default]
    x = 2

The keys are the same as what you define in the schema. You can define all, some or none of the attributes.
Same applies for the env variables.
    
    # linux example
    X=2 tester subcommand-foo
    
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