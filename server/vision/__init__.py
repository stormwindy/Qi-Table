# REPLACE THESE STUB METHODS WITH SIMILARLY IMPORTABLE LIVE METHODS
from ...base import Rectangle
from wirepickle.server import expose, Server

class CameraHandler():
    @expose('initialize_cams')
    def initialize_cams(self):
        return

    @expose('get_current_layout')
    def get_current_layout(self):
        return []

if __name__ == '__main__':
    instance = CameraHandler()
    
    Server(instance).listen('tcp://*:42069')
