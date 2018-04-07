"""
Runs the Clawfile interpreter on the current directory.

The clawfile interpreter will go through the commands in the clawfile and execute them
"""

from claw.interpreter import clawfile
from claw.utils import trim_docstring

def claw_exec(claw):
    # pylint: disable=missing-docstring
    clawfile.interpret(claw)

def claw_help(claw, short=False):
    # pylint: disable=missing-docstring,unused-argument
    if short:
        return "Builds the claw project"

    return __doc__ + "\nInterpreter documentation:\n" + trim_docstring(clawfile.__doc__)
