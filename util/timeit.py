# -*- coding: utf-8 -*-

'''
Python decorator function for measuring method execution time.
'''

# FROM: https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-
#       the-execution-time-of-methods

import time
import logging

logger = logging.getLogger(__name__)


def timeit(method):
    '''
    Take method name.
    '''
    def timed(*args, **kw):
        '''
        Take method arguments.
        '''
        ts = time.time()
        # execute the method
        result = method(*args, **kw)
        te = time.time()
        if len(args) >= 0:
            logger.info('%r -> %r -> %2.3f sec' %
                        (args[0], method.__name__, te - ts))
        else:
            logger.info('%r -> %2.3f sec' %
                        (method.__name__, te - ts))
        return result

    return timed
