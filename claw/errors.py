"""Helper errors for the Claw interpreter"""

from importlib import import_module

class ClawParserError(Exception):
    """Represents a parsing error"""
    pass

class ClawUnsupportedOpError(Exception):
    """Represents that an operation can't be used eg. because a dependency is missing"""
    pass

def check_deps(name, *args):
    """Check if all needed dependencies are there, and if not error"""
    for mod in args:
        try:
            import_module(mod)
        except:
            raise ClawUnsupportedOpError("Missing module {0}, {1} disabled".format(mod, name))
