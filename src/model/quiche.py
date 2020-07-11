from src.base_class import *
import numpy as np
from PIL import Image
from src.util import improc

# Converter definitions
class img_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        return improc.resize(image, [.5, .5])


base_size = 2048
converters = {}
converters['cheek'] = img_converter(position=[150 / base_size, 1100 / base_size])
converters['eye_brow'] = img_converter(position=[475 / base_size, 0 / base_size])
converters['eye_line'] = img_converter(position=[475 / base_size, 117 / base_size])
converters['eye_shadow'] = img_converter(position=[300 / base_size, 893 / base_size])
converters['lip'] = img_converter(position=[875 / base_size, 1550 / base_size])

# Image loader definitions
img_loader = loader()
img_loader.set_components(converters.keys())

# Patcher definitions
class patcher(patcher):
    def __init__(self, name='キッシュ', base_tex='./avatar_texture/quiche/face.png', mask_tex=None, loader=img_loader, converters=converters, options=None):
        super().__init__(name, base_tex, mask_tex, loader, converters, options)
