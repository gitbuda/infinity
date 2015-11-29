# -*- coding: utf-8 -*-

'''
Main function in the preprocessing.

The purpose of preprocessing is to: convert raw
files into the Document objects, tokenize texts
and create bag of words.
'''

from preprocess.bager import bag
from preprocess.bager import bag_of_words
from preprocess.tokenizer import tokenize_text
from preprocess.tokenizer import tokenize_documents
from data_structure.document import Document
from data_structure.document import text_hash
from data_structure.document import create_docs_from_files


def preprocess_all(raw_files):
    '''
    Procedure:
        1. create document objects
        2. tokenize
        3. remove empty documents
        4. create bag of words

    Args:
        raw_files: dict[identifier] = text

    Returns:
        dict of Documents
    '''
    documents = create_docs_from_files(raw_files)
    documents = tokenize_documents(documents)
    documents = bag_of_words(documents)

    return documents


def preprocess_one(raw_file):
    '''
    Procedure:
        1. create document
        2. fill with the data

    Args:
        raw_file: text (string)

    Returns:
        Document
    '''
    document = Document()

    document.text = raw_file
    document.identifier = text_hash(raw_file)
    document.content_hash = document.identifier
    document.tokens = tokenize_text(raw_file)
    document.bag = bag(document.tokens)

    return document
