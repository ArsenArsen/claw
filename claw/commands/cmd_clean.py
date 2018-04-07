"""Cleans out the output directory of the current project"""

from claw.utils import clean_directory

def claw_exec(claw):
    # pylint: disable=missing-docstring
    clean_directory(claw.output_dir)
