<img src="https://raw.githubusercontent.com/d3rp/clima/master/clima.png" align="left" /> Create a command line interface with minimal setup.

[![PyPI](https://img.shields.io/pypi/v/clima)](https://pypi.org/project/clima/)
[![Python versions](https://img.shields.io/pypi/pyversions/clima)]()
[![PyPI license](https://img.shields.io/pypi/l/clima)]() 
[![Build status](https://app.travis-ci.com/d3rp/clima.svg?branch=master)](https://app.travis-ci.com/github/d3rp/clima)

# clima - command line interface with minimal boilerplate

Clima helps to parse and encapsulate command-line arguments into a container that you declare as a simple schema class.

## Features

Clima handles loading and parsing command
line arguments with some off-the-shelf features, including:

- a global configuration object, that is parsed for
    - defaults
    - description for arguments
    - type casting
- handles parsing argument values additionally from
    - conf and .env files
    - env variables
    - gpg encrypted files
- more features described in the docs

## Cli definition

Creating a command-line interface for your program:

1. Import "c" decorator from clima
1. (optional) Define configuration using clima.Schema
1. Define the command line commands i.e., CLI-class:

![example ascii](https://raw.githubusercontent.com/d3rp/clima/master/example.svg)

Example: to set up a configuration and a command-line interface ready to go.

    from clima import c, Schema
    
    # Defining the settings (configuration object)
    class S(Schema):
        place = 'world'
        
    @c
    class Cli:
        def say_hi(self):
            # using configuration object 'c'
            print(f'oh hi - {c.place}')
            
            
Then, the command line usage would be:
  
     my_tool say_hi
     my_tool say_hi --place 'other world'
 
This script is included as [something that resembles the example above](examples/readme_example.py).
  
See [the read-the-docs documentation](https://python-clima.readthedocs.io/en/latest/) for
full reference.

## Installation

    pip install --user clima

## Examples and platforms

Tried and used on Linux, macOS, and windows. However, packaging and dependency management in python is sometimes hairy and your mileage may vary.

More examples in the [examples directory](examples) with printouts of the defined subcommands and helps.

### Testing the examples

All of the example scripts can be run by installing [poetry](https://python-poetry.org) and running the `run_examples.bash` script:

    pip install --user poetry
    poetry run ./run_examples.bash
   
## Other features

Clima intends to get to reasonable defaults fast. Thus it provides other often used
convenience featuers.

- Version printing
- Autocompletion for terminals (wip)
- Autocompletion for IDEs (via a hack)
- Post init hook (after initial parsing, define preliminary actions according to arguments)
- Password unwrapping/decryption with gnugpg (if installed)
- Improved, concise traceback messages (with traditional logs saved to file)

## Configuration options

It is tedious to write a long list of parameters on the command line when most use cases follow a similar pattern. There are several options to choose from to facilitate the use of configurations.

The `c` decorator/configuration chains multiple configuration options together in order of priority (lower numbers refer to higher priority):

1. command line arguments
1. Environment variables
1. .env file
1. configuration file definitions
1. decrypted passwords from `~/.password-store` if gnugpg is installed
1. defaults in the subclass inheriting `Schema`

## Building/Installing from source

This repo is based on [poetry](https://poetry.eustace.io).

    git clone https://github.com/d3rp/clima.git 
    cd clima
    poetry install --no-dev

The `--no-dev` is for to install the running environment without development tooling.

## Long description and background

You can write your subcommands as a class encapsulating the "business logic". Clima encapsulates the command-line arguments as a container, mapping its attributes as you declare them in a simple schema class.

In other words, you can use this to wrap your scripts as command line commands without resorting to Bash or maintaining argument parsing in python. It removes the need to duplicate comments to have `--help` remember what the arguments were and what they did. Sprinkling some decorator magic offers a typical user experience of a CLI program (e.g. argument parsing and validation, --help, subcommands, ...).

The premise behind Clima is that a simple script usually uses a script wide global configuration throughout the user code, or in other words, a context for the program accessed in different parts of the code. Clima populates that context, or configuration, with given arguments falling back on defaults in the code and some further complimentary options. Those are then made accessible via a global `c` variable, or container, that can be tossed around the code base with minimal additional effort. 
With almost no additional effort, Clima can provide autocompletion in IDEs (as attributes). This feature helps when extending your code as the autocomplete kicks in after typing `c.` offering those fields in your "schema" as attributes.
 
### Why another cli framework?

Clima does not try to cater as a feature-complete CLI framework like the ones listed below. It is a package to help with boilerplate to get quick but reusable tools for your workflow.

Other options for a full-featured CLI experience:

* [docopt](https://docopt.org)
* [fire](https://github.com/google/python-fire)
* [cleo](https://github.com/sdispater/cleo)
* [click](https://click.palletsprojects.com)
* [typer](https://github.com/tiangolo/typer)


## Dependencies

* [dotenv](https://github.com/theskumar/python-dotenv)
* gnugpg - this is pass through though. If it's not installed, the feature is not in use.

