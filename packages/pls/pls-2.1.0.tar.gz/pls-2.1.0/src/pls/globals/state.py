from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Optional

from pls.arg_parser import parser
from pls.fs.git import get_git_root, get_git_statuses


class Singleton(type):
    """
    This metaclass can be inherited by any class to implement the singleton
    pattern. A singleton can only be instantiated one and all subsequent
    initialisations will always return the same instance.
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        # Calling a class as ``Klass()`` instantiates it.

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class State(argparse.Namespace, metaclass=Singleton):
    """
    Holds the global state of the application.
    """

    def __init__(self):
        super().__init__()

        self.home_dir: Optional[Path] = None

        self.git_root: Optional[Path] = None
        self.git_status_map: dict[Path, str] = {}

        self.uid: Optional[int] = None
        self.gids: set[int] = set()

    def __repr__(self) -> str:
        """
        Get the string representation of the ``State`` instance. This is also
        used by ``__str__`` automatically.

        :return: the string representation
        """

        return str(self.__dict__)

    def parse_args(self, argv: Optional[list[str]] = None):
        """
        Parse the given set of arguments into the state instance. This also
        invokes the setup functions that depend on the CLI args.

        :param argv: the list of CLI arguments to parse
        """

        parser.parse_args(argv, namespace=self)
        self.setup()

    def setup(self):
        """
        Invoke all ``setup_*`` functions associated with the state. This
        function is invoked by ``parse_args`` automatically.
        """

        for setup_fn in ["home", "git", "user_groups"]:
            getattr(self, f"setup_{setup_fn}")()

    def setup_home(self):
        """
        Set up the home directory of the current user.
        """

        try:
            self.home_dir = Path.home()
        except RuntimeError:
            # Home directory could not be determined.
            pass

    def setup_git(self):
        """
        Set up the Git root of the directory whose contents are being listed.
        """

        self.git_root = get_git_root(self.directory)
        if self.git_root is not None:
            assert self.git_root is not None
            self.git_status_map = get_git_statuses(self.git_root)

    def setup_user_groups(self):
        """
        Set up the username and groups of the current active user.
        """

        try:
            from grp import getgrall
            from pwd import getpwuid
        except ModuleNotFoundError:
            # This happens on non-POSIX systems like Windows.
            return

        self.uid = os.getuid()

        self.gids = set()
        try:
            user = getpwuid(self.uid)
        except KeyError:
            return
        self.gids.add(user.pw_gid)
        username = user.pw_name
        self.gids.update(
            group.gr_gid for group in getgrall() if username in group.gr_mem
        )


state: State
"""the global state of the application"""
