# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Binary Indepentence

The problem with this model is that e.g. for only one term,
let say "test" all documents with "test" term inside have
the same wight sum.

Documentation:
    FER Text Analysis and Information Retrieval (TER)
    year: 2013/2014 slides: TAR-03-IR.pdf slide: 38-42
'''

import math
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

        Procedure:
            1. create documents
            2. get documents number
            3. for each term determine all documnets in which
               that term exists and how many time it occurs (docs_bag)

        Args:
            raw_files: dict (key = document key, value = document text)
        '''
        logger.info("Preprocessing...")
        self.documents = preprocess_all(raw_files)
        self.docs_no = len(self.documents)
        self.docs_bag = bag_of_documents(self.documents)

    @timeit
    def preprocess_one(self, raw_file):
        '''
        Takes single document (raw_file)
        and calculates all neccessary to incorporate
        that document into the existing set of documents.

        Args:
            raw_file: text (string)
        '''
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
        Theory:
            t -> term / token
            r -> relevant
            D -> document
            Q -> query
            sum -> sum by all terms from query
            w_t -> weight of term
            sum(w_t) -> sum of all weights from query

            document weight = sum(log(p(D_t|Q,r) / p(D_t|Q,not r)))
            where p(D_t|Q,r) = 0.5
                  p(D_t|Q,not r) = n_t / N_d
            where n_t = number of documents containing term t
                  N_d = total number of documents

        Args:
            query: query string
            paga: used defined page
        '''
        tokens = tokenize_text(query)
        if len(tokens) <= 0:
            return []

        results = []
        for doc_key, document in self.documents.items():
            result = 0
            for token in tokens:
                if token not in document.bag:
                    continue
                token_docs = self.docs_bag.get(token, {})
                token_docs_len = len(token_docs)
                if token_docs_len <= 0:
                    continue
                ratio = 1.0 * token_docs_len / self.docs_no
                if abs(ratio - 10e-8) < 0:
                    continue
                result += math.log(0.5 / ratio)
            if result > 0:
                results.append((doc_key, result))

        results = sorted(results, key=lambda x: x[1], reverse=True)
        results = list(map(lambda x: x[0], results))

        return results[page.start_index:page.end_index]
