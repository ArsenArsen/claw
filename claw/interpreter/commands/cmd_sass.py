"""
Takes the given input and output directories and compiles all SASS files in the input into the output directory

The command takes three parameters, namely target, directory, and glob:
    sass <source> <target> [style]
The source parameter is relative to the claw resource directory
The target parameter is where the compiled files will reside
The style argument is the style of the output.

It is assumed that the source is a directory unless it's found that it is a file

See: https://sass.github.io/libsass-python/sass.html#sass.compile

For example, to compile all sass files in scss and put them in static, as compacted css files:
    sass scss static compact
To take index.scss and compile it into static/index.css:
    sass index.scss static/index.css
"""

from os.path import join, isfile, exists, dirname
from os import makedirs
from claw.errors import ClawParserError, check_deps
check_deps("SASS compiler", "sass")
import sass

def claw_exec(claw, argv):
    # pylint: disable=missing-docstring
    if len(argv) != 3 and len(argv) != 4:
        raise ClawParserError("sass requires two or three arguments")

    src = join(claw.resource_dir, argv[1])
    dst = join(claw.output_dir, argv[2])
    style = "nested" if len(argv) == 3 else argv[3]
    if not exists(src):
        raise ClawParserError("sass source: no such file or directory")
    try:
        if isfile(src):
            makedirs(dirname(dst), exist_ok=True)
            with open(dst, 'w') as target:
                target.write(sass.compile(filename=src, output_style=style))
        else:
            sass.compile(dirname=(src, dst), output_style=style)
    except sass.CompileError as error:
        raise ClawParserError("There was an error while compiling sass files:", error)
