try:
    from base_class import *
    from util import improc
except:  # Jupyter env
    from src.base_class import *
    from src.util import improc
import numpy as np
from PIL import Image


class cheek_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        img = np.array(image)
        img[:, 1350:-1350] = np.roll(img[:, 1350:-1350], 200, axis=0)  # nose move
        img = Image.fromarray(img)
        return improc.resize(img, [0.5, 0.5])


class eye_shadow_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        return improc.resize(image, [0.66, 0.7])


class eye_brow_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        return improc.resize(improc.mirror(image), [0.3, 0.8])


class lip_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        img = np.array(image)
        lip_u = img[:112, 100:300]
        lip_l = img[112:, 100:300]

        arrx = np.sin(np.linspace(0, np.pi / 2, 100) + np.pi / 8)**2 * 100 - 20
        arry = np.zeros(100)
        lip_u = improc.affine_transform(lip_u, arrx, arry)
        arrx = np.sin(np.linspace(0, 1, 100))**2 * 100 - 20
        lip_u = improc.affine_transform(np.rot90(lip_u), arrx, arry)
        lip_u = np.rot90(lip_u, -1)[:, 25:-18]

        arrx = np.sin(np.linspace(0, np.pi / 2, 100))**1 * -70
        arry = np.zeros(100)
        lip_l = improc.affine_transform(lip_l, arrx, arry)
        arrx = np.linspace(1, 0, 100)**3 * 80
        lip_l = improc.affine_transform(np.rot90(lip_l), arrx, arry)
        lip_l = np.rot90(lip_l, -1)

        img = np.concatenate([lip_u[:-20, :], lip_l[10:, 43:]], axis=0)
        img = improc.mirror(img, axis=1)
        img = Image.fromarray(np.uint8(img * 255))
        return improc.resize(img, [0.9, 0.6])


class eye_line_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        return improc.resize(image, [.7, 1.])


class eye_line_sub_converter(converter):
    def __init__(self, type='face', position=[.0, .0], options=[]):
        super().__init__(type, position, options)

    def convert(self, image):
        image = image.crop((300, 470, 500, 500))
        return improc.resize(image, [7.5, 3.2])


base_size = 4096
converters = {}
converters['cheek'] = cheek_converter(position=[303 / base_size, 678 / base_size])
converters['eye_line'] = [eye_line_converter(position=[2370 / base_size, 796 / base_size]),
                          eye_line_sub_converter(position=[3450 / base_size, 937 / base_size])]
converters['eye_shadow'] = eye_shadow_converter(position=[166 / base_size, 338 / base_size])
converters['eye_brow'] = eye_brow_converter(position=[3207 / base_size, 791 / base_size])
converters['lip'] = lip_converter(position=[1089 / base_size, 1244 / base_size])


img_loader = loader()
img_loader.set_components(converters.keys())


class patcher(patcher):
    def __init__(self, name='ルア', base_tex='./avatar_texture/lua/face.png', mask_tex='./avatar_texture/lua/face_mask.png', loader=img_loader, converters=converters, options=None):
        super().__init__(name, base_tex, mask_tex, loader, converters, options)
