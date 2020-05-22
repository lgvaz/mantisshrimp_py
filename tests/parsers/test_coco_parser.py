import pytest
from mantisshrimp.imports import Path,json,plt
from mantisshrimp import *

source = Path('../samples')
@pytest.fixture
def annots_dict(): return json.loads((source/'annotations.json').read())

def test_image_info(annots_dict):
    ainfo = annots_dict['images'][0]
    info = ImageInfo(ainfo['id'], ainfo['file_name'], ainfo['height'], ainfo['width'], 0)
    assert info == ImageInfo(128372, filepath='000000128372.jpg', h=427, w=640, split=0)

def test_info_parser(annots_dict):
    parser = COCOInfoParser(annots_dict['images'], source=source)
    infos = parser.parse()
    assert len(infos) == 6
    assert infos[0] == ImageInfo(0, filepath=source/'000000128372.jpg', h=427, w=640, split=0)

def test_category_parser(annots_dict):
    catparser = COCOCategoryParser(annots_dict['categories'])
    catmap = catparser.parse()
    assert catmap.cats[0].name == 'background'
    assert len(catmap) == 81
    assert catmap.cats[1:] == [Category(o['id'], o['name']) for o in annots_dict['categories']]

def test_coco_annotation_parser(annots_dict):
    catmap = COCOCategoryParser(annots_dict['categories']).parse()
    annotparser = COCOAnnotationParser(annots_dict['annotations'], source/'images', catmap)
    annots = annotparser.parse()
    annot = annots[0]
    assert len(annots) == 5
    assert annot.imageid == 0
    assert annot.labels == [4]

def test_coco_parser(annots_dict):
    parser = COCOParser(annots_dict, source/'images')
    with np_local_seed(42): train_rs,valid_rs = parser.parse()
    r = train_rs[0]
    assert len(train_rs)+len(valid_rs) == 5
    assert (r.info.h, r.info.w) == (427, 640)
    assert r.info.imageid == 0
    assert r.annot[0].bbox.xywh, [0.0, 73.89, 416.44, 305.13]
    assert str(r.info.filepath) == '../samples/images/000000128372.jpg'

def test_show_record(annots_dict, monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    parser = COCOParser(annots_dict, source / 'images')
    with np_local_seed(42): train_rs, valid_rs = parser.parse()
    r = train_rs[0]
    show_record(r)

