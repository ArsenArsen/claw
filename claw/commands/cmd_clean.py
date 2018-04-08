"""Cleans out the output directory of the current project"""

from claw.utils import clean_directory

def claw_exec(claw):
    # pylint: disable=missing-docstring
    clean_directory(claw.output_dir)

def claw_help(claw, short=False):
    # pylint: disable=missing-docstring,unused-argument
    # This is so simple that detailed help is is the same as the summary
    return __doc__
