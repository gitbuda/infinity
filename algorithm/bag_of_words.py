# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Bag Of Words

A document is higher in the ranking table if it
contains more occurances of specific term.
Each document is observed separately.

The number of token occurrence in a document is
normalized by document size. From my opinion that gives
better results.
'''

import logging
from util.timeit import timeit
from data_structure.page import Page
from preprocess.bager import bag_of_documents
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess_one
from preprocess.preprocessor import preprocess_all

logger = logging.getLogger(__name__)


class IRAlgorithm:

    def configure(self, config=None):
        '''
        No configuration.
        '''
        pass

    @timeit
    def preprocess_all(self, raw_files):
        '''
        Converts the raw files into the documents.
        For each document creates tokens and bag of words.

        Args:
            raw_files: dictionary[document_key] = document_content
        '''
        logger.info("Preprocessing...")
        self.documents = preprocess_all(raw_files)
        self.docs_bag = bag_of_documents(self.documents)

    @timeit
    def preprocess_one(self, raw_file):
        '''
        Takes single document (raw_file)
        and calculates all that is neccessary to incorporate
        that document into the existing set of documents.

        Args:
            raw_file: text (string)
        '''
        logger.info("Preprocessing one...")

        # create document
        document = preprocess_one(raw_file)

        # update docs_bag dict
        for token, occurrences in document.bag.items():
            docs_number = self.docs_bag.get(token, {})
            docs_number[document.identifier] = occurrences
            self.docs_bag[token] = docs_number

        # add the document to the documents set
        self.documents[document.identifier] = document

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        Procedure:
            1. tokenize the query
            2. for each token get normalized score for each document
               that contains the token
            3. sum all normalized scores

        Why normalization:
        E.g. let's say that the query is "test" the document
        "Test one more time." is more relevant than document
        "Test one more time because something could went wrong.",
        because test has bigger impact.

        Args:
            query: query string
            page: page size and offset

        Returns:
            list of identifiers
        '''
        tokens = tokenize_text(query)
        if len(tokens) <= 0:
            return []

        data = {}
        for token in tokens:
            if token not in self.docs_bag:
                continue
            docs_bag_item = self.docs_bag[token]
            for doc_key, token_occurrence in docs_bag_item.items():
                doc_size = len(self.documents[doc_key].tokens)
                if doc_size <= 0:
                    normalized = 0
                else:
                    normalized = token_occurrence / doc_size
                data[doc_key] = data.get(doc_key, 0) + normalized
        data = sorted(data, key=data.get, reverse=True)

        return data[page.start_index:page.end_index]
