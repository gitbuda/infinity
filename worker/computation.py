# -*- coding: utf-8 -*-

'''
Computational instance.
'''

import json
import falcon
import parser
import requests
from data_structure.page import Page
from common.falcon.middleware.max_body import max_body
from common.falcon.middleware.require_json import RequireJSON
from common.falcon.middleware.json_translator import JSONTranslator
from algorithm.bag_of_words import IRAlgorithm as BagOfWords


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class QueryResource:

    def __init__(self):
        '''
        Fetch all documents from the database and initialize
        the algorithm for ranking (bag of words)
        '''
        print("Document Resource init start")
        r = requests.get('http://idb.infinity.buda.link:9001/api/data/documents/all')
        documents = {}
        for document in json.loads(r.text):
            identifier = document['identifier']
            print(identifier)
            text = document['content']
            documents[identifier] = text
        print("All documents are fetched")
        self.algorithm = BagOfWords()
        self.algorithm.configure()
        self.algorithm.preprocess_all(documents)
        print("Document Resource init end")

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        '''
        Returns documents ranked by search query within the request body.

        Args:
            req.params['pagenum'] = page number
            req.params['pagesize'] = page size
            req.body = ranking query
        '''
        pagenum = int(req.get_param('pagenum', default=0))
        pagesize = int(req.get_param('pagesize', default=5))
        page = Page(pagenum, pagesize)
        body = req.context['doc']
        query = body['query']
        rank = self.algorithm.run(query, page)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(rank)

# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])
query_resource = QueryResource()
app.add_route('/api/query', query_resource)
