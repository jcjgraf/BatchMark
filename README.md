## Vimiv Batch Mark
> [vimiv](https://github.com/karlch/vimiv-qt) plugin for batch marking images

Vimiv Batch Mark lets you easily mark contiguous images

### Installation
- Clone this project into `$XDG_DATA_HOME/vimiv/plugins/`
- Activate Vimiv Importer by adding `batchmark =` to the `PLUGINS` section of `$XDG_CONFIG_HOME/vimiv/vimiv.conf`.

### Usage
- Select the first image you want to mark
- Run `:batchmark-start`
- Select the last image you want to mark
- Run `:batchmark-end`

If at least one image in the range is not marked, all images get marked. If all images are already marked, the all get unmarked.

### Commands

- `batchmark-start`: Start Batch Mark selector at current image.

- `batchmark-end`: End Batch Mark selection at current image. If the selection is valid the selected images are (un)marked.

- `batchmark-toggle`: Starts/ends a Batch Mark selection depending if we have started on already. Binding this command to e.g. `V` in vimiv would result in similar functionality as Vims visual mode.

- `batchmark-cancel`: Cancels an already started Batch Mark selection.

### Status Bar Module
Batch Mark provides the status bar module `{batchmark}`. It indicates if a Batch Mark has been started and if the current Batch Mark got invalid due to a change of path.

For instruction on how to enable it please consult the [vimiv docs](https://karlch.github.io/vimiv-qt/documentation/configuration/statusbar.html).
