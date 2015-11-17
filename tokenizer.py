# -*- coding: utf-8 -*-


def tokenize(documents):
    '''
    '''
    assert isinstance(documents, dict)

    for key, document in documents.items():
        tokens = document.text.split()
        document.tokens = tokens

    return documents

if __name__ == '__main__':
    pass
