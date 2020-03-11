#! /usr/bin/env python

import math
from wirepickle.server import Server, expose
from wirepickle.client import Client

VISION_URI = 'tcp://127.0.0.1:65500'
PATH_CALCULATION_FREQ = 15 # every N ticks

class QiTable:
    __tick_count     = 0
    __desired_layout = None
    __paths          = None
    __pathfinder     = None
    __executor       = None

    def __init__(self):
        # some setup
        self.vision = Client(VISION_URI)
        self.__tick_count = 0
        
        self.__executor = None # TODO: load execution engine

    @expose('get_elapsed_ticks')
    def get_elapsed_ticks(self):
        return self.__tick_count;

    @expose('begin_navigation')
    def begin_navigation(self, layout):
        self.__tick_count = 0
        self.__desired_layout = layout
        self.__pathfinder = None # TODO: load a real pathfinder
        # TODO: some other shit here
        pass

    @expose('get_next_step')
    def get_next_step(self):
        # figure out where our tables are
        positions = self.vision.locate();
        
        # see if we need to recalculate the paths
        if self.__tick_count % PATH_CALCULATION_FREQ == 0:
            self.__paths = self.__pathfinder.pathfind(positions, layout);
        
        # execution
        if not self.__executor.execute(self.__paths):
            print('something is WRONG')
        else:
            self.__paths.advance()


if __name__ == '__main__':
    qi = QiTable()

    serv = Server(qi)
    serv.listen('tcp://*:42069')

