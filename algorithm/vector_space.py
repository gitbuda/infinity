# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Vector Space

Standard TF * IDF implementation.
'''

import numpy as np

from util.timeit import timeit
from scipy.sparse import csr_matrix
from data_structure.page import Page
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess

tf = lambda freq, max_freq: 0.5 + 0.5 * freq / max_freq
euclidian = lambda x, y: np.sqrt(np.sum((x-y)**2))
mahalanobis = lambda x, y: np.sum(np.absolute(x - y))


class IRAlgorithm:

    def configure(self, config=None):
        '''
        The main config is which distance function to use.
        '''
        self.idf = None
        self.tokens = {}
        self.tokens_no = 0
        self.distance = euclidian

    @timeit
    def process(self, raw_files):
        '''
        '''
        self.documents = preprocess(raw_files)

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

        # TF * IDF for each document
        for key, document in self.documents.items():
            doc_tf = np.zeros(self.tokens_no)
            bag = document.bag
            max_freq = bag[max(bag, key=bag.get)]
            for token in document.bag:
                index = self.tokens[token]
                doc_tf[index] = tf(bag[token], max_freq)
            document.w = csr_matrix(doc_tf * self.idf)

        print("TOKENS NO: %s" % self.tokens_no)

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        '''
        tokens = tokenize_text(query)
        if len(tokens) <= 0:
            return []

        query_tf = np.zeros(self.tokens_no)
        for token in tokens:
            if token not in self.tokens:
                continue
            index = self.tokens[query]
            query_tf[index] = tf(1, 1)
        query_w = query_tf * self.idf

        ranks = []
        for key, document in self.documents.items():
            ranks.append((key, self.distance(document.w.toarray(), query_w)))

        ranks = sorted(ranks, key=lambda x: x[1])

        return ranks[page.start_index:page.end_index]
