#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
from document import create_doc_from_files
import tokenizer
import bager
import util.argument as arg

# import preprocessor
# # documents = preprocessor.spacy_parse(documents)


if __name__ == '__main__':

    query = arg.get('q', '')

    files = parser.parse('20news-18828', 'iso-8859-1')

    documents = create_doc_from_files(files)
    documents = tokenizer.tokenize(documents)
    documents = bager.bag(documents)

    order = []
    for key, document in documents.items():
        score = document.bag.get(query, 0)
        order.append((key, score))

    order = sorted(order, key=lambda x: x[1], reverse=True)

    print(order[:10])

    # document1 = documents['20news-18828/comp.graphics/37930']
    # document2 = documents['20news-18828/sci.med/58043']
    # print(document1.bag)
    # print(document2.bag)
