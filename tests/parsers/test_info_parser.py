from mantisshrimp.imports import *
from mantisshrimp.parsers import *

def test_image_info():
    annots = json.loads(Path('../../sampels/annotations.json').read())
    ainfo = annots['images'][0]
    info = ImageInfo(ainfo['id'], ainfo['file_name'], ainfo['height'], ainfo['width'], 0)
    expect = ImageInfo(128372, filepath='000000128372.jpg', h=427, w=640, split=0)
    assert info == expect
