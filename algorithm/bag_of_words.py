# -*- coding: utf-8 -*-

'''
Information Retrieval Algorithm: Bag of words

A document is higher in the ranking table if it
contains more occurances of specific term.
Each document is observed separately.

Normalization TODO: write comment
'''

# from util.timeit import timeit
from data_structure.page import Page
from preprocess.bager import bag_of_documents
from preprocess.tokenizer import tokenize_text
from preprocess.preprocessor import preprocess


class IRAlgorithm:

    def configure(self, config=None):
        '''
        No configuration.
        '''
        pass

    # @timeit
    def process(self, raw_files):
        '''
        Converts the raw files into the documents.
        For each document create tokens and bag of words.

        Args:
            raw_files: dictionary[document_key] = document_content
        '''
        self.documents = preprocess(raw_files)
        self.docs_bag = bag_of_documents(self.documents)

    # @timeit
    def run(self, query, page=Page(0, 20)):
        '''
        1. query is tokenized
        2. for each token get normalized score for each document where
           it is
        3. sum all normalized scores

        Why normalization:
        E.g. let say that query is "test", document "Test one more time."
        is more relevant than document "Test one more time because something
        could went wrong."
        '''
        tokens = tokenize_text(query)
        if len(tokens) <= 0:
            return []

        data = {}
        for token in tokens:
            if token not in self.docs_bag:
                continue
            docs_bag_item = self.docs_bag[token]
            for doc_key, token_occurrence in docs_bag_item.items():
                doc_size = len(self.documents[doc_key].tokens)
                if doc_size <= 0:
                    normalized = 0
                else:
                    normalized = token_occurrence / doc_size
                data[doc_key] = data.get(doc_key, 0) + normalized
        data = sorted(data, key=lambda x: x[1], reverse=True)

        return data[page.start_index:page.end_index]
