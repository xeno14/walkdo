#!/usr/bin/env python

import walkdo
import string
import os


# Gives name conversion rule. In this case, all files will be converted into
# upper case.
@walkdo.name
def upper(root, filename):
    return string.upper(filename)


# Pick files with extention 'jpeg'. In this case, just return True or False.
@walkdo.dest("jpeg")
def pick_jpeg(root, filename):
    _, ext = os.path.splitext(filename)
    if ext == ".jpg" or ext == ".jpeg":
        return True
    return False


# Pick png files.
@walkdo.dest("png")
def pick_png(root, filename):
    _, ext = os.path.splitext(filename)
    if ext == ".png":
        return True
    return False


# If the function returns string, new directory named after the returned string
# will be created under the destination.
@walkdo.dest("by_ext")
def pick_by_ext(root, filename):
    _, ext = os.path.splitext(filename)
    ext = string.lower(ext[1:])  # remove '.'
    return ext


if __name__ == '__main__':
    import sys
    walkdo.start(sys.argv)
