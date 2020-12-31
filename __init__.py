# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

from typing import Any

from vimiv import api
from vimiv.gui.mainwindow import MainWindow
from vimiv.utils import log

_logger = log.module_logger(__name__)

start_index = None
start_paths = None

library = MainWindow.instance._library


@api.commands.register()
def batchmarkstart() -> None:
    global start_paths, start_index

    start_paths = library.model().paths
    currentPath = library.current()
    start_index = library.model().paths.index(currentPath)


@api.commands.register()
def batchmarkend() -> None:
    global start_paths, start_index

    end_paths = library.model().paths

    if start_paths != end_paths:
        return

    currentPath = library.current()
    end_index = library.model().paths.index(currentPath)

    selected_paths = end_paths[
        min(start_index, end_index) : max(start_index, end_index) + 1
    ]

    # If all images are maked, unmark them, else mark them
    was_marked = False

    for path in selected_paths:
        try:
            api.mark._unmark(path)
        except ValueError:
            was_marked = True
            continue

    if was_marked:
        for path in selected_paths:
            api.mark._mark(path)
