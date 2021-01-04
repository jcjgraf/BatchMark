# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from typing import Any

from vimiv import api
from vimiv.gui.mainwindow import MainWindow
from vimiv.utils import log

_logger = log.module_logger(__name__)

library = MainWindow.instance._library


class BatchMark:
    @api.objreg.register
    def __init__(self) -> None:
        self.start_index = None
        self.end_index = None
        self.paths = None

    @api.commands.register()
    def batchmark_start(self) -> None:
        """Start Batch Mark Selection.

        Starts the selection at the currently selected image."""

        self.paths = api.pathlist()
        current_path = api.current_path()
        self.start_index = self.paths.index(current_path)

    @api.commands.register()
    def batchmakr_end(self) -> None:
        """End Batch Mark Selection.

        Ends the selection at the currently selected image. If at least one image in the
        selection is unmarked, all images get markded. If all images are already marked,
        they all get unmarked."""

        end_paths = library.model().paths

        if self.paths is None or self.paths != end_paths:
            self.paths = None
            return

        current_path = api.current_path()
        self.end_index = self.paths.index(current_path)

        self.batchmarktoggle()

    @api.commands.register()
    def batchmark_toggle(self) -> None:
        """Toggles the currently selected region.

        If at least one image in the selection is unmarked, all images get markded. If
        all images are already marked, they all get unmarked."""

        if self.paths is None or self.start_index is None or self.end_index is None:
            self.paths = None
            return

        selected_paths = self.paths[self._getLowerBound() : self._getUpperBound()]

        unmarked = False  # If true, at least one image in selected_paths is not marked

        # If all images are maked, unmark them, else mark them
        for path in selected_paths:
            try:
                api.mark._unmark(path)
            except ValueError:
                unmarked = True
                continue

        # By now all images are unmarked. Mark all agin in case ther was at least
        # one unmarked image in the beginning
        if unmarked:
            for path in selected_paths:
                api.mark._mark(path)

    def _getLowerBound(self):
        return min(self.start_index, self.end_index)

    def _getUpperBound(self):
        return max(self.start_index, self.end_index) + 1


def init(*_args: Any, **_kwargs: Any) -> None:
    """Initialize BatchMark class."""
    BatchMark()
