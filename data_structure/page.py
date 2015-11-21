# -*- coding: utf-8 -*-


class Page(object):
    '''
    '''
    def __init__(self, page_num, page_size):
        '''
        '''
        self.start_index = page_num * page_size
        self.end_index = self.start_index + page_size

    # data encapsulation
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
