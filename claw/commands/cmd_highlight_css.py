"""Provides the required CSS files for syntax highlighting, as is defaulted for Pygments"""

from os import makedirs
from os.path import dirname, join
from claw.errors import ClawParserError, check_deps
check_deps("Code highlighting", "pygments")
from pygments.formatters.html import HtmlFormatter

def claw_exec(claw):
    # pylint: disable=missing-docstring
    print(HtmlFormatter().get_style_defs(".highlight"))

def claw_help(claw, short=False) -> str:
    # pylint: disable=W0612,W0613,missing-docstring
    return "Provides syntax highlighting related css files" if short else __doc__
