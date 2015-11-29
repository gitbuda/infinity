# -*- coding: utf-8 -*-

'''
Arguments utility. The main purpose of these methods
is to return value for an argument.
'''

import sys


def get_argv(name, default=None):
    '''
    Gets argument from sys.argv

    Args:
        name: argument name
        default: default value

    Returns:
        argument value
    '''
    # exclude the name of script
    # python script.py ... -> script.py is excluded
    args = sys.argv[1:]

    return get(args, name, default)


def get_cl(cl, name, default=None):
    '''
    Gets argument from generic command line array.

    Args:
        cl: list of command line argumetns
        name: argument name
        default: default value

    Returns:
        argument value
    '''
    return get(cl, name, default)


def get(source, name, default=None):
    '''
    Gets argument from source array.

    Args:
        source: list of arguments and values
        name: argument name
        default: default value

    Returns:
        argument value
    '''
    assert isinstance(source, list)
    assert len(name) > 0

    # append - of --, because otherwise
    # the caller has to write - or -- 
    # every time he wants a value
    if len(name) == 1:
        name = '-' + name
    else:
        name = '--' + name

    # if there is no name in array
    # return default value
    try:
        index = source.index(name)
    except ValueError:
        return default

    # if name is the last argument -> no value ->
    # return default
    if index >= len(source) - 1:
        return default

    # value is one position next to
    # argument
    arg = source[index + 1]

    return arg
