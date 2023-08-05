#  TerminalPyth

Library that allows you to call terminal commands in python whithout discarding previous commands (unlike os.system() command does).

Install:

    $ pip install terminalpyth

Usage:

    import terminalpy

Create a terminalpy object. Pass True or False as argument if you want (or not) to have back the output.

    trm = terminalpy.Terminal(output=True)

Only one straight-forward method: type. Pass inside it the command you want to be executed.

    trm.type('pwd')

    # in this case, returns path to the current directory

It works with pretty much every terminal command. 

To use "sudo", if you are not in a terminal session itself, you must add the "-S" option, to read the password from your IDE (e.g. Pycharm).
