# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Bag of words

A document is higher in the ranking table if it
contains more occurances of specific term.
Each document is observed separately.
'''

from util.timeit import timeit
# from heapq import heappop, heappush
from preprocess.preprocessor import preprocess


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
        self.terms = {}
        for key, document in self.documents.items():
            for term, no in document.bag.items():
                docs_no = self.terms.get(term, {})
                docs_no[key] = no
                self.terms[term] = docs_no

    @timeit
    def run(self, query, page_num=0, page_size=20):
        '''
        '''
        start_page = page_num * page_size
        end_page = start_page + page_size

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
        docs_bag_item = self.terms[query]
        data = []
        for key, bag_item in docs_bag_item.items():
            data.append((key, bag_item))
        data = sorted(data, key=lambda x: x[1], reverse=True)

        return data[start_page:end_page]
