import pytest
from mantisshrimp.imports import Path,json
from mantisshrimp.parsers import *

source = Path('../samples/annotations.json')
@pytest.fixture
def annots(): return json.loads(source.read())

def test_image_info(annots):
    ainfo = annots['images'][0]
    info = ImageInfo(ainfo['id'], ainfo['file_name'], ainfo['height'], ainfo['width'], 0)
    assert info == ImageInfo(128372, filepath='000000128372.jpg', h=427, w=640, split=0)

def test_info_parser(annots):
    parser = COCOInfoParser(annots['images'], source=source)
    infos = parser.parse()
    assert len(infos) == 6
    assert infos[0] == ImageInfo(0, filepath=source/'000000128372.jpg', h=427, w=640, split=0)
