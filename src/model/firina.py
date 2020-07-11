from src.base_class import *
import numpy as np
from PIL import Image
from src.util import improc
from skimage.transform import rotate


class cheek_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        img = np.array(image)
        img[:, 1350:-1350] = np.roll(img[:, 1350:-1350], 200, axis=0)  # nose move
        img = Image.fromarray(img)
        return improc.resize(img, [0.7, 0.7])


class eye_shadow_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        return improc.resize(image, [0.82, 0.82])


class eye_line_converter(converter):
    def __init__(self, position=[.0, .0], mask_tex='./avatar_texture/firina/eye_line_mask.png', options=[]):
        super().__init__(position, options)
        self.mask_tex = mask_tex

    def convert(self, image):
        mask = Image.open(self.mask_tex)
        image = improc.resize(image, [.66, 1.07])
        image = np.array(image)
        image = rotate(image, -5, resize=True)
        image = Image.fromarray(np.uint8(image * 255))
        image = improc.masking(image, mask)
        return image


class eye_brow_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        return improc.resize(image, [1., .86])


class lip_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        img = np.array(image)
        lip_u = img[:112, 100:300]
        arrx = np.sin(np.linspace(0, np.pi / 2, 100) + np.pi / 8)**2 * 80 - 20
        arrx[-20:] += np.sin(np.linspace(0, np.pi / 2, 20)) * 10
        arry = np.zeros(100)
        lip_u = improc.affine_transform_by_arr(lip_u, arrx, arry)
        arrx = np.sin(np.linspace(0, 1, 100))**4 * 150 - 20
        lip_u = improc.affine_transform_by_arr(np.rot90(lip_u), arrx, arry)
        lip_u = np.rot90(lip_u, -1)
        lip_u = improc.resize(lip_u[20:103, 25:-22], [1.25, 1.25])
        lip_u = np.uint8(lip_u * 255)

        lip_l = img[112:, 100:300]
        arrx = np.sin(np.linspace(0, np.pi / 2, 100))**1 * -70
        arry = np.zeros(100)
        lip_l = improc.affine_transform_by_arr(lip_l, arrx, arry)
        arrx = np.linspace(1, 0, 100)**3 * 80
        lip_l = improc.affine_transform_by_arr(np.rot90(lip_l), arrx, arry)
        lip_l = np.rot90(lip_l, -1)
        lip_l = improc.resize(lip_l[5:, 50:-5], [1.05, 1.25])
        lip_l = np.uint8(lip_l * 255)

        img = np.concatenate([lip_u[:, 10:-1], lip_l[:, :-1]], axis=0)
        img = improc.mirror(img, axis=1)
        return improc.resize(Image.fromarray(img), [0.92, 1.])


class eye_line_sub_converter(converter):
    def __init__(self, position=[.0, .0], options=[]):
        super().__init__(position, options)

    def convert(self, image):
        image = image.crop((300, 470, 500, 500))
        return improc.resize(image, [4.3, 4.3])


base_size = 4096
converters = {}
converters['cheek'] = cheek_converter(position=[823 / base_size, 2485 / base_size])
converters['eye_shadow'] = eye_shadow_converter(position=[860 / base_size, 2073 / base_size])
converters['eye_brow'] = eye_brow_converter(position=[2149 / base_size, 692 / base_size])
converters['eye_line'] = [eye_line_converter(position=[981 / base_size, 206 / base_size]),
                          eye_line_sub_converter(position=[1129 / base_size, 110 / base_size])]
converters['lip'] = lip_converter(position=[1868 / base_size, 3183 / base_size])


img_loader = loader()
img_loader.set_components(converters.keys())


class patcher(patcher):
    def __init__(self, name='フィリナ', base_tex='./avatar_texture/firina/face.png', mask_tex='./avatar_texture/firina/face_mask.png', loader=img_loader, converters=converters, options=None):
        super().__init__(name, base_tex, mask_tex, loader, converters, options)
