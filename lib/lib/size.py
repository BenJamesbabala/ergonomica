#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/size.py]

Defines the "size" command.
"""

import os
import math
from lib.lang.error import ErgonomicaError

verbs = {}

SIZES = ["byte(s)", "kilobyte(s)", "megabyte(s)", "gigabyte(s)", "terabyte(s)", "petabyte(s)"]
NAME_SIZES = ["byte", "kilobyte", "megabyte", "gigabyte", "terabyte", "petabyte"]
SHORT_SIZES = ["B", "kB", "MB", "GB", "TB", "PB"]

def size(env, args, kwargs):
    """[FILE,...] {unit:UNIT}@Prints the size of each file. If unit specified, displays size in that unit (B, kB, MB,...)."""
    out = []
    try:
        unit = kwargs["unit"]
        size_factor = 1
        if unit in SHORT_SIZES:
            size_factor = SHORT_SIZES.index(unit)
        elif unit in SIZES:
            size_factor = SIZES.index(unit) 
        elif unit in NAME_SIZES:
            size_factor = NAME_SIZES.index(unit)
                
        for item in args:
            try:
                size = os.path.getsize(item)
                out.append(item + " : " + str(size / 1024 ** size_factor) + " " + SIZES[size_factor])
            except OSError:
                raise ErgonomicaError("[ergo: NoSuchFileError]: No such file '%s'." % (item))
    except KeyError:
        for item in args:
            try:
                size = 0
                if item[0] in ["/", "~"]:
                    size = os.path.getsize(item)
                else:
                    size = os.path.getsize(env.directory + "/" + item)
                    size_factor = int(math.floor(math.log(size) / 6.93147))
                    out.append(item + " : " + str(size / 1024**size_factor) + " " + SIZES[size_factor])
            except OSError:
                raise ErgonomicaError("[ergo: NoSuchFileError]: No such file '%s'." % (item))
    return out

verbs["size"] = size
