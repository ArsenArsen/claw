"""
Simple help display command.

Side note, you can use this as an example interface for claw commands.
"""

import os
from claw.utils import import_module, trim_docstring, indent_block

def claw_exec(claw):
    """
    Executes the claw help command

    It will simply print out the claw docstring,
    then commands woth their short help strings, or
    if a command argument is supplied, it's long help
    """
    if len(claw.args) != 2:
        print(claw.docstring)
        help_dict = {}
        longest_name = 1
        for cmd in claw.commands:
            cmod = import_module(cmd)
            name = os.path.basename(cmd)[4:-3]
            help_dict[name] = cmod.claw_help(claw, True)
            longest_name = max(len(name), longest_name)
        print("Commands:")
        for cmd, help_str in help_dict.items():
            print("\t" + cmd
                  + ((1 + longest_name - len(cmd)) * " ") + f"-> {help_str}")
    else:
        execmod = None
        for cmd in claw.commands:
            if os.path.basename(cmd)[4:-3] == claw.args[1]:
                execmod = import_module(cmd)
                break
        if execmod:
            print("Help for " + claw.args[1] + ":")
            print(indent_block(trim_docstring(execmod.claw_help(claw, False)),
                               indent=" ", count=4))

def claw_help(claw, short=False) -> str:
    # pylint: disable=W0612,W0613
    """Supplies string used by the help command"""
    return "This page" if short else __doc__
