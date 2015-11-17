# -*- coding: utf-8 -*-

import re

special = '[><!@#$%^&*?_~-£():.]'
cleaner = lambda x: re.sub(special, '', x.lower())


def tokenize(documents):
    '''
    '''
    assert isinstance(documents, dict)

    for key, document in documents.items():
        tokens = list(filter(None, map(cleaner, document.text.split())))
        document.tokens = tokens

    return documents

if __name__ == '__main__':
    pass
