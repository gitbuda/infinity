# -*- coding: utf-8 -*-

from data_structure.document import create_doc_from_files
from preprocess.tokenizer import tokenize
from preprocess.bager import bag

# Set up spaCy
# from spacy.en import English
# parser = English()
#
#
# def spacy_parse(documents):
#     '''
#     '''
#     for key, document in documents.items():
#         parsed_data = parser(document.text)
#         document.parsed = parsed_data
#
#     return documents


def preprocess(raw_files):
    '''
    1. create document object
    2. tokenize
    3. create bad of words
    '''
    documents = create_doc_from_files(raw_files)
    documents = tokenize(documents)
    documents = bag(documents)

    return documents
