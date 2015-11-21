#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
import util.argument as arg

from algorithm.bag_of_words import IRAlgorithm as BagOfWords
from algorithm.vector_space import IRAlgorithm as VectorSpace
from algorithm.binary_independence import IRAlgorithm as BinaryIndependence

# import preprocessor
# # documents = preprocessor.spacy_parse(documents)

if __name__ == '__main__':

    query = arg.get('q', '')

    # files = parser.parse('20news-18828/rec.autos', 'iso-8859-1')
    files = parser.parse('20news-18828', 'iso-8859-1')

    algorithm = BagOfWords()
    algorithm = VectorSpace()
    algorithm = BinaryIndependence()

    algorithm.configure()
    algorithm.process(files)
    rank = algorithm.run(query)
    print(rank[:10])

    # document1 = documents['20news-18828/comp.graphics/37930']
    # document2 = documents['20news-18828/sci.med/58043']
    # print(document1.bag)
    # print(document2.bag)
