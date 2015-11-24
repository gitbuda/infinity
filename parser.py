# -*- coding: utf-8 -*-

import logging
import codecs
from os import walk, path
from preprocess.twenty_newsgroups import strip_newsgroup_header
from preprocess.twenty_newsgroups import strip_newsgroup_quoting
from preprocess.twenty_newsgroups import strip_newsgroup_footer

log = logging.getLogger(__name__)


def parse(folder_path, encoding):
    '''
    Each file under folder_path will be stored inside the
    dictionary as string. The key is relative file path
    and the value is file content.

    Args:
        folder_path: folder which contains all files
        encoding: encoding used for all files

    Returns:
        dictionary where key = file path
                         value = file content
    '''
    files = {}
    for (dirpath, dirnames, filenames) in walk(folder_path):
        for filename in filenames:
            filepath = path.join(dirpath, filename)
            with codecs.open(filepath, 'r', encoding) as f:
                filecontent = strip_newsgroup_header(f.read())
                filecontent = strip_newsgroup_quoting(filecontent)
                filecontent = strip_newsgroup_footer(filecontent)
            files[filepath] = filecontent
    log.info('Parser finished: %s documents' % len(files))
    return files


if __name__ == '__main__':

    files = parse('20news-18828', 'iso-8859-1')
    assert len(files) == 18828
