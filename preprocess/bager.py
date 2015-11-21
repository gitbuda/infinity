# -*- coding: utf-8 -*-


def bag_of_words(documents):
    '''
    '''
    for doc_key, document in documents.items():
        for token in document.tokens:
            document.bag[token] = document.bag.get(token, 0) + 1
    return documents


def bag_of_documents(documents):
    '''
    '''
    terms = {}
    for doc_key, document in documents.items():
        for term, occurrences in document.bag.items():
            docs_number = terms.get(term, {})
            docs_number[doc_key] = occurrences
            terms[term] = docs_number
    return terms


if __name__ == '__main__':
    pass
