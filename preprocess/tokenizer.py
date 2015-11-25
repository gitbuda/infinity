# -*- coding: utf-8 -*-

'''
TODO: comment
'''

import re
from stemming.porter2 import stem

special = '[><!@#$%^&*?_~-£():.,"`]'
spacer = lambda x: re.sub(special, ' ', x.lower())
cleaner = lambda x: re.sub(special, '', x.lower())


def tokenize_text(text):
    '''
    '''
    text = spacer(text)
    tokens = list(filter(None, map(cleaner, text.split())))
    tokens = list(filter(lambda x: len(x) < 25, tokens))
    pattern = '^[a-z0-9]*$'
    tokens = list(filter(lambda x: re.search(pattern, x), tokens))
    tokens = list(map(lambda x: stem(x), tokens))
    return tokens


def tokenize_documents(documents):
    '''
    For each document create list of tokens.
    Remove documents with empty list of tokens.

    Args:
        documents: dict of documents
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
