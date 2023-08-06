"""Sub-command of `hdev` to print out python version information."""
from hdev.command.sub_command import SubCommand


class PythonVersion(SubCommand):
    """Sub-command of `hdev` to print out python version information."""

    name = "python_version"
    help = "Dump the versions of Python in various formats"

    @classmethod
    def configure_parser(cls, parser):
        """Set up arguments needed for the sub-command."""

        parser.add_argument(
            "--style",
            required=True,
            help="The style to output the codes (`plain`, `json`, `tox`)",
        )

        parser.add_argument(
            "--first",
            default=False,
            action="store_const",
            const=True,
            help="Only return the first item found",
        )

        parser.add_argument(
            "--floating",
            default=False,
            action="store_const",
            const=True,
            help="Mark the last digit of marked versions with 'x'",
        )

        parser.add_argument(
            "--include-future",
            default=False,
            action="store_const",
            const=True,
            help="Include aspirational versions of Python",
        )

    def __call__(self, args):
        """Run the command.

        :param args: An ArgParser Namespace object
        """
        # pylint: disable=import-outside-toplevel
        from hdev.pyenv.version_file import PyenvVersionFile

        version_file = PyenvVersionFile(args.project.root_dir / ".python-version")

        string = version_file.versions(
            exclude=None if args.include_future else {"future"},
            floating=args.floating,
            first=args.first,
        ).as_string(style=args.style)

        # Don't emit a new line to make this easy to splat into the middle of
        # other scripts
        print(string, end="")
