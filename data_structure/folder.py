# -*- coding: utf-8 -*-

'''
The instance of Folder class contains a set
of documents.

Symbols:
    D   -> all documents inside the folder
    t   -> term
    idf -> inverse document frequency
'''


class Folder:
    def __init__(self):

        # all documents inside the folder
        self.documents = None

        # idf vector
        #
        # one element of vector is:
        # idf(t_i,D) = log(|D| / |{d elem D | t_i elem D_j}|)
        #
        self.idf = None
