# -*- coding: utf-8 -*-

'''
Document object.

Each document has: text, unique identifer, content hash,
list of tokens and bag of words (dict[token] = number of occurrences).
'''


class Document(object):

    def __init__(self):
        self.text = ""
        self.identifier = ""
        self.content_hash = ""
        self.tokens = []
        self.bag = {}


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
    document.content_hash = hash(text)

    return document


def create_docs_from_files(files):
    '''
    Create dictionary of documents.

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
