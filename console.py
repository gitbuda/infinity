#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
import tokenizer
from document import create_doc_from_files

if __name__ == '__main__':
    files = parser.parse('20news-18828', 'iso-8859-1')
    documents = create_doc_from_files(files)
    documents = tokenizer.tokenize(documents)
    print(documents['20news-18828/comp.graphics/37930'].tokens)
