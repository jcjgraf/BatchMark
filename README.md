## Vimiv Batch Mark
> [vimiv](https://github.com/karlch/vimiv-qt) plugin for batch marking images

Vimiv Batch Mark lets you easily mark contiguous images.

### Installation
- Clone this project into `$XDG_DATA_HOME/vimiv/plugins/`.
- Activate Vimiv Batch Mark by adding `batchmark =` to the `PLUGINS` section of `$XDG_CONFIG_HOME/vimiv/vimiv.conf`.

### Usage
- Select the first image you want to mark
- Run `:batchmark-toggle`
- Select the last image you want to mark
- Run `:batchmark-toggle`

In case the start image is currently marked, all images in the selection will be unmarked. Otherwise, all images in the selection will be marked.

The selection can be undone by calling `batchmark-cancel`. Pressing `ESC` has the same effect.

### Commands

- `batchmark-start`: Start Batch Mark Selection at current image.

- `batchmark-accept`: End Batch Mark Selection at current image.

- `batchmark-toggle`: Dynamically start or end the Batch Mark Selection. Binding this command to e.g. `v` in vimiv would result in similar functionality as Vims visual mode.

- `batchmark-cancel`: Cancels an already started Batch Mark Selection.

### Status Bar Module
Batch Mark provides the status bar module `{batchmark}`. It indicates if a Batch Mark Selection has been started.

For instruction on how to enable it please consult the [vimiv docs](https://karlch.github.io/vimiv-qt/documentation/configuration/statusbar.html).
