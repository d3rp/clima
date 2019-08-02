# Quick and dirty cli template

QDCT .. rolls off your tongue nice and easy.

To wrap your scripts as command line commands without
fussing about and maintaining argument parsing etc.
while still having the typical usage options available.

This idea is centred around a global configuration which
is populated with given arguments falling back optional on
defined defaults in the code and/or a configuration file.

## Preliminary installations

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
    
Note: consecutive steps presume the pipenv environment is being
used/activated

## Installing as command line program i.e. a command

    # Create pyproject.toml
    flit init 
    
    # Install dev version (omit --symlink for more permanent solution):
    flit install --symlink

## Usage

    # Test the damage
    cli -- -h
    cli -- -i
    
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
  * code completion should work in the IDE
  * configure should know to chain config file with params
  * ...
* maybe a logging setup (--dryrun)