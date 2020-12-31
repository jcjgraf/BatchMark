## Vimiv Batch Mark
> [vimiv-qt](https://raw.github.com/karlch/vimiv-qt) plugin for batch marking images

Vimiv Batch Mark lets you easily mark contiguous images

### Installation
- Clone this project into `$XDG_DATA_HOME/vimiv/plugins/`
- Activate Vimiv Importer by adding `batchmark =` to the `PLUGINS` section of `$XDG_CONFIG_HOME/vimiv/vimiv.conf`.

### Usage
- Select the first image you want to mark
- Run `:batchmarkstart`
- Select the last image you want to mark
- Run `:batchmarkend`

If at least one image in the range is not marked, all images get marked. If all images are already marked, the all get unmarked.
