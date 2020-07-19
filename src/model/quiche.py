try:
    from base_class import *
    from util import improc
except:  # Jupyter env
    from src.base_class import *
    from src.util import improc
import numpy as np
from PIL import Image


class img_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.5, .5])


basesize = 2048
patchers = dict.fromkeys(['face'])
patchers['face'] = {
    'cheek': [patcher(loader('cheek'), img_converter(), [150, 1100], basesize=basesize)],
    'eye_brow': [patcher(loader('eye_brow'), img_converter(), [475, 0], basesize=basesize)],
    'eye_line': [patcher(loader('eye_line'), img_converter(), [475, 117], basesize=basesize)],
    'eye_shadow': [patcher(loader('eye_shadow'), img_converter(), [300, 893], basesize=basesize)],
    'lip': [patcher(loader('lip'), img_converter(), [875, 1550], basesize=basesize)],
}

manager = model_manager(model='quiche', displayname='キッシュ', patchers=patchers, options={})
