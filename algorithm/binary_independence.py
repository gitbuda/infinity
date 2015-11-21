# -*- coding: utf-8 -*-

from util.timeit import timeit
from data_structure.page import Page
from preprocess.bager import bag_of_documents
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess


class IRAlgorithm:
    '''
    '''
    def configure(self, config=None):
        '''
        '''
        pass

    @timeit
    def process(self, raw_files):
        '''
        '''
        self.documents = preprocess(raw_files)
        self.docs_no = len(self.documents)
        self.docs_bag = bag_of_documents(self.documents)

    @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        '''
        tokens = tokenize_text(query)
        if len(tokens) <= 0:
            return []

        results = []
        for doc_key, document in self.documents.items():
            result = 0
            for token in tokens:
                if token not in document.bag:
                    continue
                token_docs = self.docs_bag.get(token, {})
                token_docs_len = len(token_docs)
                if token_docs_len <= 0:
                    continue
                ratio = 1.0 * token_docs_len / self.docs_no
                if abs(ratio - 10e-6) < 0:
                    continue
                result += 0.5 / ratio
            if result > 0:
                results.append((doc_key, result))
        results = sorted(results, key=lambda x: x[1], reverse=True)

        return results[page.start_index:page.end_index]
