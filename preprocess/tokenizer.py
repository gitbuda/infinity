# -*- coding: utf-8 -*-

'''
Tokenize text. Remove special characters: [><!@#$%^&*?_~-£():.,"`]

Stemmer used for this task is Snowball (Porter2) stemmer, because it
is less aggressive than Lancaster stemmer and faster than
Porter stemmer.
'''

import re
from stemming.porter2 import stem

special = '[><!@#$%^&*?_~-£():.,"`]'
spacer = lambda x: re.sub(special, ' ', x.lower())
cleaner = lambda x: re.sub(special, '', x.lower())


def tokenize_text(text):
    '''
    Converts text to list of tokens. General idea
    is to remove special characters and run stemming algorithm.

    Args:
        text: raw text

    Returns:
        list of tokens
    '''
    # replace special characters with space
    text = spacer(text)
    # split and replace special characters with ''
    tokens = list(filter(None, map(cleaner, text.split())))
    # remove too big words
    tokens = list(filter(lambda x: len(x) < 25, tokens))
    pattern = '^[a-z0-9]*$'
    # leave only words containing chars and numbers
    tokens = list(filter(lambda x: re.search(pattern, x), tokens))
    # stem algorithm
    tokens = list(map(lambda x: stem(x), tokens))

    return tokens


def tokenize_documents(documents):
    '''
    For each document creates list of tokens.
    For each document defines order number (index).
    Deletes documents that have empty list of tokens.

    Args:
        documents: dict of documents

    Returns:
        documents: dict of documents with the tokenization
        and empty documents are removed from input dictionary
    '''
    assert isinstance(documents, dict)

    valid_documents = {}

    index = 0
    for doc_key, document in documents.items():
        tokens = tokenize_text(document.text)
        if not tokens:
            continue
        document.index = index
        index += 1
        document.tokens = tokens
        valid_documents[doc_key] = document

    return valid_documents
