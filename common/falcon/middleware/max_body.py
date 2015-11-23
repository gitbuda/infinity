# -*- coding: utf-8 -*-

'''
Flacon max body length decorator function.
'''

import falcon


def max_body(limit):

    def hook(req, resp, resource, params):
        '''
        TODO: comment
        '''
        length = req.content_length

        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')
            raise falcon.HTTPRequestEntityTooLarge('Request body is too large',
                                                   msg)

    return hook
