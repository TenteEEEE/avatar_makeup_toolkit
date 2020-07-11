from PIL import Image
from src.util import improc


class patcher():
    """
    patcher provides patched images via various converters
    """

    def __init__(self, name, base_tex="./avatar_texture/quiche/face.png", mask_tex=None, loader=None, converters={}, options={}):
        self.name = name
        self.base = Image.open(base_tex)
        self.base_size = self.base.size
        self.loader = loader
        self.converters = converters
        if mask_tex is None:
            self.mask = mask_tex
        else:
            self.mask = Image.open(mask_tex).convert('L')
        try:
            self.options = options['options']
        except:
            self.options = options

    def __len__(self):
        return self.loader.data_num

    def patch(self, index, transparent=False):
        if transparent:
            patched = Image.new("RGBA", self.base_size)
        else:
            patched = self.base.copy()
        query = self.loader.make_query(index)
        if len(query) == 0:
            return None
        images = self.loader.load_imgs_by_query(query)
        for key in self.converters.keys():
            if key in self.options.keys():
                if self.options[key] < 0: # Ignore patching
                    continue
                elif self.options[key] > 0: # Index overwite
                    images[key] = self.loader.load_img(self.options[key], key)
            cvts = self.converters[key]
            cvts = [cvts] if type(cvts) is not list else cvts
            for cvt in cvts:
                cvt.options = self.options
                converted = cvt.get_converted(images[key])
                position = [int(converted['position'][i] * self.base_size[i]) for i in range(2)]
                if self.mask is None:
                    patched = improc.overlay(patched, converted['image'], position)
                else:
                    patched = improc.overlay_with_mask(patched, converted['image'], self.mask, position)
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
