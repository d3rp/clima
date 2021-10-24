Usage
=====

.. _installation:

Installation
------------

To use clima, first install it using pip:

.. code-block:: console

   (.venv) $ pip install clima

Usage
-----

.. note::

    The section below is a piece-wise description of the `script_example.py <https://github.com/d3rp/clima/examples/script_example.py>`_ .

First, import the required components and define the `Schema` subclass:

.. code-block:: python

    from clima import c, Schema
    
    class Configuration(Schema):
        a: str = 'A'  # a description
        x: int = 1  # x description

It can be then run:

.. code-block:: console

    ./script.py foo -h
    
Which would print out the help page:

.. code-block:: console

     Usage:       script.py foo [ARGS]
     
     Description: Args:
         --a (str): a description (Default is 'A')
         --x (int): x description (Default is 1)    


Here, *Configuration* is an arbitrary name, no magic there. The inherited `Schema` class
defines the attributes (i.e. `a` and `x` in this example). 

Note the specific formatting of the `Schema` subclass:

        # attribute[: type] = default value  [# Description for the --help]
        a: str = 'A'  # a description
       
`a` is the attribute that can be called in the code later with `c.a`. In this example, it has a type of 'str' and a default
value of 'A'. The values in square brackets `[]` are
optional.

Clima parses the comment after the definition for the command-line help printout. In other words, Clima parses all of these parts to be displayed when the program is called using the argument '--help'. For example like this:

The example shown in this readme is at `examples/readme_example.py`.

Clima parses the methods as subcommands with their respective doc-strings, when the class is wrapped with the decorator `@c`, and will show these in the subcommand's help printout. 

The subcommands should be defined somewhat as follows:

.. code-block:: python

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

.. code-block:: python

    ...
        ...
        print(c.a)
        print(c.x)

As a decorator, `@c` defines the class to be parsed as the subcommands. As an object `c` it is used to access all the arguments.


Examples and platforms
----------------------

Tried and used on Linux, macOS, and windows. However, packaging and dependency management in python is sometimes hairy and
your mileage may vary.

More examples in the [examples directory](examples) with printouts of the defined subcommands and helps.


Testing the examples
********************

The [examples](examples) can be tried out by cloning the repo and running from repo directory root (on linux and the like):

.. code-block:: console

    git clone https://github.com/d3rp/clima.git 
    cd clima
    PYTHONPATH=$PWD python ./examples/readme_example.py foo -h

Running the examples that wrap a module:

.. code-block:: console

    PYTHONPATH=$PWD python ./examples/module_example/__main__.py -h
    PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-foo -h
    PYTHONPATH=$PWD python ./examples/module_example/__main__.py subcommand-bar
    ...


All of the example scripts can be run by installing [poetry](https://python-poetry.org) and running the `run_examples.bash`
script:

k. code-block:: console
    pip install poetry
    poetry run ./run_examples.bash
