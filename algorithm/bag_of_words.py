# -*- coding: utf-8 -*-

import bager
import tokenizer

from data_structure.document import create_doc_from_files


class IRAlgorithm:
    '''
    '''
    def configure(self, config=None):
        '''
        '''
        pass

    def process(self, raw_files):
        '''
        '''
        self.documents = create_doc_from_files(raw_files)
        self.documents = tokenizer.tokenize(self.documents)
        self.documents = bager.bag(self.documents)

    def run(self, query):
        '''
        '''
        order = []
        for key, document in self.documents.items():
            # TODO: query should be logical statement
            score = document.bag.get(query, 0)
            order.append((key, score))
        order = sorted(order, key=lambda x: x[1], reverse=True)
        return order
