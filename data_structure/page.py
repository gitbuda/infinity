# -*- coding: utf-8 -*-

'''
Results from any kind of query or search have to be
paged because if there is, let's say 1M result objects,
the client doesn't want to see them all at once for sure.

Via object of this class client can define the range of
results which will be returned.
'''


class Page(object):

    def __init__(self, page_num, page_size):
        '''
        A page is defined with page number and page size.

        Range is calculated as follows:
            [page_num * page_size : page_num * page_size + page_size]
                         ^                          ^
                         |                          |
                    start index                 end index

        Args:
            page_num: ordinal number of page (starts with 0)
            page_size: number of entities within one page
        '''
        self.start_index = page_num * page_size
        self.end_index = self.start_index + page_size

    @property
    def start_index(self):
        return self.__start_index

    @start_index.setter
    def start_index(self, value):
        self.__start_index = value

    @property
    def end_index(self):
        return self.__end_index

    @end_index.setter
    def end_index(self, value):
        self.__end_index = value
