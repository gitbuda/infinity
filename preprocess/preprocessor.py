# -*- coding: utf-8 -*-

'''
Main function in the preprocessing.

TODO: integrate pro tokenizer and/or lematizer.
'''

from preprocess.bager import bag_of_words
from preprocess.tokenizer import tokenize_documents
from data_structure.document import create_docs_from_files


def preprocess(raw_files):
    '''
    Procedure:
        1. create document object
        2. tokenize
        3. create bad of words
        4. remove empty documents
    '''
    documents = create_docs_from_files(raw_files)
    documents = tokenize_documents(documents)
    documents = bag_of_words(documents)

    return documents
