# -*- coding: utf-8 -*-


class Document(object):
    '''
    '''
    def __init__(self):
        self.text = ""
        self.identifier = ""
        self.content_hash = ""
        self.tokens = []
        self.parsed = None
        self.bag = {}


def create_doc(filepath, filecontent):
    '''
    '''
    document = Document()

    document.text = filecontent
    document.content_hash = hash(filecontent)

    return document


def create_doc_from_files(files):
    '''
    '''
    documents = {}
    for key, content in files.items():
        document = create_doc(key, content)
        documents[key] = document
    return documents


if __name__ == '__main__':
    pass
