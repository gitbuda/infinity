# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Bag of words

A document is higher in the ranking table if it
contains more occurances of specific term.
Each document is observed separately.
'''

from util.timeit import timeit
from data_structure.page import Page
from preprocess.preprocessor import preprocess
from preprocess.bager import bag_of_documents
# from heapq import heappop, heappush


class IRAlgorithm:

    def configure(self, config=None):
        pass

    def process(self, raw_files):
        '''
        Converts the raw files into the documents.
        For each document create tokens and bag of words.

        Args:
            raw_files: dictionary[document_key] = document_content
        '''
        self.documents = preprocess(raw_files)
        self.docs_bag = bag_of_documents(self.documents)

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        '''
        # TODO: query should be logical statement

        # # implementation 1
        # docs = []
        # for key, document in self.documents.items():
        #     score = document.bag.get(query, 0)
        #     docs.append((key, score))
        # docs = sorted(docs, key=lambda x: x[1], reverse=True)
        # return docs

        # # implementation 2
        # heap = []
        # for key, document in self.documents.items():
        #     score = document.bag.get(query, 0)
        #     heappush(heap, (-score, key))

        # # clear element from beginning
        # for i in range(start_page):
        #     heappop(heap)

        # # take page elements
        # data = []
        # for i in range(start_page, end_page):
        #     data.append(heappop(heap))

        # return data

        # # implementation 3
        docs_bag_item = self.docs_bag[query]
        data = []
        for key, bag_item in docs_bag_item.items():
            data.append((key, bag_item))
        data = sorted(data, key=lambda x: x[1], reverse=True)

        return data[page.start_index:page.end_index]
