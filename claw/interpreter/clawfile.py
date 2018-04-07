"""
Goes over a clawfile and interprets it in a simple manner.

A clawfile consists of a simple command format:
    <command> <argument1> <arguments ...>
For example:
    template ~ posts/.* basic-post.tml

All argument and command splitting is done via the shlex module.
The syntax of shlex is similar to the UNIX shell, and for example:
    print "my special string" of characters
Would split into:
    ['print', 'my special string', 'of', 'characters']
Leading and trailing indentations are ignored.
Commands are defined via seperate modules in the interpreter.

Special case comands are:
    source_dir   - sets the source file directory of the project
    resource_dir - sets the resource directory of the project
    output_dir   - sets the output directory of the project
"""

from os.path import exists, join, dirname, basename
from shlex import split
from claw.utils import import_module
from claw.errors import ClawParserError

def interpret(claw, execute=True):
    """Loads and interprets a clawfile"""
    base = claw.dir
    lines = None
    commands = []

    with open(join(base, "Clawfile"), "r") as clawfile:
        lines = clawfile.readlines()

    for line in lines:
        argv = split(line)
        if len(argv) == 2:
            if argv[0] == "source_dir":
                claw.source_dir = argv[1]
                commands.append([])
                continue
            elif argv[0] == "resource_dir":
                claw.resource_dir = argv[1]
                commands.append([])
                continue
            elif argv[0] == "output_dir":
                claw.output_dir = argv[1]
                commands.append([])
                continue
        commands.append(argv)

    if execute:
        for line, argv in enumerate(commands):
            if not argv:
                continue
            command_file = join(dirname(__file__), "commands/cmd_" + basename(argv[0]) + ".py")
            if not exists(command_file):
                print("Error in parsing clawfile")
                print("Unknown command " + argv[0] + " on line " + str(line))
                exit(1)

            command = import_module(command_file)
            try:
                command.claw_exec(claw, argv)
            except ClawParserError as error:
                print("Parse error on " + line + ": ")
                print(error)
