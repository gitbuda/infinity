# -*- coding: utf-8 -*-

from preprocess.bager import bag_of_words
from preprocess.tokenizer import tokenize_documents
from data_structure.document import create_docs_from_files

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
    documents = create_docs_from_files(raw_files)
    documents = tokenize_documents(documents)
    documents = bag_of_words(documents)

    return documents
