# -*- coding: utf-8 -*-

# FROM: https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-
#       the-execution-time-of-methods

import time


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r -> %2.3f sec' % (method.__name__, te - ts))
        return result

    return timed
