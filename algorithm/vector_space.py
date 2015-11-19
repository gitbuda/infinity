# -*- coding: utf-8 -*-

import bager
import tokenizer
import numpy as np

from math import log
from data_structure.document import create_doc_from_files

tf = lambda freq, max_freq: 0.5 + 0.5 * freq / max_freq
euclidian = lambda x, y: np.sqrt(np.sum((x-y)**2))
mahalanobis = lambda x, y: np.sum(np.absolute(x - y))


class IRAlgorithm:

    def configure(self, config=None):
        '''
        '''
        self.idf = None
        self.token_doc_no = {}
        # token index
        self.tokens = {}
        self.tokens_no = 0
        self.distance = euclidian

    def process(self, raw_files):
        '''
        '''
        self.documents = create_doc_from_files(raw_files)
        self.documents = tokenizer.tokenize(self.documents)
        self.documents = bager.bag(self.documents)

        # TODO: extract from here
        # TODO: write more optimal
        # all terms indices
        for key, document in self.documents.items():
            for token in document.bag:
                # for idf
                self.token_doc_no[token] = self.token_doc_no.get(token, 0) + 1
                if token in self.tokens:
                    continue
                else:
                    self.tokens[token] = self.tokens_no
                    self.tokens_no += 1

        # idf vector
        self.idf = np.zeros(self.tokens_no)
        for token, doc_no in self.token_doc_no.items():
            index = self.tokens[token]
            self.idf[index] = log(len(self.documents) / doc_no)

        # tf + tf * idf
        for key, document in self.documents.items():
            document.tf = np.zeros(self.tokens_no)
            bag = document.bag
            max_freq = bag[max(bag, key=bag.get)]
            for token in document.bag:
                index = self.tokens[token]
                document.tf[index] = tf(bag[token], max_freq)
            document.w = document.tf * self.idf

        # print(len(self.documents))
        # print(len(self.idf))
        # print(self.idf)
        # print(len(self.token_doc_no))

    def run(self, query):
        '''
        '''
        if query not in self.tokens:
            return []

        # TODO: finish
        query_tf = np.zeros(self.tokens_no)
        index = self.tokens[query]
        query_tf[index] = tf(1, 1)
        query_w = query_tf * self.idf

        ranks = []
        for key, document in self.documents.items():
            ranks.append((key, self.distance(document.w, query_w)))

        ranks = sorted(ranks, key=lambda x: x[1])

        return ranks
