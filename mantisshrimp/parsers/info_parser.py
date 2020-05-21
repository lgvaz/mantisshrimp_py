__all__ = ['ImageInfo', 'InfoParser']

from ..imports import *
from ..utils import *
from ..core import *
from .splits import *

@dataclass(frozen=True)
class ImageInfo:
    imageid: int
    filepath: Union[str, Path]
    h: int
    w: int
    split: int = 0

    def __post_init__(self): super().__setattr__('filepath', self.filepath)


class InfoParser:
    def __init__(self, data, source=None, idmap=None):
        self.data, self.source = data, Path(source or '.')
        self.idmap = idmap or IDMap()

    def __iter__(self): yield from self.data
    def __len__(self):  return len(self.data)

    def prepare(self, o): pass
    def imageid(self, o): raise NotImplementedError
    def filepath(self, o): raise NotImplementedError
    def h(self, o): raise NotImplementedError
    def w(self, o): raise NotImplementedError
    def split(self, o): return random_split()

    def parse(self):
        xs,imageids = [],[]
        for o in tqdm(self):
            self.prepare(o)
            imageid = self.idmap[self.imageid(o)]
            if imageid not in imageids:
                imageids.append(imageid)
                xs.append(ImageInfo(imageid=imageid, filepath=self.filepath(o),
                                    split=self.split(o), h=self.h(o), w=self.w(o)))
        return xs

