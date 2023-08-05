"""Pylint extension with performance anti-patterns"""
from typing import TYPE_CHECKING

from perflint.for_loop_checker import ForLoopChecker, LoopInvariantChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter

__version__ = "0.4.0"


def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """

    linter.register_checker(ForLoopChecker(linter))
    linter.register_checker(LoopInvariantChecker(linter))
