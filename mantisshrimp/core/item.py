__all__ = ['Item']

from ..imports import *
from ..utils import *
from .bbox import *
from .mask import *

@dataclass
class Item:
    img: np.ndarray
    iid: int
    labels: List[int]
    iscrowds: List[int]
    bboxes: List[BBox] = None
    masks: MaskArray = None

    #     keypoints: #TODO
    @classmethod
    def from_record(cls, r):
        return cls(
            img=open_img(r.iinfo.fp),
            iid=r.iinfo.iid,
            labels=r.annot.oids,
            iscrowds=r.annot.iscrowds,
            bboxes=r.annot.bboxes,
            masks=MaskArray.from_segs(r.annot.segs, r.iinfo.h, r.iinfo.w) if r.annot.segs else None,
            # keypoints: TODO
        )

    def asdict(self): return self.__dict__

    # TODO: This creates a copy, is that necessary?
    def replace(self, **kwargs): return dataclasses.replace(self, **kwargs)
