__all__ = ['sample_category_parser', 'sample_info_parser', 'sample_annotation_parser', 'sample_data_parser']

from mantisshrimp.all import *

source = Path(__file__).absolute().parent.parent.parent/'samples'
annots_dict = json.loads((source/'annotations.json').read())

def sample_category_parser():
    return COCOCategoryParser(annots_dict['categories'])

def sample_info_parser():
    return COCOInfoParser(annots_dict['images'], source=source)

def sample_annotation_parser():
    catmap = sample_category_parser().parse()
    return COCOAnnotationParser(annots_dict['annotations'], source/'images', catmap)

def sample_data_parser():
    return COCOParser(annots_dict, source/'images')
