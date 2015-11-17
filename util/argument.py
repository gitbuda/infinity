# -*- coding: utf-8 -*-

import sys


def get(name, default=None):
    '''
    '''
    assert len(name) > 0

    args = sys.argv[1:]

    if len(name) == 1:
        name = '-' + name
    else:
        name = '--' + name

    index = args.index(name)

    if index >= len(args) - 1:
        return default

    arg = args[index + 1]
    return arg


if __name__ == '__main__':
    pass
