# -*- coding: utf-8 -*-

'''

'''

import json
import falcon
import parser
from worker.middleware.max_body import max_body
from worker.middleware.require_json import RequireJSON
from worker.middleware.json_translator import JSONTranslator
from algorithm.bag_of_words import IRAlgorithm as BagOfWords


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DocumentResource:

    def __init__(self):
        print("Document Resource init start")
        files = parser.parse('../20news-18828', 'iso-8859-1')
        self.algorithm = BagOfWords()
        self.algorithm.configure()
        self.algorithm.process(files)
        print("Document Resource init end")

    def on_get(self, req, resp):
        '''
        Returns all available documents.

        Args:
            req.params['pagenum'] = page number
            req.params['pagesize'] = page size
        '''
        resp.status = falcon.HTTP_200  # This is the default status
        response = [{'id': '1', 'name': 'bla1'}, {'id': '2', 'name': 'bla2'}]
        resp.body = json.dumps(response)

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        '''
        Returns documents ranked by search query within request body.

        Args:
            req.params['pagenum'] = page number
            req.params['pagesize'] = page size
            req.body = ranking query
        '''
        body = req.context['doc']
        query = body['query']
        rank = self.algorithm.run(query)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(rank)

# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])

# Resources are represented by long-lived class instances
document_resource = DocumentResource()

# things will handle all requests to the '/things' URL path
app.add_route('/api/document', document_resource)
