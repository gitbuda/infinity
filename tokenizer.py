# -*- coding: utf-8 -*-

import re

special = '[><!@#$%^&*?_~-£():.,"`]'
spacer = lambda x: re.sub(special, ' ', x.lower())
cleaner = lambda x: re.sub(special, '', x.lower())


def tokenize(documents):
    '''
    '''
    assert isinstance(documents, dict)

    for key, document in documents.items():
        text = spacer(document.text)
        tokens = list(filter(None, map(cleaner, text.split())))
        tokens = list(filter(lambda x: len(x) < 25, tokens))
        pattern = '^[a-z0-9]*$'
        tokens = list(filter(lambda x: re.search(pattern, x), tokens))
        document.tokens = tokens

    return documents

if __name__ == '__main__':
    pass
