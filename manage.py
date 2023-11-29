import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from collections.abc import Sequence
from contextlib import suppress
from pathlib import Path

import pytest
from rich import print
from rich_argparse import RichHelpFormatter

PROJECT_ROOT: Path = Path(__file__).resolve().parent

SOURCE_RELATIVE_PATH: Path = Path("./docs/source/")
SOURCE_DIR: Path = PROJECT_ROOT.joinpath(SOURCE_RELATIVE_PATH)

BUILD_RELATIVE_PATH: Path = Path("./docs/build/")
BUILD_DIR: Path = PROJECT_ROOT.joinpath(BUILD_RELATIVE_PATH)

AVAILABLE_BUILDERS: tuple[str, ...] = (
    "html",
    "dirhtml",
    "singlehtml",
    "htmlhelp",
    "qthelp",
    "devhelp",
    "epub",
    "applehelp",
    "latex",
    "man",
    "texinfo",
    "text",
    "gettext",
    "doctest",
    "linkcheck",
    "xml",
    "pseudoxml",
)
BUILD_HELP: str = (
    "Builder to pass to `sphinx-build` (Defaults to html). The available builders are: "
    f"{', '.join(f'[green]{b}[/]' for b in AVAILABLE_BUILDERS)}. "
    "See https://www.sphinx-doc.org/en/master/usage/builders/index.html for more "
    "information about sphinx builders."
)


def clean_docs() -> int:
    print("Removing", BUILD_DIR)
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    return 0


def build_docs(builder: str) -> int:
    output_dir = BUILD_DIR.joinpath(builder)
    with suppress(KeyboardInterrupt):
        res = subprocess.run(["sphinx-build", SOURCE_DIR, output_dir, "-b", builder])
        return res.returncode


# TODO: Change `delay` to float (See below)
def serve_docs(builder: str, *, open_browser: bool, delay: int) -> int:
    output_dir = BUILD_DIR.joinpath(builder)
    auto_build_cmd = [
        "sphinx-autobuild",
        SOURCE_DIR,
        output_dir,
        "--watch",
        "src",
        "-b",
        builder,
    ]
    if open_browser:
        auto_build_cmd.append("--open-browser")
        auto_build_cmd.append("--delay")
        auto_build_cmd.append(str(delay))
    with suppress(KeyboardInterrupt):
        res = subprocess.run(auto_build_cmd)
        return res.returncode


def run_tests() -> int:
    return pytest.main([])


def setup(*, dry_run: bool) -> int:
    if dry_run:
        print("Steps to setup the project:")
        print("  1. Install `pre-commit` hooks: `pre-commit install`")
        return 0
    with suppress(KeyboardInterrupt):
        print("Installing `pre-commit` hooks", end="\n\n")
        res = subprocess.run(["pre-commit", "install"])
        if res.returncode == 0:
            print("[green]Done![/]")
        else:
            print(
                "[red]Couldn't install `pre-commit` hooks. Aborting setup.[/]",
                file=sys.stderr,
            )
            return res.returncode
        return 0


def get_parser() -> ArgumentParser:
    RichHelpFormatter.highlights.append(r"\b(?P<metavar>BUILDER)\b")
    parser = ArgumentParser(
        description="Utility scripts and commands to manage the project's development.",
        formatter_class=RichHelpFormatter,
    )
    subparsers = parser.add_subparsers(required=True, title="commands")

    # docs group
    docs_parser = subparsers.add_parser(
        "docs",
        description="Commands to manage the documentation of the project.",
        help="Documentation management",
        formatter_class=parser.formatter_class,
    )
    docs_subparsers = docs_parser.add_subparsers(required=True, title="commands")
    docs_clean_parser = docs_subparsers.add_parser(
        "clean",
        description=(
            "Delete the generated documentation directory and all of its contents."
        ),
        help="Remove built documentation",
        formatter_class=docs_parser.formatter_class,
    )
    docs_clean_parser.set_defaults(command=clean_docs)

    docs_build_parser = docs_subparsers.add_parser(
        "build",
        description=(
            "Build the documentation using `sphinx-build`. The output will be placed "
            f"in {BUILD_RELATIVE_PATH.joinpath('BUILDER')} relative to the project "
            "root. BUILDER is the parameter passed to --builder (for example: html)."
        ),
        help="Build documentation",
        formatter_class=docs_parser.formatter_class,
    )
    docs_build_parser.add_argument(
        "-b",
        "--builder",
        default="html",
        choices=AVAILABLE_BUILDERS,
        metavar="BUILDER",
        help=BUILD_HELP,
    )
    docs_build_parser.set_defaults(command=build_docs)

    docs_serve_parser = docs_subparsers.add_parser(
        "serve",
        description=(
            "Spawn a server that serves the documentation and reloads automatically "
            "when files are changed (live reloading) using `sphinx-autobuild`. Like "
            "the [blue]build[/] command, the output will be placed in "
            f"{BUILD_RELATIVE_PATH.joinpath('BUILDER')} relative to the project root "
            "where BUILDER is the value of the parameter --builder."
        ),
        help="Serve documentation with live reloading",
        formatter_class=docs_parser.formatter_class,
    )
    docs_serve_parser.add_argument(
        "-b",
        "--builder",
        default="html",
        choices=AVAILABLE_BUILDERS,
        metavar="BUILDER",
        help=BUILD_HELP,
    )
    docs_serve_parser.add_argument(
        "-o",
        "--open-browser",
        action="store_true",
        help="Open the browser after building the documentation",
    )
    # TODO: Change parameter type to float once `sphinx-autobuild` supports floats
    docs_serve_parser.add_argument(
        "-d",
        "--delay",
        type=int,
        default=0,
        help=(
            "How long to wait before opening the browser in seconds "
            "(Defaults to 0, that is, no delay). Note that this parameter has no "
            "effect without the --open-browser parameter."
        ),
    )
    docs_serve_parser.set_defaults(command=serve_docs)

    # test command
    test_parser = subparsers.add_parser(
        "test",
        description="Run tests using `pytest`.",
        help="Run tests",
        formatter_class=parser.formatter_class,
    )
    test_parser.set_defaults(command=run_tests)

    # setup command
    setup_parser = subparsers.add_parser(
        "setup",
        description=(
            "Perform initial setup of the project. This should be the first thing to "
            "do after cloning the repository."
        ),
        help="Initial setup of the project when start developing",
        formatter_class=parser.formatter_class,
    )
    setup_parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Print what running the setup command would do without doing it",
    )
    setup_parser.set_defaults(command=setup)

    return parser


def main(args: Sequence[str] | None = None) -> None:
    parser = get_parser()
    args = vars(parser.parse_args(args))
    os.chdir(PROJECT_ROOT)
    command = args.pop("command")
    sys.exit(command(**args))


if __name__ == "__main__":
    main()
