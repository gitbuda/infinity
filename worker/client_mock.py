# -*- coding: utf-8 -*-

'''
Mock of the computation instance.

On this way is easier to develope
web client interface.
'''

import json
import falcon
from common.falcon.middleware.max_body import max_body
from common.falcon.middleware.require_json import RequireJSON
from common.falcon.middleware.json_translator import JSONTranslator
from data_structure.page import Page


class SingleDocumentResource:

    def __init__(self):
        super().__init__()

    def on_get(self, req, resp, identifier):
        '''
        Return document with the identifier.
        '''
        data = {}
        data['2'] = "two"
        data['3'] = "three"
        data['1'] = 'one'
        data['4'] = 'four'
        data['5'] = 'five'
        data['6'] = 'six'
        data['44'] = 'fourty four'
        data['446'] = 'four hunderd and forty four'
        data['100'] = 'one hunderd'
        text = data[identifier]
        response = {'identifier': identifier, 'content': text}
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(response)


class QueryResourceMock:

    def __init__(self):
        '''
        '''
        pass

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        '''
        Returns documents ranked by search query within request body.

        Args:
            req.params['pagenum'] = page number
            req.params['pagesize'] = page size
            req.body = ranking query
        '''
        # body = req.context['doc']
        # query = body['query']
        rank = ['2', '3', '1', '4', '5', '6', '44', '446', '100']
        try:
            page_number = int(req.params['pagenum'])
            page_size = int(req.params['pagesize'])
        except Exception:
            page_number = 0
            page_size = 5
        page = Page(page_number, page_size)
        data = rank[page.start_index:page.end_index]
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(data)

# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])
query_resource = QueryResourceMock()
app.add_route('/api/document/{identifier}', SingleDocumentResource())
app.add_route('/api/query', query_resource)
