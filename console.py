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
import readline  # NOQA
import util.argument as arg
from data_structure.page import Page
from data_structure.document import text_hash
from algorithm.algorithm_box import AlgorithmBox

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # defaults
    QUERY = 'test case'
    ALGORITHM = 'bag_of_words'
    # ALGORITHM = 'vector_space'
    # ALGORITHM = 'binary_independence'
    RESULTS = 20
    DOCUMENT = ''

    # get input arguments
    query = arg.get_argv('q', QUERY)
    algorithm_name = arg.get_argv('a', ALGORITHM)
    number_of_results = int(arg.get_argv('n', RESULTS))

    # load local files
    # files_path = 'test-small/subset'
    files_path = '20news-18828/alt.atheism'
    # files_path = '20news-18828'
    logger.info('Loading files...')
    files = parser.parse(files_path, 'iso-8859-1')
    logger.info('Files from %s are loaded.' % files_path)

    # create algorithm box object (context object)
    algorithm_box = AlgorithmBox()
    algorithm_box.files = files

    # execute algorithm
    page = Page(0, number_of_results)
    algorithm = algorithm_box.algorithm(algorithm_name)
    rank = algorithm.run(query, page)
    print()
    logger.info("Result: %s" % rank)
    print()

    print()
    print('---- MANUAL ----------')
    print('-q "query" DEFAULT: "test case"')
    print('-a "algorithm" -> bag_of_words, vector_space, binary_independence')
    print('                  DEFAULT: bag_of_words')
    print('-n "number of results" DEFAULT: 20')
    print('-d "new document" DEFAULT: ""')
    print('-e exit')
    print('----------------------')
    print()

    # if -d exists its priority is the higest one
    # so if -d exists the new document will be added
    # everything else will be ignored

    while True:
        command_line = shlex.split(input('Infinity > '))
        if '-e' in command_line:
            print("Bye!")
            break

        query = arg.get_cl(command_line, 'q', QUERY)
        algorithm_name = arg.get_cl(command_line, 'a', ALGORITHM)
        number = int(arg.get_cl(command_line, 'n', RESULTS))
        document = arg.get_cl(command_line, 'd', DOCUMENT)

        if document is not '':
            # TODO: replace with UUID
            document_hash = text_hash(document)
            files[document_hash] = document
            algorithm_box.append(document)
            logger.info('New document: key = %s, content = %s' %
                        (document_hash, document))
            continue

        # try to execute the algorithm
        try:
            page = Page(0, number)
            algorithm = algorithm_box.algorithm(algorithm_name)
            rank = algorithm.run(query, page)
            print()
            logger.info("Result: %s" % rank)
            print()
        except Exception as e:
            import traceback
            traceback.print_exc()
