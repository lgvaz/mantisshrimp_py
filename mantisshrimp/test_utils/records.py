__all__ = ['sample_category_parser', 'sample_info_parser', 'sample_annotation_parser', 'sample_data_parser',
           'sample_records', 'sample_datasets']

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

def sample_records():
    with np_local_seed(42):
        return sample_data_parser().parse(show_pbar=False)

def sample_datasets():
    train_rs, valid_rs = sample_records()
    return Dataset(train_rs), Dataset(valid_rs)

