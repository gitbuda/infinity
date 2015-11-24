#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
CLI interface.

-q "query" -> "It is a basic principle of Islam that if one is born muslim..."
-a "algorithm" -> "bag_of_words"
-n "number of results" -> 20

Implemented algorithms:
    bag_of_words
    vector_space
    binary_independence
'''

import shlex
import parser
import logging
import util.argument as arg
from data_structure.page import Page
from algorithm.algorithm_box import AlgorithmBox

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # get input arguments
    query = arg.get_argv('q', 'test')
    algorithm_name = arg.get_argv('a', 'bag_of_words')
    number_of_results = int(arg.get_argv('n', 20))

    # load local files
    files_path = '20news-18828'
    logger.info('Loading files...')
    files = parser.parse('20news-18828', 'iso-8859-1')
    logger.info('Files from %s are loaded.' % files_path)

    # create algorithm box object (context object)
    algorithm_box = AlgorithmBox()
    algorithm_box.files = files

    # execute algorithm
    page = Page(0, number_of_results)
    algorithm = algorithm_box.algorithm(algorithm_name)
    rank = algorithm.run(query, page)
    logger.info("Result: %s" % rank)

    print('---- MANUAL ----------')
    print('-q "query"')
    print('-a "algorithm"')
    print('-n "number of results"')
    print('-d "new document"')
    print('-e exit')
    print('----------------------')

    # if -d exists its priority is the higest one
    # so if -d exists the new document will be added
    # everything else will be ignored

    while True:
        command_line = shlex.split(input('Arguments:'))
        if '-e' in command_line:
            print("Bye!")
            break

        query = arg.get_cl(command_line, 'q', 'test')
        algorithm_name = arg.get_cl(command_line, 'a', 'bag_of_words')
        number = int(arg.get_cl(command_line, 'n', 20))
        document = arg.get_cl(command_line, 'd', '')

        if document is not '':
            document_hash = str(hash(document))
            files[document_hash] = document
            algorithm_box.files = files
            logger.info('New document: key = %s, content = %s' %
                        (document_hash, document))
            continue

        # execute algorithm
        page = Page(0, number)
        algorithm = algorithm_box.algorithm(algorithm_name)
        rank = algorithm.run(query, page)
        logger.info("Result: %s" % rank)
