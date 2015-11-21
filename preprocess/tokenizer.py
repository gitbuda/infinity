# -*- coding: utf-8 -*-

import re

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
    return tokens


def tokenize_documents(documents):
    '''
    '''
    assert isinstance(documents, dict)

    for doc_key, document in documents.items():
        document.tokens = tokenize_text(document.text)

    return documents

if __name__ == '__main__':
    pass
