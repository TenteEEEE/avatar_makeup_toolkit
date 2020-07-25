try:
    from base_class import *
    from util import improc
except:  # Jupyter env
    from src.base_class import *
    from src.util import improc
import numpy as np
from PIL import Image
from skimage.transform import rotate


class cheek_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        img = np.array(image)
        img[:, 1350:-1350] = np.roll(img[:, 1350:-1350], 200, axis=0)  # nose move
        img = Image.fromarray(img)
        return improc.resize(img, [0.7, 0.7])


class eye_shadow_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [0.82, 0.82])


class eye_line_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)
        self.mask_tex = './avatar_texture/firina/eye_line_mask.png'

    def convert(self, image):
        mask = Image.open(self.mask_tex)
        image = improc.resize(image, [.66, 1.07])
        image = np.array(image)
        image = rotate(image, -5, resize=True)
        image = Image.fromarray(np.uint8(image * 255))
        image = improc.masking(image, mask)
        return image


class eye_brow_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        return improc.resize(image, [1., .86])


class lip_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        img = np.array(image)
        lip_u = img[:112, 100:300]
        arrx = np.sin(np.linspace(0, np.pi / 2, 100) + np.pi / 8)**2 * 80 - 20
        arrx[-20:] += np.sin(np.linspace(0, np.pi / 2, 20)) * 10
        arry = np.zeros(100)
        lip_u = improc.affine_transform(lip_u, arrx, arry)
        arrx = np.sin(np.linspace(0, 1, 100))**4 * 150 - 20
        lip_u = improc.affine_transform(np.rot90(lip_u), arrx, arry)
        lip_u = np.rot90(lip_u, -1)
        lip_u = improc.resize(lip_u[20:103, 25:-22], [1.25, 1.25])
        lip_u = np.uint8(lip_u * 255)

        lip_l = img[112:, 100:300]
        arrx = np.sin(np.linspace(0, np.pi / 2, 100))**1 * -70
        arry = np.zeros(100)
        lip_l = improc.affine_transform(lip_l, arrx, arry)
        arrx = np.linspace(1, 0, 100)**3 * 80
        lip_l = improc.affine_transform(np.rot90(lip_l), arrx, arry)
        lip_l = np.rot90(lip_l, -1)
        lip_l = improc.resize(lip_l[5:, 50:-5], [1.05, 1.25])
        lip_l = np.uint8(lip_l * 255)

        img = np.concatenate([lip_u[:, 10:-1], lip_l[:, :-1]], axis=0)
        img = improc.mirror(img, axis=1)
        return improc.resize(Image.fromarray(img), [0.92, 1.])


class eye_line_sub_converter(converter):
    def __init__(self, options=[]):
        super().__init__(options)

    def convert(self, image):
        image = image.crop((300, 470, 500, 500))
        return improc.resize(image, [4.3, 4.3])


basesize = 4096
patchers = dict.fromkeys(['face'])
patchers['face'] = {
    'cheek': [patcher(loader('cheek'), cheek_converter(), [823, 2485], basesize=basesize)],
    'eye_shadow': [patcher(loader('eye_shadow'), eye_shadow_converter(), [860, 2073], basesize=basesize)],
    'eye_brow': [patcher(loader('eye_brow'), eye_brow_converter(), [2149, 692], basesize=basesize)],
    'eye_line': [patcher(loader('eye_line'), eye_line_converter(), [981, 206], basesize=basesize),
                 patcher(loader('eye_line'), eye_line_sub_converter(), [1129, 110], basesize=basesize)],
    'lip': [patcher(loader('lip'), lip_converter(), [1868, 3183], basesize=basesize)],
}

manager = model_manager(model='firina', displayname='フィリナ', patchers=patchers, options={})
