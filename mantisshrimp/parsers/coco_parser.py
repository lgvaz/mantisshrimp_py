__all__ = ['COCOInfoParser']

from .info_parser import *

class COCOInfoParser(InfoParser):
    def imageid(self, o): return o['id']
    def filepath(self, o): return self.source/o['file_name']
    def h(self, o): return o['height']
    def w(self, o): return o['width']
