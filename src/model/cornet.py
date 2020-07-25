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
class cheek_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.5, .5])


class eye_line_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        image = np.array(image)
        image = rotate(image, 5, resize=True)
        image = Image.fromarray(np.uint8(image * 255))
        return improc.resize(image, [.55, .5])


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
        image = rotate(image, 5, resize=True)
        image = Image.fromarray(np.uint8(image * 255))
        return improc.resize(image, [.5, .5])


class lip_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.7, .7])


basesize = 2048
patchers = dict.fromkeys(['face'])
patchers['face'] = {
    'cheek': [patcher(loader('cheek'), cheek_converter(), [150, 1100], basesize=basesize)],
    'eye_line': [patcher(loader('eye_line'), eye_line_converter(), [486, 72], basesize=basesize)],
    'eye_shadow': [patcher(loader('eye_shadow'), eye_shadow_converter(), [301, 911], basesize=basesize)],
    'eye_brow': [patcher(loader('eye_brow'), eye_brow_converter(), [434, -38], basesize=basesize)],
    'lip': [patcher(loader('lip'), lip_converter(), [816, 1499], basesize=basesize)],
}

manager = model_manager(model='cornet', displayname='コルネット', patchers=patchers, options={})
