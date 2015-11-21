# -*- coding: utf-8 -*-

import numpy as np

from util.timeit import timeit
from preprocess.preprocessor import preprocess
from scipy.sparse import csr_matrix

tf = lambda freq, max_freq: 0.5 + 0.5 * freq / max_freq
euclidian = lambda x, y: np.sqrt(np.sum((x-y)**2))
mahalanobis = lambda x, y: np.sum(np.absolute(x - y))


class IRAlgorithm:

    def configure(self, config=None):
        '''
        '''
        self.idf = None
        # self.token_doc_no = {}
        # token index
        self.tokens = {}
        self.tokens_no = 0
        self.distance = euclidian

    @timeit
    def process(self, raw_files):
        '''
        '''
        self.documents = preprocess(raw_files)

        # TODO: extract from here
        # TODO: write more optimal

        # IDF
        self.idf = []
        for key, document in self.documents.items():
            for token in document.bag:
                if token not in self.tokens:
                    self.idf.append(0)
                    self.tokens[token] = self.tokens_no
                    self.tokens_no += 1
                index = self.tokens[token]
                self.idf[index] += 1
        self.idf = np.array(self.idf)
        self.idf = np.log(1.0 * len(self.documents) / self.idf)

        # tf + tf * idf
        for key, document in self.documents.items():
            doc_tf = np.zeros(self.tokens_no)
            bag = document.bag
            max_freq = bag[max(bag, key=bag.get)]
            for token in document.bag:
                index = self.tokens[token]
                doc_tf[index] = tf(bag[token], max_freq)
            document.w = csr_matrix(doc_tf * self.idf)

    @timeit
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
            ranks.append((key, self.distance(document.w.toarray(), query_w)))

        ranks = sorted(ranks, key=lambda x: x[1])

        return ranks
