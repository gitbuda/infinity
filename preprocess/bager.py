# -*- coding: utf-8 -*-

'''
Creates bag of words (for each document dictionary of
tokens occurance) and bag of documents (for each token
number of documents that contains the term).
'''


def bag_of_words(documents):
    '''
    For each document calculate the bag of words.

    Args:
        documents: dictionary[doc_key] = Document

    Returns:
        dictionary of Documents
    '''
    for doc_key, document in documents.items():
        for token in document.tokens:
            document.bag[token] = document.bag.get(token, 0) + 1
    return documents


def bag_of_documents(documents):
    '''
    For each term/token calculate the bag of documents.
    Equivalent to the bag of words.

    Args:
        documents: dictionary[doc_key] = Document

    Returns:
        dictionary of Documents
    '''
    terms = {}
    for doc_key, document in documents.items():
        for term, occurrences in document.bag.items():
            docs_number = terms.get(term, {})
            docs_number[doc_key] = occurrences
            terms[term] = docs_number
    return terms
