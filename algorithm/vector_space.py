# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Vector Space

TF * IDF implementation.

Documentation:
    FER Text Analysis and Information Retrieval (TAR)
    year: 2013/2014 slides: TAR-03-IR.pdf
'''

import logging
import numpy as np
from util.timeit import timeit
from preprocess.bager import bag
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse import vstack, hstack
from data_structure.page import Page
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess_one
from preprocess.preprocessor import preprocess_all
from sklearn.metrics.pairwise import euclidean_distances

logger = logging.getLogger(__name__)

tf = lambda freq, max_freq: freq / max_freq


class IRAlgorithm:

    def configure(self, config=None):
        '''
        Default is the euclidean because it is faster than
        the cosine distance.
        '''
        self.distance = euclidean_distances

    @timeit
    def preprocess_all(self, raw_files):
        '''
        Converts the raw files into the documents and
        executes preprocess algorithm on all of them.

        Calculates tf, idf, tf * idf.

        Args:
            raw_files: dict[identifier] = text
        '''
        logger.info("Preprocessing...")
        self.documents = preprocess_all(raw_files)
        self.docs_no = len(self.documents)

        self.determine_idf()
        self.determine_tf()
        self.tf_idf = self.tf.multiply(self.idf)

    @timeit
    def preprocess_one(self, raw_file):
        '''
        Takes single document (raw_file)
        and calculates all neccessary to incorporate
        that document into the existing set of documents.

        Args:
            raw_file: text (string)
        '''
        logger.info("Preprocessing one...")

        # create document
        document = preprocess_one(raw_file)
        if document.identifier in self.documents:
            logger.info("Document already exists.")
            return

        # update documents
        self.documents[document.identifier] = document
        self.docs_no = len(self.documents)
        self.iterative_docs.append(document.identifier)

        # update tokens
        for token, occurrence in document.bag.items():
            if token not in self.tokens:
                self.tokens[token] = self.tokens_no
                self.tokens_no += 1

        new_tf_shape = (self.docs_no, self.tokens_no)
        new_idf_shape = (1, self.tokens_no)

        # resize matrices
        tf_lil = resize_tf(self.tf, new_tf_shape)
        idf_lil = resize_idf(self.idf, new_idf_shape)

        # update tf
        max_freq = document.bag[max(document.bag, key=document.bag.get)]
        for token, freq in document.bag.items():
            token_index = self.tokens[token]
            doc_index = self.docs_no - 1
            tf_lil[doc_index, token_index] = tf(freq, max_freq)

        # update idf
        for token in document.bag:
            index = self.tokens[token]
            idf_lil[0, index] += 1

        # convert back to csr (faster multiplication)
        self.tf = tf_lil.tocsr()
        self.idf = idf_lil.tocsr()

        # TODO: multiply only last row
        self.tf_idf = self.tf.multiply(self.idf)

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        Procedure:
            1. tokenize the query
            2. calculate query weight
            3. calculate all distances
            4. sort distances
            5. return sorted result

        Args:
            query: query string
            page: page size and offset

        Returns:
            list of identifiers
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

        # sort results and return specified page
        distances = distances[:, 0]
        sorted_indices = np.argsort(distances)
        top = sorted_indices[page.start_index:page.end_index]
        f = np.vectorize(lambda x: self.iterative_docs[x])
        result = list(f(top))

        return result

    @timeit
    def determine_idf(self):
        '''
        Calculate Inverse Frequency vector from all documents.

                                |D|
        idf_i = log(---------------------------)
                    |{d elem D | t_i elem D_j}|

        This method also calculates tokens dict, tokens number
        and iterative_docs (list of all document identifiers).

        Returns:
            nothing but self.idf is recalculated
        '''
        self.tokens = {}
        self.tokens_no = 0
        self.idf = []
        self.iterative_docs = [0] * len(self.documents)
        for key, document in self.documents.items():
            self.iterative_docs[document.index] = key
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

                                freq(t_i, d_j)
        tf(t_i, d_j) = --------------------------------
                        max(freq(k, d_j) | k elem D_j)

        Returns:
            nothing but self.tf is recalculated
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

    def print_tf_idf(self):
        '''
        Debug method
        '''
        print('----------------')
        print('TF: ', self.tf.toarray())
        print('IDF: ', self.idf.toarray())
        print('TF IDF: ', self.tf_idf.toarray())
        print('----------------')


def resize_tf(matrix, new_shape):
    '''
    Takes matrix and appends rows and columns
    to fit the new shape. Fills out with zeros.

    Args:
        matrix: csr matrix
        new shape: numpy shape tuple

    Returns:
        matrix: resized lil matrix
    '''
    original_shape = matrix.shape
    row = csr_matrix((1, original_shape[1]))
    matrix = vstack([matrix, row])
    cols_no = new_shape[1] - original_shape[1]
    if cols_no <= 0:
        return matrix
    col = csr_matrix((new_shape[0], cols_no))
    matrix = hstack([matrix, col])
    return matrix.tolil()


def resize_idf(matrix, new_shape):
    '''
    Takes matrix and appends cols to fit the new shape.

    Args:
        matrix: csr matrix
        new shape: numpy shape tuple

    Returns:
        matrix: resized lil matrix
    '''
    original_shape = matrix.shape
    cols_no = new_shape[1] - original_shape[1]
    if cols_no <= 0:
        return matrix
    col = csr_matrix((1, cols_no))
    matrix = hstack([matrix, col])
    return matrix.tolil()


def resize_to_lil(matrix, shape):
    '''
    Resize sparse matrix by converting it
    to DOK and then converts it into LIL.

    Not very optimal, but scipy doesn't have
    csr_matrix reshape implemented.

    Args:
        matrix: sparse matrix
        shape: new matrix shape

    Returns:
        reshaped lil_matrix
    '''

    tf_dok = matrix.todok()
    tf_dok.resize(shape)
    return tf_dok.tolil()
