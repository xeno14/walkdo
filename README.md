walkdo
======

Walk the directory tree and bring to new place.

# Example

```sh
example.py --src=$HOME/Pictures/ --dest=/path/to/dst --cmd=symlink
```

You will find `jpeg` and `png` directories under `dst` and `jpeg` contains
full of jpeg symlinks and `png` so on.


Run `example.py --help` for help.

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

```python
@walkdo.dest("jpeg")
def pick_jpeg(root, filename):
    """Pick files with jpeg filenam extension."""
    _, ext = os.path.splitext(filename)
    if ext == ".jpg" or ext == ".jpeg":
        return True
    return False
```

See `example.py`
