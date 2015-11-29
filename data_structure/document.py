# -*- coding: utf-8 -*-

'''
Document object.

Each document has: text, unique identifer, content hash,
list of tokens and bag of words (dict[token] = number of occurrences).
'''

import hashlib


class Document(object):

    def __init__(self):
        self.text = ""
        self.identifier = ""
        self.content_hash = ""
        self.tokens = []
        self.bag = {}


def text_hash(text):
    '''
    Returns hash from text. In the current implementation
    hash algorithm is SHA1. Two reasons for that exist:
    1. for the same text hash has to be the same
    2. for different texts hashes have to be different
       (with the SHA1 algorithm probability that 2 different texts will
       have the same hash is really, REALLY small)
       e.g GIT uses the same principle

    Args:
        text: string represents a document

    Returns:
        hash: SHA1 hash of text
    '''
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


def create_doc(identifier, text):
    '''
    Create the Document object.

    Args:
        identifier: document identifier
        text: document text

    Returns:
        Document object
    '''
    document = Document()

    document.identifier = identifier
    document.text = text
    document.content_hash = text_hash(text)

    return document


def create_docs_from_files(files):
    '''
    Creates dictionary of documents.

    Args:
        files: dict[file_path] = text

    Returns:
        dict of Documents
    '''
    documents = {}

    for file_path, content in files.items():
        document = create_doc(file_path, content)
        documents[file_path] = document

    return documents
