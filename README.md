# Quick and dirty cli template

QDCT .. rolls off your tongue nice and easy.

    # Create pyproject.toml
    flit init 
    
    # Install dev version (omit --symlinks for more permanent solution):
    flit install --symlink

    # Test the damage
    pipenv shell
    cli -- -h
    cli -- -i
    
TODO:

* How to pass namedtuple's signature programmatically to the Cli functions?    
  * Need to do code generation i.e. write the signature into a separate python file and eval that?
  * Any fire-specific tricks to use for this? Cli(C) definition doesn't work..
    * Maybe overwriting the 'usage' portion or generating a docstring
  * Create a companion class which describes the namedtuple fields' functions
* generate man page in a reasonable fashion