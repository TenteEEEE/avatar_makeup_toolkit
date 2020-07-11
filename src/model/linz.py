from src.base_class import *
import numpy as np
from PIL import Image
from src.util import improc
from skimage.transform import rotate

# Converter definitions
class img_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        return improc.resize(image, [.5, .5])


class eye_shadow_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        return improc.resize(image, [.46, .5])


class eye_brow_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        image = np.array(image)
        image = rotate(image, 3, resize=True)
        image = Image.fromarray(np.uint8(image * 255))
        return improc.resize(image, [.5, .5])


class lip_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        return improc.resize(image, [.53, .53])


base_size = 2048
converters = {}
converters['cheek'] = img_converter(position=[150 / base_size, 1100 / base_size])
converters['eye_line'] = img_converter(position=[475 / base_size, 110 / base_size])
converters['eye_shadow'] = eye_shadow_converter(position=[301 / base_size, 911 / base_size])
converters['eye_brow'] = eye_brow_converter(position=[457 / base_size, -14 / base_size])
converters['lip'] = lip_converter(position=[867 / base_size, 1538 / base_size])

# Image loader definitions
img_loader = loader()
img_loader.set_components(converters.keys())

# Patcher definitions
class patcher(patcher):
    def __init__(self, name='Linz', base_tex='./avatar_texture/linz/face.png', mask_tex=None, loader=img_loader, converters=converters, options=None):
        super().__init__(name, base_tex, mask_tex, loader, converters, options)
