# -*- coding: utf-8 -*-

import json
import falcon
# import parser
import datetime
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from data_structure.document import text_hash
from common.falcon.middleware.max_body import max_body
from common.falcon.middleware.require_json import RequireJSON
from common.falcon.middleware.json_translator import JSONTranslator


class DocumentBase(object):

    def __init__(self):
        '''
        Create db connection and
        load data from the local folder.
        '''
        self.client = MongoClient('db.infinity.buda.link', 27017,
                                  connect=False)
        self.db = self.client.styria
        self.documents = self.db.documents
        # files = parser.parse('../20news-18828', 'iso-8859-1')
        # for file_name, file_content in files.items():
        #     self.insert(file_content)

    def insert(self, content):
        '''
        Private method for mongodb insertion operation.
        '''
        document = {}

        content_hash = text_hash(content)
        existing_documents = self.documents.find({"identifier": content_hash})
        if existing_documents.count() > 0:
            return existing_documents[0]

        document['content'] = content
        document['identifier'] = content_hash
        document['date'] = datetime.datetime.utcnow()
        result = self.documents.insert_one(document)
        print("Inserted: %s" % content_hash)
        inserted = self.documents.find({"identifier": content_hash})[0]
        return inserted


class SingleDocumentResource(DocumentBase):

    def __init__(self):
        super().__init__()

    def on_get(self, req, resp, identifier):
        '''
        Return document with the identifier.
        '''
        cursor = self.documents.find({"identifier": identifier})
        if cursor.count() <= 0:
            resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_200
            resp.body = dumps(cursor[0])


class CountDocumentResource(DocumentBase):

    def __init__(self):
        super().__init__()

    def on_get(self, req, resp):
        '''
        Returns counter of documents.
        '''
        count = self.documents.count()
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'count': str(count)})


class DocumentResource(DocumentBase):

    def __init__(self):
        super().__init__()

    def on_get(self, req, resp):
        '''
        Returns documents (with pagination).
        '''
        pagenum = int(req.get_param('pagenum', default=0))
        pagesize = int(req.get_param('pagesize', default=20))
        resp.status = falcon.HTTP_200
        documents = []
        cursor = self.documents.find().skip(pagenum * pagesize).limit(pagesize)
        for document in cursor:
            documents.append(document)
        resp.body = dumps(documents)

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        '''
        Create new document. If the same document
        exists do nothing, only return document id.
        '''
        body = req.context['doc']
        if 'content' not in body:
            raise falcon.HTTPBadRequest('Wrong request body.',
                                        'content element is required')
        content = body['content']
        result = self.insert(content)
        resp.body = dumps(document)


class AllDocumentResource(DocumentBase):

    def __init__(self):
        super().__init__()

    def on_get(self, req, resp):
        '''
        Returns all documents.
        '''
        resp.status = falcon.HTTP_200
        documents = []
        cursor = self.documents.find()
        for document in cursor:
            documents.append(document)
        resp.body = dumps(documents)


app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])
app.add_route('/api/data/document/{identifier}', SingleDocumentResource())
app.add_route('/api/data/documents', DocumentResource())
app.add_route('/api/data/documents/count', CountDocumentResource())
app.add_route('/api/data/documents/all', AllDocumentResource())
