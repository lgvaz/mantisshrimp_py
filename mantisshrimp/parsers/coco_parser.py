__all__ = ['COCOInfoParser', 'COCOAnnotationParser', 'COCOCategoryParser']

from ..core import *
from .info_parser import *
from .annotation_parser import *
from .category_parser import *

class COCOInfoParser(InfoParser):
    def imageid(self, o): return o['id']
    def filepath(self, o): return self.source/o['file_name']
    def h(self, o): return o['height']
    def w(self, o): return o['width']

class COCOAnnotationParser(AnnotationParser):
    def imageid(self, o):  return o['image_id']
    def label(self, o): return o['category_id']
    def bbox(self, o): return BBox.from_xywh(*o['bbox'])
    def iscrowd(self, o): return o['iscrowd']
    def mask(self, o):
        seg = o['segmentation']
        if o['iscrowd']: return RLE.from_coco(seg['counts'])
        else:            return Polygon(seg)

class COCOCategoryParser(CategoryParser):
    def id(self, o): return o['id']
    def name(self, o): return o['name']

