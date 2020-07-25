try:
    from base_class import *
    from util import improc
except:  # Jupyter env
    from src.base_class import *
    from src.util import improc
import numpy as np
from PIL import Image


class cheek_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        img = np.array(image)
        img[:, 1350:-1350] = np.roll(img[:, 1350:-1350], 250, axis=0)  # nose move
        img = Image.fromarray(img)
        return improc.resize(img, [.15, .15])


class eye_shadow_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.21, .21])


class lip_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.32, .32])


basesize = 1024
patchers = dict.fromkeys(['face'])
patchers['face'] = {
    'cheek': [patcher(loader('cheek'), cheek_converter(), [250, 550], basesize=basesize)],
    'eye_shadow': [patcher(loader('eye_shadow'), eye_shadow_converter(), [207, 446], basesize=basesize)],
    'lip': [patcher(loader('lip'), lip_converter(), [417, 737], basesize=basesize)],
}

manager = model_manager(model='vroid', displayname='VRoid', patchers=patchers, options={})
