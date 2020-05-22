__all__ = ['show_record']

from ..utils import *
from .show_annotation import *

def show_record(r, label=True, bbox=True, mask=True, catmap=None, ax=None):
    im = open_img(r.iinfo.fp)
    h,w,_ = im.shape
    names = [catmap.i2o[i].name for i in r.annot.oids] if notnone(catmap) else r.annot.oids
    return show_annotation(im, ax=ax,
                      labels=names if label else None,
                      bboxes=r.annot.bboxes if bbox else None,
                      masks=r.annot.get_mask(h,w) if mask else None)
