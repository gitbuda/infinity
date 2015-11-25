# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Bag Of Words

A document is higher in the ranking table if it
contains more occurances of specific term.
Each document is observed separately.

The number of token occurrence in a document is
normalized by document size. From my (buda) opinion
the results are better.
'''

import logging
from util.timeit import timeit
from data_structure.page import Page
from preprocess.bager import bag_of_documents
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess

logger = logging.getLogger(__name__)


class IRAlgorithm:

    def configure(self, config=None):
        '''
        No configuration.
        '''
        pass

    @timeit
    def process(self, raw_files):
        '''
        Converts the raw files into the documents.
        For each document create tokens and bag of words.

        Args:
            raw_files: dictionary[document_key] = document_content
        '''
        logger.info("Preprocessing...")
        self.documents = preprocess(raw_files)
        self.docs_bag = bag_of_documents(self.documents)

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        Procedure:
            1. tokenize the query
            2. for each token get normalized score for each document
               that contains the token
            3. sum all normalized scores

        Why normalization:
        E.g. let say that the query is "test" the document
        "Test one more time." is more relevant than document
        "Test one more time because something could went wrong.",
        because test has the bigger impact.
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
