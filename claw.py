#!/usr/bin/env python3
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
from jinja2 import Environment
from claw.utils import import_module
from claw.interpreter import clawfile

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

def claw_construct(commands: str, docstring: str, args: list, dir: str, src=None, res=None, out=None) -> Claw:
    """Constructs a Claw named tuple"""
    jinja = Environment()
    filterpath = join(dirname(__file__), "claw/filters")
    for filters in glob(join(filterpath, "*.py")):
        if basename(filters) == "__init__.py":
            continue
        module = import_module(filters)
        for new_filter in module.claw_filters():
            jinja.filters[new_filter.__name__] = new_filter
    return Claw(commands=commands, docstring=docstring, args=args,
                dir=dir, source_dir=src or join(dir, "src"),
                resource_dir=res or join(dir, "resources"),
                output_dir=out or join(dir, "output"),
                jinja=jinja, context={})

if __name__ == "__main__":
    args = sys.argv
    clawdir = dirname(realpath(__file__))
    commands = glob(join(clawdir, "claw/commands/cmd_*.py"))
    execmod = import_module(join(clawdir, "claw/commands/cmd_help.py"))
    clawwd = os.getcwd()
    if len(args) > 1:
        if len(args) > 3 and args[1] == "-c":
            clawwd = realpath(args[2])
            print(clawwd)
            if not exists(clawwd):
                print("Claw directory does not exist")
                exit(1)
            args = args[2:]
        for cmd in commands:
            if basename(cmd)[4:-3] == args[1]:
                execmod = import_module(cmd)
                break

        cf = claw_construct(commands=commands, args=args[1:], docstring=__doc__, dir=clawwd)
        if exists(join(clawwd, "Clawfile")):
            clawfile.interpret(cf, False)
        execmod.claw_exec(cf)
    else:
        execmod.claw_exec(claw_construct(commands=commands, args=['help'], docstring=__doc__, dir=clawwd))
