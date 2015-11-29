# -*- coding: utf-8 -*-

'''
Generally, information retrival algorithms have some
kind of preprocessing. The main purpose of
this class is to control the preprocessing.
'''

from data_structure.document import text_hash
from algorithm.bag_of_words import IRAlgorithm as BagOfWords
from algorithm.vector_space import IRAlgorithm as VectorSpace
from algorithm.binary_independence import IRAlgorithm as BinaryIndependence


class AlgorithmBox:

    def __init__(self):
        '''
        Instantiate all available algorithms.
        '''
        self.available_algorithms = {
            'bag_of_words': BagOfWords(),
            'vector_space': VectorSpace(),
            'binary_independence': BinaryIndependence()
        }

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, value):
        self.__files = value
        # if variable files is changed than all algorithms
        # have to be reinitialized
        self.prepared_algorithms = {}

    def append(self, raw_file):
        '''
        Add raw_file to the files and update all
        prepared algorithms.

        Args:
            raw_file: file represented as string
        '''
        file_key = text_hash(raw_file)
        self.files[file_key] = raw_file

        for alg_name, algorithm in self.prepared_algorithms.items():
            algorithm.preprocess_one(raw_file)

    def algorithm(self, algorithm_name):
        '''
        Returns instance of the algorithm specified by algorithm name.

        If algorithm is not initialized this method will run
        initialization. If files are not changed
        the next call of this method will not reinitialize the algorithm.

        Args:
            algorithm_name: name of concrete algorithm
        '''
        if algorithm_name not in self.available_algorithms:
            # TODO: use AlgorithmException
            raise Exception("No Algorithm")

        if algorithm_name not in self.prepared_algorithms:
            algorithm = self.available_algorithms[algorithm_name]
            algorithm.configure()
            algorithm.preprocess_all(self.files)
            self.prepared_algorithms[algorithm_name] = algorithm

        return self.prepared_algorithms[algorithm_name]
