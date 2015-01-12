walkdo
======

Walk the directory tree and bring to new place.

# Example

```sh
example.py --src=$HOME/Pictures/ --dest=/path/to/dst --cmd=symlink
```

You will find `jpeg` and `png` directories under `dst` and `jpeg` contains
full of jpeg symlinks and `png` so on. If you do not want to create links,
add flag `--dryrun`.

Run `example.py --help` to see descriptions about flags.


# Decorators

## name

It gives name conversion rule.

```python
@walkdo.name
def upper(root, filename):
    """Convert filename into uppercase."""
    return string.upper(filename)
```

## dest

It gives condition to pick files to place under the destination.
It is allowed to return either bool or string. If string is returned, new
directory named after the string will be created under the destination.

```python
@walkdo.dest("jpeg")
def pick_jpeg(root, filename):
    """Pick files with jpeg filenam extension."""
    _, ext = os.path.splitext(filename)
    if ext == ".jpg" or ext == ".jpeg":
        return True
    return False

# This is equivalent to pick_jpeg
@walkdo.dest(".")
def pick_jpeg_2(root, filename):
    """Pick files with jpeg filenam extension."""
    _, ext = os.path.splitext(filename)
    if ext == ".jpg" or ext == ".jpeg":
        return "jpeg"
    return False
```

See `example.py`
