# -*- coding: utf-8 -*-

'''
Main function in the preprocessing.

The purpose of preprocessing is to: convert raw
files into the Document objects, tokenize texts
and create bag of words.
'''

from preprocess.bager import bag_of_words
from preprocess.tokenizer import tokenize_documents
from data_structure.document import create_docs_from_files


def preprocess(raw_files):
    '''
    Procedure:
        1. create document objects
        2. tokenize
        3. remove empty documents
        4. create bad of words

    Args:
        raw_files: dict[identifier] = text

    Returns:
        dict of Documents
    '''
    documents = create_docs_from_files(raw_files)
    documents = tokenize_documents(documents)
    documents = bag_of_words(documents)

    return documents
