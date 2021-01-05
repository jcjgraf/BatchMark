# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from typing import Any

from vimiv import api
from vimiv.config import styles
from vimiv.utils import log, wrap_style_span

_logger = log.module_logger(__name__)


class BatchMark:
    class STATUS:
        invalid = 0
        idle = 1
        started = 2

    @api.objreg.register
    def __init__(self) -> None:
        self._reset()

    @api.commands.register()
    def batchmark_start(self) -> None:
        """Start Batch Mark Selection.

        Starts the selection at the currently selected image."""

        self.paths = api.pathlist()
        current_path = api.current_path()
        self.start_index = self.paths.index(current_path)

    @api.commands.register()
    def batchmark_end(self) -> None:
        """End Batch Mark Selection.

        Ends the selection at the currently selected image. If at least one image in the
        selection is unmarked, all images get markded. If all images are already marked,
        they all get unmarked."""

        if self.get_status() in (self.STATUS.idle, self.STATUS.invalid):
            self._reset()
            return

        current_path = api.current_path()
        self.end_index = self.paths.index(current_path)

        selected_paths = self.paths[self._get_lower_bound() : self._get_upper_bound()]

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

        self._reset()

    @api.commands.register()
    def batchmark_toggle(self) -> None:
        """Starts and ends batchmark selection.

        If not batchmark selection has been started or the last one is no longer valid
        (e.g. when the path was changed) a batch mark is started. Else the batch mark
        is ended and if at least one image in the selection is unmarked, all images get
        markded. If all images are already marked, they all get unmarked."""

        if self.get_status() in (self.STATUS.idle, self.STATUS.invalid):
            self.batchmark_start()

        elif self.get_status() == self.STATUS.started:
            self.batchmark_end()
            self._reset()

    def get_status(self):

        if self.paths is None or self.start_index is None:
            return self.STATUS.idle

        paths = api.pathlist()

        if paths != self.paths:
            return self.STATUS.invalid

        return self.STATUS.started

    @api.status.module("{batchmark}")
    def batchmark(self) -> str:
        status = self.get_status()

        if status == self.STATUS.started:
            color = styles.get("base0d")
            return wrap_style_span(f"color: {color}", "<b>+</b>")

        if status == self.STATUS.invalid:
            color = styles.get("base08")
            return wrap_style_span(f"color: {color}", "<b>+</b>")

        return ""

    def _reset(self):
        self.start_index = None
        self.end_index = None
        self.paths = None

    def _get_lower_bound(self):
        return min(self.start_index, self.end_index)

    def _get_upper_bound(self):
        return max(self.start_index, self.end_index) + 1


def init(*_args: Any, **_kwargs: Any) -> None:
    """Initialize BatchMark class."""
    BatchMark()
