"""Initializes a basic claw structure"""

import os
from claw.utils import trim_docstring

DEFAULT_FILES = {
    "src/index.md": """
        title: CLAW Default Page
        ---
        # CLAW
        **C**oo**L** **A**ssembler of **W**ebsites
    """,
    "resources/index.tml": """
        <head>
            <title>{{ title }}</title>
            <link rel="stylesheet" type="text/css" href="static/style.css">
        </head>
        <body>
            {{ body }}
        </body>
    """,
    "resources/style.css": """
        strong {
            color: #cdcdcd;
        }
    """,
    "Clawfile": """
        template index.md index.tml
        static *.css
    """
}

def claw_exec(claw):
    """Inserts a basic directory structure and Clawfile into the clawdir."""
    base = claw.dir
    if os.listdir(base) and not "--force" in claw.args:
        print("Current directory not empty, aborting")
        print("Use --force to bypass this check")
        return

    os.makedirs(os.path.join(base, "output"))
    os.makedirs(os.path.join(base, "src"))
    os.makedirs(os.path.join(base, "resources"))

    for filename, text in DEFAULT_FILES.items():
        with open(os.path.join(base, filename), "w") as target:
            target.write(trim_docstring(text))

def claw_help(claw, short=False):
    # pylint: disable=unused-argument
    """Provides an explanation of this command"""
    return "Makes a simple base claw project directory" if short else __doc__
