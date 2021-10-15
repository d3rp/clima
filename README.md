<img src="https://raw.githubusercontent.com/d3rp/clima/master/clima.png" align="left" /> Create a command line interface with minimal setup.


[![PyPI](https://img.shields.io/pypi/v/clima)](https://pypi.org/project/clima/)
[![Python versions](https://img.shields.io/pypi/pyversions/clima)]()
[![PyPI license](https://img.shields.io/pypi/l/clima)]() 
[![Build status](https://app.travis-ci.com/d3rp/clima.svg?branch=master)](https://app.travis-ci.com/github/d3rp/clima)
[![Dependencies](https://badges.hiptest.com/librariesio/release/github/d3rp/clima)](https://libraries.io/pypi/clima) 

 # clima - command line interface with a schema 

##### Table of contents

  * [Briefly](#briefly)
     * [Features](#features)
     * [Cli definition](#cli-definition)
     * [Configuration object in a spiffy](#configuration-object-in-a-spiffy)
  * [Installing](#installing)
  * [Usage](#usage)
  * [Examples and platforms](#examples-and-platforms)
     * [Testing the examples](#testing-the-examples)
  * [Version printing](#version-printing)
  * [Autocompletion](#autocompletion)
     * [..in IDEs (wip)](#in-ides-wip)
     * [..in bash](#in-bash)
  * [Post init hook](#post-init-hook)
     * [Cli.post_init()](#clipost_init)
     * [Schema.post_init()](#schemapost_init)
  * [Configuration options](#configuration-options)
     * [Configuration file and environment variables](#configuration-file-and-environment-variables)
     * [Type casting with configuration definition](#type-casting-with-configuration-definition)
     * [Configuration file in the home directory](#configuration-file-in-the-home-directory)
     * [.env file](#env-file)
     * [Password unwrapping/decryption with pass](#password-unwrappingdecryption-with-pass)
  * [Additional features via Fire](#additional-features-via-fire)
  * [Truncated error printing](#truncated-error-printing)
  * [Ways to run the script for the uninitiated](#ways-to-run-the-script-for-the-uninitiated)
     * [Linking executable script to ~/.local/bin](#linking-executable-script-to-localbin)
     * [Packaging a module (pip ready)](#packaging-a-module-pip-ready)
  * [Building/Installing from source](#buildinginstalling-from-source)
  * [Long description and background](#long-description-and-background)
     * [Why another cli framework?](#why-another-cli-framework)
  * [Dependencies](#dependencies)
   
## Briefly

### Features

Clima handles loading and parsing command
line arguments with some off-the-shelf features, including:

- a global configuration object
    - a quick definition of defaults
    - defining defaults doubles as a description for help on the command line
    - type handling with annotations
- definitions with configuration files
- env variables
    - loading .env files
- secrets stored with [pass](https://www.passwordstore.org/)
- post_init hook

### Cli definition

Creating a command-line interface for your program:

1. Import all necessary parts from the package clima
1. (optional) Define configuration i.e., Schema
1. Define the command line commands i.e., CLI-class:

![example ascii](https://raw.githubusercontent.com/d3rp/clima/master/example.svg)

Example: to set up a configuration and a command-line interface ready to go.

    from clima import c
    
    @c
    class Cli:
        def say_hi(self):
            print('oh hi - whatever this is..')
            
            
The command line usage form could be as simple as:
  
     my_tool say_hi
  
### Configuration object in a spiffy

    from clima import c
    
    # Defining the settings (configuration object)
    class S(Schema):
        place = 'world'
        
    @c
    class Cli:
        def say_hi(self):
            # using configuration object 'c'
            print(f'oh hi - {c.place}')
            
            
Again, the command line usage form could be as simple as:
  
     my_tool say_hi
     my_tool say_hi --place 'other world'
 
See the `examples` folder and other sections for more examples. For example, the folder includes [something that resembles
the example above](examples/readme_example.py).
  

## Installing

    pip install --user clima

[toc](#table-of-contents)

   

## Usage

See the example file in [`examples/script_example.py`](examples/script_example.py). Here's a rundown of the individual
parts in such a script (adapted from another example at [module example](examples/module_example)).

First, import the required components:

    from clima import c, Schema
    
In your code, define the `Schema` subclass:

    class Configuration(Schema):
        a: str = 'A'  # a description
        x: int = 1  # x description

Here "Configuration" is an arbitrary name, no magic there. The inherited `Schema` class
defines the attributes (i.e. `a` and `x` in this example). 

Note the specific formatting of the `Schema` subclass:

        # attribute[: type] = default value  [# Description for the --help]
        a: str = 'A'  # a description
       
`a` is the attribute that can be called in the code later with `c.a`. In this example, it has a type of 'str' and a default
value of 'A'. The values in square brackets `[]` are
optional.

Clima parses the comment after the definition for the command-line help printout. In other words, Clima parses all of these parts to be displayed when the program is called using the argument '--help'. For example like this:

    ./script.py foo -h
    
Will now produce:

     Usage:       script.py foo [ARGS]
     
     Description: Args:
         --a (str): a description (Default is 'A')
         --x (int): x description (Default is 1)    

The example shown in this readme is at `examples/readme_example.py`.

Clima parses the methods as subcommands with their respective doc-strings, when the class is wrapped with the decorator `@c`, and will show these in the subcommand's help printout. 

The subcommands should be defined somewhat as follows:

    @c
    class Cli:
        def subcommand_foo(self):
            """This will be shown in --help for subcommand-foo"""
            print('foo')
            print(c.a)
            print(c.x)

        def subcommand_bar(self):
            """This will be shown in --help for subcommand-bar"""
            print('bar')

Note the double usage of the `c` - first as a decorator and later as the parsed configuration
inside the method:

    ...
        ...
        print(c.a)
        print(c.x)

As a decorator, `@c` defines the class to be parsed as the subcommands. As an object `c` it is used to access all the arguments.

[toc](#table-of-contents)

## Examples and platforms

Tried and used on Linux, macOS, and windows. However, packaging and dependency management in python is sometimes hairy and
your mileage may vary.

More examples in the [examples directory](examples) with printouts of the defined subcommands and helps.


### Testing the examples

The [examples](examples) can be tried out by cloning the repo and running from repo directory root (on linux and the like):

    git clone https://github.com/d3rp/clima.git 
    cd clima
    PYTHONPATH=$PWD python ./examples/readme_example.py foo -h

Running the examples that wrap a module:

    PYTHONPATH=$PWD python ./examples/module_example/__main__.py -h
    PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-foo -h
    PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-bar
    ...

The output should resemble this (fire v0.1.3 prints out Args, fire v0.2.1 does not (though it looks much nicer))

```
$ tester subcommand-foo -- -h

Type:        method
String form: <bound method Cli.subcommand_foo of <__main__.Cli object at 0x000002995AD74BE0>>
File:        C:\Users\foobar\code\py\clima\tester\__main__.py
Line:        18
Docstring:   This will be shown in --help for subcommand-foo
Args:
    --a (str): a description (Default is 'A')
    --x (int): x description (Default is 1)

Usage:       __main__.py subcommand-foo [--X ...]
```

All of the example scripts can be run by installing [poetry](https://python-poetry.org) and running the `run_examples.bash`
script:

    pip install --user poetry
    ./run_examples.bash
   
[toc](#table-of-contents)

## Version printing

Version printing works via the `version` subcommand and provides a version check functionality for (poetry) packaged scripts. Thus with bumping the version with poetry, Clima will handle parsing the current version of the packaged tool thus providing a subcommand such as:

    my_tool version
   
Clima parses the `version` attribute into the `c` object, so if you want control over it, you can overwrite it with the `post_init` or by handling the `c.version` otherwise.

## Autocompletion
 
### ..in IDEs (wip)

Also, to enable autocompletion in IDEs, this hack suffices:

    c: Configuration = c

Put it in the "global namespace" e.g. just after defining the template. See the [`examples/script_example.py`](examples/script_example.py) for a specific example.

When all is complete, the imported `c` variable should have all the bits and pieces for the configuration. It can be
used inside the Cli class as well as imported around the codebase thus encapsulating all the configurations into one
container with quick access to the attributes (`c.a`, `c.x`, ...).

### ..in bash

Running the script with `-- --completion` arguments should print an autocompletion declaration to include in a bash completions file:

    my_tool -- --completion
  
TBD: zsh etc. completions

## Post init hook

There are two ways to define a `post_init` hook depending on the `Schema` subclass or the `Cli` definition.

### Cli.post_init()

On some occasions, it is helpful to deduce specific defaults from the given arguments, 
for example, in a cross-platform build allowing
only minimal CLI arguments. For those cases, there is a `post_init` hook
When defining the `post_init()` in the `Cli` class, for example:

    @c
    class Cli:
    
        @staticmethod
        def post_init(s):
            if s.platform = 'win':
                self.bin_path = 'c:/Users/foo/bar'
            else:
                s.bin_path = '/Users/mac/sth'
            
        def subcommand(self):
            pass
               
The method will have access to the cli args, but can not introduce new variables to the schema.

This is arguably the more useful of the two variations of post_inits.

Note: The signature of the `post_init()` differs in these two options. For the time being, it is a `@staticmethod`

### Schema.post_init()

This alternative provides post_init-like features that are overrideable with the CLI arguments.

    class SoAdvanced(Schema):
    
        platform: str = 'win'  # a description
        bin_path: pathlib.Path = ''  # x description
        
        def post_init(self, *args):
            if self.platform = 'win':
                self.win_specific_field = 'All your files are locked by us..'
            
                
Note: This post_init() does not have access to the CLI arguments, but the `Schema`'s post_init can introduce new
attributes/properties/fields/arguments to the configuration, which the `Cli`-class post-init can't.
The `Schema`'s `post_init()` hook is run after the schema object's initialisation, but BEFORE the command-line object's initialisation. 


[toc](#table-of-contents)

## Configuration options

It is tedious to write a long list of parameters on the command line when most use cases follow a similar pattern. There are several options to choose from to facilitate the use of configurations.

The `c` decorator/configuration chains multiple configuration options together in order of priority (lower numbers refer to higher priority):

1. command line arguments
1. Environment variables
1. .env file
1. configuration file definitions
1. decrypted passwords from `~/.password-store` if gnugpg is installed
1. defaults in the subclass inheriting `Schema`

### Configuration file and environment variables


The configuration file should be named with either the postfix `.cfg` or `.conf`, for example `foo.conf`, and have an ini type formatting including
an explicit 'Clima' section:

    # foo.conf
    [Clima]
    x = 2

The keys are the same as in the schema class' declaration. Default values can be defined for all, some or none of the attributes. The same applies to the env variables.
    
    # linux example
    X=2 tester subcommand-foo
    
A configuration file defined this way can be located in the current working directory or - if your `Schema` defines a
 `cwd` field - there. Clima
will try to use the first configuration file it finds, so that might produce some caveats.

    class Conf(Schema):
        cwd = ''

    # Running ./script.py --cwd <folder> would automatically load the first *.conf file in <folder>

### Type casting with configuration definition
 
The `Schema` definition can have type annotations, which are used to cast the given arguments. For example

    class C(Schema):
        p: Path = ''  # Path to something

Results in `c.p`'s type cast as `Path`.   

### Configuration file in the home directory

You can also define the config file in the configuration class (one inheriting `Schema`) by defining the
magic field `CFG`.

For example, lets say the command `my_tool` (packaged etc) has a user configuration file at `~/.my_tool.conf`. This
can now be handled with just adding `CFG = Path.home() / '.my_tool.conf` to the Schema:

    from pathlib import Path
    
    class S(Schema):
        bing = 'bang'
        CFG = Path.home() / '.my_tool.conf'
    
Then, for example, the configuration file would be written as:

    #~/.my_tool.conf
    [Clima]
    bing = diudiu

Running the command `my_tool` would produce the value in the configuration file, though the arguments can still be overriden. 

    my_tool run 
    # diudiu
    
    my_tool run --bing bam
    # bam
    
### .env file
 
 This is handled by [dotenv](https://github.com/theskumar/python-dotenv). In short, all the defaults defined in the
 `Schema` subclass can be overridden either by:
 
    <field> = <value>

or

    export <field> = <value>
    
### Password unwrapping/decryption with pass
 
 Note: Currently this works only for gpg-keys without password. It's not ideal, but it's better than plain text `.env`
 files ;)
 
 Note 2: Leading and trailing whitespace (including `\n` linefeeds) are stripped, when decrypted.
 
 [pass](https://passwordstore.org) can be used to store passwords as gpg encrypted files under the home directory. Clima
 uses the default path of ~/.password-store and the files found within. It will then match the arguments with the 
 stored passwords, for example:
 
     tree -A ~/.password-store                                                                                                                                                                                                                                                                             ✔ | 41s | anaconda3 
     /Users/me/.password-store
     ├── work
     │   ├── ci
     │   │   ├── sign_id.gpg
     │   │   ├── sign_pw.gpg
     ... ... ...
 
 And an according `Schema` definition:
 
     class Conf(Schema):
         sign_id: str = ''  # signing id for the CI
         sign_pw: str = ''  # signing pw for the CI
 
 Would accept those arguments as cli arguments, or if omitted, would traverse through the `.password-store` and decrypt the
 found `sign_id.gpg` and `sign_pw.gpg` placing the values found in the configuration object `c`.
     
 [toc](#table-of-contents)      
 
## Additional features via Fire

See the [Python Fire's Flags](https://github.com/google/python-fire/blob/master/docs/using-cli.md#python-fires-flags)
documentation for nice additional features such as:

    # e.g. tester.py is our cli program
    tester.py subcommand-foo -- --trace
    tester.py -- --interactive
    tester.py -- --completion
    

## Truncated error printing

This feature rose as an opinionated option, and I admit, it should be something the user could bypass. Even though I have used python for a few years professionally, I am still not satisfied with its error printing. When raising exceptions, Clima truncates the error lists and tries to provide a more readable version of the "first" point of failure. The whole traceback is written into a logfile `exception_traceback.log` to examine if the truncated output provides insufficient information.

Note: When running the examples, the `exception_traceback.log` file will be written inside the `examples` directory


## Ways to run the script for the uninitiated

Here are some suggestions on how to wrap scripts using Clima.

### Linking executable script to ~/.local/bin

Let's say those lines were written in a file named `script.py`. Command line usage in a terminal would then be e.g.:

    python script.py foo
    python script.py foo --a 42

Adding this line in `script.py`

    #!/usr/bin/env python
    
and changing its execution permissions (mac, linux):

    chmod +x script.py
   
Allows for a shorter means of execution:

    ./script.py foo

Now this could be linked as an adhoc command for example:

    ln -s $PWD/script.py ~/.local/bin/my_command

### Packaging a module (pip ready)

For a pip-installable package, one could [package this as a runnable command](https://github.com/d3rp/my_tool) -
publish in the public or one's private pypi etc - and then approach the convenience factor shown at first.

    pip install my_tool
    my_command foo -h

To publish with poetry is quite straight forward. First create an account in pypi.org and then:

    cd <project directory>
    poetry build
    poetry publish
 
You can use `version` to bump up versions:
    
    poetry version patch

## Building/Installing from source

This repo is based on [poetry](https://poetry.eustace.io).

    git clone https://github.com/d3rp/clima.git 
    cd clima
    poetry install --no-dev

The `--no-dev` is for to install the running environment without development tooling.

[toc](#table-of-contents)

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

* fire - [python-fire](https://github.com/google/python-fire) from google does the cli wrapping / forked and included 
into the repo - I wanted to have the version 0.1.x formatting and help output with few hacks of my own


[toc](#table-of-contents)
