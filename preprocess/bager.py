# -*- coding: utf-8 -*-


def bag(documents):
    '''
    '''
    for key, document in documents.items():
        for token in document.tokens:
            document.bag[token] = document.bag.get(token, 0) + 1
    return documents


if __name__ == '__main__':
    pass
