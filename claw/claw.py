"""
Claw is a website compiler built to be light, fast, and modern.

The idea behind claw is to just do it.
Claw takes an input folder, such as:
    /
    +-- /src
    |   +-- /index.md                   --> output/index.html
    |   +-- /posts
    |       +-- /posts/hello-world.md   --> output/posts/hello-world.html
    |       +-- /posts/how-are-ya.md    --> output/posts/how-are-ya.html
    +-- /Clawfile
    +-- /resources
        +-- index.tml
        +-- post.tml
        +-- style.css                   --> output/static/style.css

An example Clawfile would be:
    template index.md index.tml
    template posts/* post.tml
    static *.css

Compilation is as simple as `claw build'
You can take /output and slap it in your nginx server

Default project directory is the current working directory but it can be changed with -c
"""
import os
from os.path import exists, join, realpath, dirname, basename
import sys
from glob import glob
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader
from claw.utils import import_module
from claw.interpreter import clawfile
from claw.errors import ClawUnsupportedOpError

Claw = namedtuple("Claw", [
    "commands",
    "docstring",
    "args",
    "dir",
    "source_dir",
    "resource_dir",
    "output_dir",
    "jinja",
    "context"
])

# pylint: disable=too-many-arguments
def claw_construct(commands: str, args: list, directory: str, src=None, res=None, out=None) -> Claw:
    """Constructs a Claw named tuple"""
    resr = res or join(directory, "resources")
    jinja = Environment(loader=FileSystemLoader(resr, followlinks=True))
    filterpath = join(dirname(__file__), "filters")
    for filters in glob(join(filterpath, "*.py")):
        if basename(filters) == "__init__.py":
            continue
        module = import_module(filters)
        for new_filter in module.claw_filters():
            jinja.filters[new_filter.__name__] = new_filter
    return Claw(commands=commands, docstring=__doc__, args=args,
                dir=directory, source_dir=src or join(directory, "src"),
                resource_dir=resr,
                output_dir=out or join(directory, "output"),
                jinja=jinja, context={})

def main(args=sys.argv):
    """Entry point to claw"""
    clawdir = dirname(realpath(__file__))
    commands = glob(join(clawdir, "commands/cmd_*.py"))
    execmod = import_module(join(clawdir, "commands/cmd_help.py"))
    clawwd = os.getcwd()
    if len(args) > 1:
        if len(args) > 3 and args[1] == "-c":
            clawwd = realpath(args[2])
            if not exists(clawwd):
                print("Claw directory does not exist")
                exit(1)
            args = args[2:]
        for cmd in commands:
            if basename(cmd)[4:-3] == args[1]:
                try:
                    execmod = import_module(cmd)
                except ClawUnsupportedOpError as exception:
                    print("This command is currently unavailable: " + str(exception))
                break
        claw_ctx = claw_construct(commands=commands, args=args[1:], directory=clawwd)
        if exists(join(clawwd, "Clawfile")):
            clawfile.interpret(claw_ctx, False)
        execmod.claw_exec(claw_ctx)
    else:
        execmod.claw_exec(claw_construct(commands=commands, args=['help'], directory=clawwd))
