# -*- coding: utf-8 -*-

'''
Creates a bag of words (for each document dictionary of
tokens occurrence) and a bag of documents (for each token
number of documents that contains the term).
'''


def bag(tokens):
    '''
    Calculates single bag of words for the list of tokens.

    Args:
        tokens: list of tokens

    Returns:
        bag of words: dict[token] = number of occurrences
    '''
    bag = {}
    for token in tokens:
        bag[token] = bag.get(token, 0) + 1
    return bag


def bag_of_words(documents):
    '''
    For each document calculates the bag of words.

    Args:
        documents: dictionary[doc_key] = Document

    Returns:
        dictionary of Documents
    '''
    for doc_key, document in documents.items():
        document.bag = bag(document.tokens)

    return documents


def bag_of_documents(documents):
    '''
    For each term/token calculates the bag of documents.
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
