# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from typing import Any

from PyQt5.QtCore import QObject

from vimiv import api
from vimiv.config import styles
from vimiv.utils import log, wrap_style_span

_logger = log.module_logger(__name__)


class BatchMark(QObject):
    class STATUS:
        invalid = 0
        idle = 1
        started = 2

    @api.objreg.register
    def __init__(self) -> None:
        super().__init__()
        self._reset()
        self._action = self._reverse_action = None

        api.signals.escape_pressed.connect(self.batchmark_cancel)
        api.signals.event_handled.connect(self._batchmark_update)
        api.working_directory.handler.loaded.connect(self.batchmark_cancel)

    def _batchmark_update(self):
        """Update the marked paths according to the current position."""
        if self.get_status() != self.STATUS.started:
            return

        current_path = api.current_path()
        self.end_index = self.paths.index(current_path)

        selected_paths = set(
            self.paths[self._get_lower_bound() : self._get_upper_bound()]
        )

        no_longer_marked = self._triggered - selected_paths

        api.mark.mark(selected_paths, self._action)
        api.mark.mark(no_longer_marked, self._reverse_action)

        self._triggered = selected_paths

    @api.commands.register()
    def batchmark_start(self) -> None:
        """Start Batch Mark Selection at the current image.

        In case the current image is marked, we will unmark the batch."""

        self.paths = api.pathlist()
        self._prev_marked = set(api.mark.paths)
        current_path = api.current_path()
        if api.mark.is_marked(current_path):
            self._action = api.mark.Action.Unmark
            self._reverse_action = api.mark.Action.Mark
        else:
            self._action = api.mark.Action.Mark
            self._reverse_action = api.mark.Action.Unmark
        self.start_index = self.paths.index(current_path)

    @api.commands.register()
    def batchmark_accept(self) -> None:
        """Accept the changes of the current Batch Mark Selection."""
        self._reset()

    @api.commands.register()
    def batchmark_toggle(self) -> None:
        """Starts and ends Batch Mark Selection.

        In case we are currently in Batch Mark, accept the changes. Otherwise start
        Batch Mark."""

        if self.get_status() == self.STATUS.started:
            self.batchmark_accept()
            self._reset()
        else:
            self.batchmark_start()

    @api.commands.register()
    def batchmark_cancel(self) -> None:
        """Cancels the Batch Mark Selection if started."""
        if self.get_status() == self.STATUS.started:
            to_mark = self._triggered & self._prev_marked
            to_unmark = self._triggered - self._prev_marked
            api.mark.mark(to_mark, api.mark.Action.Mark)
            api.mark.mark(to_unmark, api.mark.Action.Unmark)
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
        self._prev_marked = set()
        self._triggered = set()

    def _get_lower_bound(self):
        return min(self.start_index, self.end_index)

    def _get_upper_bound(self):
        return max(self.start_index, self.end_index) + 1


def init(*_args: Any, **_kwargs: Any) -> None:
    """Initialize BatchMark class."""
    BatchMark()
