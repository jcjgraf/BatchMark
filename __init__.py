# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from typing import Any

from PyQt5.QtCore import QObject

from vimiv import api
from vimiv.config import styles
from vimiv.utils import log, wrap_style_span

_logger = log.module_logger(__name__)


class BatchMark(QObject):
    @api.objreg.register
    def __init__(self) -> None:
        super().__init__()
        self._reset()
        self._action = self._reverse_action = None

        api.signals.escape_pressed.connect(self.batchmark_cancel)
        api.signals.event_handled.connect(self._batchmark_update)
        api.working_directory.handler.loaded.connect(self.batchmark_cancel)

        _logger.debug("Initialized BatchMark")

    def _batchmark_update(self):
        """Update the marked paths according to the current position."""
        if not self._is_started():
            _logger.info("Need to start selection first")
            return

        current_path = api.current_path()
        self.end_index = self.paths.index(current_path)

        selected_paths = set(
            self.paths[
                min(self.start_index, self.end_index) : max(
                    self.start_index, self.end_index
                )
                + 1
            ]
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

        _logger.debug("New selection started")

    @api.commands.register()
    def batchmark_accept(self) -> None:
        """Accept the changes of the current Batch Mark Selection."""
        self._reset()
        _logger.debug("Selection accepted")

    @api.commands.register()
    def batchmark_toggle(self) -> None:
        """Starts and ends Batch Mark Selection.

        In case we are currently in Batch Mark, accept the changes. Otherwise start
        Batch Mark."""

        if self._is_started():
            self.batchmark_accept()
        else:
            self.batchmark_start()

    @api.commands.register()
    def batchmark_cancel(self) -> None:
        """Cancels the Batch Mark Selection if started."""
        if self._is_started():
            to_mark = self._triggered & self._prev_marked
            to_unmark = self._triggered - self._prev_marked
            api.mark.mark(to_mark, api.mark.Action.Mark)
            api.mark.mark(to_unmark, api.mark.Action.Unmark)
            self._reset()
            _logger.debug("Selection cancelled")
        else:
            _logger.debug("Nothing to cancel")

    def _is_started(self):
        """Indicate if a selection has been started."""
        if self.paths is None or self.start_index is None:
            return False

        return True

    @api.status.module("{batchmark}")
    def batchmark(self) -> str:
        if self._is_started():
            color = styles.get("base0d")
            return wrap_style_span(f"color: {color}", "<b>+</b>")

        return ""

    def _reset(self):
        self.start_index = None
        self.end_index = None
        self.paths = None
        self._prev_marked = set()
        self._triggered = set()


def init(*_args: Any, **_kwargs: Any) -> None:
    """Initialize BatchMark class."""
    BatchMark()
