# -*- coding: utf-8 -*-

'''
Generally, information retrival algorithms have some
kind of preprocessing. The main purpose of
this class is to control the preprocessing.
'''

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

    def algorithm(self, algorithm_name):
        '''
        Returns instance of the algorithm specified by algorithm name.

        If algorithm is not initialized this method will run
        initialization. If data (files) are not change meanwhile
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
            algorithm.process(self.files)
            self.prepared_algorithms[algorithm_name] = algorithm

        return self.prepared_algorithms[algorithm_name]
