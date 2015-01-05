#!/usr/bin/env python

import walkdo
import string
import os


@walkdo.name
def upper(root, filename):
    return string.upper(filename)


@walkdo.dest("jpeg")
def pick_jpeg(root, filename):
    _, ext = os.path.splitext(filename)
    if ext == ".jpg" or ext == ".jpeg":
        return True
    return False


@walkdo.dest("png")
def pick_png(root, filename):
    _, ext = os.path.splitext(filename)
    if ext == ".png":
        return True
    return False


if __name__ == '__main__':
    import sys
    walkdo.start(sys.argv)
