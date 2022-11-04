from argparse import ArgumentParser


class PArgumentParser(ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        # Ignore comments
        if arg_line.startswith("#"):
            return []

        # strip whitespace at beginning and end of line
        arg_line = arg_line.strip()

        # When copying parameters from the command line to a file,
        # some users might copy the quotes they used on the command
        # line into the config file. We ignore these if the line
        # starts and ends with the same quote.
        if arg_line.startswith("'") and arg_line.endswith("'") or \
                arg_line.startswith('"') and arg_line.endswith('"'):
            arg_line = arg_line[1:-1]

        return [arg_line]


parser = PArgumentParser(
    prog="piaz",
)
parser.add_argument(
    "remote",
    metavar="[USERNAME[:PASSWORD]@]ADDR[:PORT]",
    help="""
    SSH hostname (and optional username and password) of remote %(prog)s server
    """
)
parser.add_argument(
    "-t",
    "--tool",
    help="""
    Config tool to apply on remote server. 
    """,
    default="v2ray",
    choices=["v2ray", "xui", "gost"],
)
parser.add_argument(
    "-c",
    "--command",
    help="""
    Command to override the default command of the tool's container.
    Example: -c "-L ss://chacha20:password@:8338"
    """,
    default="",
)

