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
        image = np.array(image)
        image[:, 1350:-1350] = np.roll(image[:, 1350:-1350], 100, axis=0)  # nose move
        image = Image.fromarray(image)
        return improc.resize(image, [.25, .25])


class eye_shadown_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        image = np.array(image)
        [r, c, d] = image.shape
        image = image[:, :int(c / 2)]
        arrx = np.sin(np.linspace(0, np.pi / 2, 36))**2 * 150
        arry = np.zeros(36)
        image = improc.affine_transform(image, arrx, arry)
        image = Image.fromarray(np.uint8(image * 255))
        image = improc.mirror(image, axis=1)
        return improc.resize(image, [.32, .38])


class lip_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.25, .25])


class eye_line_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)
        self.mask_tex = './avatar_texture/rearalice/eye_line_mask.png'

    def convert(self, image):
        mask = Image.open(self.mask_tex)
        image = np.array(image)
        image = improc.resize(improc.rotate(image, 37.2), [.76, .76])
        image = Image.fromarray(np.uint8(image * 255))
        image = improc.masking(image, mask)
        return image


class eye_brow_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [.35, .35])


basesize = 4096
patchers = dict.fromkeys(['face'])
patchers['face'] = {
    'cheek': [patcher(loader('cheek'), cheek_converter(), [791, 1010], basesize=basesize)],
    'eye_brow': [patcher(loader('eye_brow'), eye_brow_converter(), [1573, 3327], basesize=basesize)],
    'eye_line': [patcher(loader('eye_line'), eye_line_converter(), [1440, 2553], basesize=basesize)],
    'eye_shadow': [patcher(loader('eye_shadow'), eye_shadown_converter(), [685, 878], basesize=basesize)],
    'lip': [patcher(loader('lip'), lip_converter(), [1161, 1284], basesize=basesize)],
}

manager = model_manager(model='rearalice', displayname='リアアリス', patchers=patchers, options={})
