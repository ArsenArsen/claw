"""
Simple command to print out the text from the input.

Can be used as an example command for building more complex ones
"""

def claw_exec(claw, argv):
    # pylint: disable=unused-argument,missing-docstring
    print(" ".join(argv[1:]))
