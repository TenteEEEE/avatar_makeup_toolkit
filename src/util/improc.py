import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps


def perspective_transform(img, matrix):
    homography = skt.ProjectiveTransform(matrix=matrix)
    out = skt.warp(img, homography)
    return out


def affine_transform(img, arrx, arry, smoothx=False, smoothy=False, mvx=10, mvy=10):
    [r, c, d] = img.shape
    src_cols = np.linspace(0, c, int(np.sqrt(len(arrx))))
    src_rows = np.linspace(0, r, int(np.sqrt(len(arry))))
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    if smoothx:
        lx = len(arrx)
        arrx = np.convolve(arrx, np.ones(mvx) / mvx, mode='valid')
        arrx = skt.resize(arrx, (lx, 1), anti_aliasing=True, mode='reflect')[:, 0]
    if smoothy:
        ly = len(arry)
        arry = np.convolve(arry, np.ones(mvy) / mvy, mode='valid')
        arry = skt.resize(arry, (ly, 1), anti_aliasing=True, mode='reflect')[:, 0]
    dst_rows = src[:, 1] + arrx
    dst_cols = src[:, 0] + arry
    dst = np.vstack([dst_cols, dst_rows]).T
    affin = skt.PiecewiseAffineTransform()
    affin.estimate(src, dst)
    return skt.warp(img, affin)


def resize(img, mag):
    if isinstance(img, np.ndarray):
        return skt.resize(img, (np.int(img.shape[0] * mag[0]), np.int(img.shape[1] * mag[1])), anti_aliasing=True, mode='reflect')
    else:
        return img.resize((int(img.size[0] * mag[1]), int(img.size[1] * mag[0])))


def mirror(img, axis=0):
    if isinstance(img, np.ndarray):
        if axis == 0:
            return np.concatenate([img, img[::-1]], axis=0)
        else:
            return np.concatenate([img, img[:, ::-1]], axis=1)
    else:
        if axis == 0:
            tmp = ImageOps.flip(img)
            dst = Image.new('RGBA', (img.width, img.height * 2))
            dst.paste(img, (0, 0))
            dst.paste(tmp, (0, img.height))
        else:
            tmp = ImageOps.mirror(img)
            dst = Image.new('RGBA', (img.width * 2, img.height))
            dst.paste(img, (0, 0))
            dst.paste(tmp, (img.width, 0))
        return dst


def alpha_brend(ref, template, pos=[0, 0]):
    r, c, d = template.shape
    mask = template[:, :, -1]
    ref[pos[0]:pos[0] + r, pos[1]:pos[1] + c, :3] = ref[pos[0]:pos[0] + r, pos[1]:pos[1] + c, :3] * (1. - mask[:, :, None]) + template[:, :, :3] * mask[:, :, None]
    return ref


def overlay(ref, template, pos=[0, 0]):
    ovl = Image.new("RGBA", ref.size)
    ovl.paste(template, pos)
    ref = Image.alpha_composite(ref, ovl)
    return ref


def overlay_with_mask(ref, template, mask, pos=[0, 0]):
    pad = Image.new("RGBA", ref.size)
    ovl = Image.new("RGBA", ref.size)
    pad.paste(template, pos)
    ovl = Image.composite(pad, ovl, mask)
    ref = Image.alpha_composite(ref, ovl)
    return ref


def masking(ref, mask):
    tmp = Image.new("RGBA", ref.size)
    return Image.composite(ref, tmp, mask)
    
def rotate(img, deg, resize=True):
    return skt.rotate(img, deg, resize=resize)
