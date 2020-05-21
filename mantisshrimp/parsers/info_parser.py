__all__ = ['ImageInfo']

from ..imports import *
from ..utils import *
from ..core import *

@dataclass(frozen=True)
class ImageInfo:
    image_id: int
    filepath: Union[str, Path]
    h: int
    w: int
    split: int = 0

    def __post_init__(self): super().__setattr__('filepath', self.filepath)


source = Path('../../samples/')
annots = json.loads((source/'annotations.json').read())
annots.keys()
annots['images']
annot = annots['images'][0]

ImageInfo(annot['id'], annot['file_name'], annot['height'], annot['width'], 0)

