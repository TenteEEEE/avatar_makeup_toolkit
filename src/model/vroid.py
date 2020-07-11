from src.base_class import *
import numpy as np
from PIL import Image
from src.util import improc


class cheek_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        img = np.array(image)
        img[:, 1350:-1350] = np.roll(img[:, 1350:-1350], 250, axis=0)  # nose move
        img = Image.fromarray(img)
        return improc.resize(img, [.15, .15])


class eye_shadow_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        return improc.resize(image, [.21, .21])


class lip_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        return improc.resize(image, [.32, .32])


base_size = 1024
converters = {}
converters['cheek'] = cheek_converter(position=[250 / base_size, 550 / base_size])
converters['eye_shadow'] = eye_shadow_converter(position=[207 / base_size, 446 / base_size])
converters['lip'] = lip_converter(position=[417 / base_size, 737 / base_size])

img_loader = loader()
img_loader.set_components(converters.keys())


class patcher(patcher):
    def __init__(self, name='VRoid', base_tex='./avatar_texture/vroid/face.png', mask_tex=None, loader=img_loader, converters=converters, options=None):
        super().__init__(name, base_tex, mask_tex, loader, converters, options)
