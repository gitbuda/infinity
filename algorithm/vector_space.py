# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Vector Space

TF * IDF implementation.
'''

import logging
import numpy as np
from util.timeit import timeit
from preprocess.bager import bag
from scipy.sparse import lil_matrix
from scipy.sparse import csr_matrix
from data_structure.page import Page
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess
from sklearn.metrics.pairwise import cosine_distances

logger = logging.getLogger(__name__)

tf = lambda freq, max_freq: 0.5 + 0.5 * freq / max_freq


class IRAlgorithm:

    def configure(self, config=None):
        '''
        The main config is which distance function to use.
        '''
        self.distance = cosine_distances

    @timeit
    def process(self, raw_files):
        '''
        '''
        logger.info("Preprocessing...")
        self.documents = preprocess(raw_files)
        self.docs_no = len(self.documents)

        self.determine_idf()
        self.determine_tf()
        self.calculate_tf_idf()

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        '''
        # tokenize query
        tokens = tokenize_text(query)
        if len(tokens) <= 0:
            return []

        # calculate query weigth
        bag_of_words = bag(tokens)
        max_freq = bag_of_words[max(bag_of_words, key=bag_of_words.get)]
        query_tf = lil_matrix((1, self.tokens_no))
        for token, freq in bag_of_words.items():
            if token not in self.tokens:
                continue
            index = self.tokens[token]
            query_tf[0, index] = tf(freq, max_freq)
        query_tf = csr_matrix(query_tf)
        query_w = csr_matrix(query_tf.multiply(self.idf))

        # calculate distances between all documents and query
        distances = self.distance(self.tf_idf, query_w)

        # sort results and return specified page of results
        distances = distances[:, 0]
        sorted_indices = np.argsort(distances)
        top = sorted_indices[page.start_index:page.end_index]

        f = np.vectorize(lambda x: self.iterative_docs[x])

        return list(f(top))

    @timeit
    def determine_idf(self):
        '''
        '''
        self.tokens = {}
        # tokens number
        self.tokens_no = 0
        self.idf = []
        self.iterative_docs = []
        for key, document in self.documents.items():
            self.iterative_docs.append(key)
            for token in document.bag:
                if token not in self.tokens:
                    self.idf.append(0)
                    self.tokens[token] = self.tokens_no
                    self.tokens_no += 1
                index = self.tokens[token]
                self.idf[index] += 1
        self.idf = np.array(self.idf)
        self.idf = np.log(1.0 * len(self.documents) / self.idf)
        self.idf = csr_matrix(self.idf)

    @timeit
    def determine_tf(self):
        '''
        Calculate Term Frequency matrix from all documents.
        '''
        self.tf = lil_matrix((self.docs_no, self.tokens_no))
        for key, document in self.documents.items():
            bag = document.bag
            max_freq = bag[max(bag, key=bag.get)]
            for token in document.bag:
                token_index = self.tokens[token]
                doc_index = document.index
                self.tf[doc_index, token_index] = tf(bag[token], max_freq)
        self.tf = self.tf.tocsr()

    @timeit
    def calculate_tf_idf(self):
        '''
        '''
        self.tf_idf = self.tf.multiply(self.idf)
