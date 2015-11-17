# -*- coding: utf-8 -*-

# Set up spaCy
from spacy.en import English
parser = English()


def spacy_parse(documents):
    '''
    '''
    for key, document in documents.items():
        parsed_data = parser(document.text)
        document.parsed = parsed_data

    return documents

if __name__ == '__main__':
    pass
