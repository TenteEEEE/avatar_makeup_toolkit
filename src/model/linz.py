try:
    from base_class import *
    from util import improc
except:  # Jupyter env
    from src.base_class import *
    from src.util import improc
import numpy as np
from PIL import Image
from skimage.transform import rotate


# Converter definitions
class img_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.5, .5])


class eye_shadow_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.46, .5])


class eye_brow_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        image = np.array(image)
        image = rotate(image, 3, resize=True)
        image = Image.fromarray(np.uint8(image * 255))
        return improc.resize(image, [.5, .5])


class lip_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.53, .53])


basesize = 2048
patchers = dict.fromkeys(['face'])
patchers['face'] = {
    'cheek': [patcher(loader('cheek'), img_converter(), [150, 1100], basesize=basesize)],
    'eye_line': [patcher(loader('eye_line'), img_converter(), [475, 110], basesize=basesize)],
    'eye_shadow': [patcher(loader('eye_shadow'), eye_shadow_converter(), [301, 911], basesize=basesize)],
    'eye_brow': [patcher(loader('eye_brow'), eye_brow_converter(), [457, -14], basesize=basesize)],
    'lip': [patcher(loader('lip'), lip_converter(), [867, 1538], basesize=basesize)],
}

manager = model_manager(model='linz', displayname='リンツ', patchers=patchers, options={})
