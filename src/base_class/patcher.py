import os
from PIL import Image
try:
    from util import improc
except:  # Jupyter env
    from src.util import improc


class patcher:
    def __init__(self, loader, converter, position=[0., 0.], basesize=2048, options={}):
        self.loader = loader
        self.converter = converter
        self.basesize = basesize
        self.position = position
        # when the position is > 1.0, it normalizes the position by basesize
        if True in [p > 1. for p in self.position]:
            self.position = [p / basesize for p in self.position]
        self.options = options
        self.set_options(self.options)

    def patch(self, texture, index, material=None, mask=None):
        if material is None:
            material = self.load_img(index)
        material = self.convert(material)
        position = [round(self.position[i] * texture.size[i]) for i in range(2)]
        if material is not None:  # if index is out of bounds or <0, material is None
            if mask is None:
                texture = improc.overlay(texture, material, position)
            else:
                texture = improc.overlay_with_mask(patched, material, mask, position)
        return texture

    def set_options(self, options):
        self.loader.options = options
        self.converter.options = options

    def load_img(self, index):
        return self.loader.load_img(index)

    def convert(self, image):
        return self.converter.convert(image)


class model_manager:
    def __init__(self, model, displayname='キッシュ', rootdir="./avatar_texture/", patchers={}, options={}):
        self.model = model
        self.displayname = displayname
        self.rootdir = rootdir + '/' if rootdir[-1] is not '/' else rootdir
        self.patchers_dict = patchers
        self.support_parts = patchers.keys()
        # if mask_tex is not None:
        #     self.mask = Image.open(mask_tex).convert('L')
        # else:
        #     self.mask = None
        # try:
        #     self.options = options['options']
        # except:
        self.options = options

    def __len__(self):
        return len(self.patchers)

    def patch_part(self, part, setindex, transparent=False):
        patched = Image.open(f'{self.rootdir}{self.model}/{part}.png')
        if transparent:
            patched = Image.new("RGBA", patched.size)
        if os.path.exists(f'{self.rootdir}{self.model}/{part}_mask.png'):
            mask = Image.open(f'{self.rootdir}{self.model}/{part}_mask.png').convert('L')
        else:
            mask = None

        part_patchers = self.patchers_dict[part]
        for material in part_patchers.keys():
            index = setindex
            if material in self.options.keys():
                if self.options[material] < 0:  # Ignore patching
                    continue
                elif self.options[material] > 0:  # Index overwite
                    index = self.options[material]
            for p in part_patchers[material]:
                p.set_options(self.options)
                patched = p.patch(patched, index, mask=mask)
        return patched

    def ask(self, question, default=False, default_msg=None):
        if default_msg is None:
            default_msg = 'y' if default else 'n'
        message = question + ' [default:' + default_msg + '] (y/n):'
        while True:
            ans = input(message)
            if ans in ['', 'y', 'n']:
                break
        matching_char = ['', 'y'] if default else ['', 'n']

        if ans in matching_char:
            return True if default else False
        else:
            return False if default else True
